#!/usr/bin/env python
# coding: utf-8

from PIL import Image
import os
import pandas as pd
import numpy as np
import json
from tqdm import tqdm
import math


def script():

    print("Collecting data NCAA basketball json!")

    absolute_path = "data\\NCAA\\NCAA_1_jersey"
    crop_path = "numbers\\basketball_numbers"
    img_folder_path = "NCAA\\NCAA_1_tracking\\playerTrackingFrames"
    cor_path = "NCAA\\NCAA_1_jersey\\data\\tracksVisualised"

    num = 0
    x = 0
    alpha = 0.1
    num = 0
    annos_list = []
    anno_dict = {"file_name": [], "text": []}
    pathes_list = []

    if not os.path.exists(crop_path):
        os.makedirs(crop_path)

    file_name = ".json"
    jpeg_name = ".jpg"

    anno_pathses = {}
    img_pathses = {}
    # пройдемся рекурсивно по всем папкам, начиная с absolute_path
    for root, dirs, files in os.walk(absolute_path):

        # проверяем, есть ли заданный файл в списке файлов текущей папки

        # (folder_name[1] in root) & ('frames' in root)  &

        for file in files:

            folder_name = os.path.split(root)

            if file_name in file:
                # если есть, то добавляем путь в список
                anno_pathses[folder_name[1]] = root

    for root, dirs, files in os.walk(img_folder_path):

        for file in files:

            folder_name = os.path.split(root)

            if jpeg_name in file:

                img_pathses[folder_name[1]] = root

    for folder, path in tqdm(anno_pathses.items()):
        files = os.listdir(path)

        for file in files:
            if ".json" in file:
                anno = os.path.join(path, file)
                jpg_file = file.replace(".json", ".jpg")
                jpg_file = "frame_" + jpg_file
                img_path = os.path.join(img_pathses[folder], jpg_file)
                img = Image.open(img_path)
            else:
                continue

            with open(anno, "r") as f:
                data = json.load(f)

            points = pd.read_json(json.dumps(data["shapes"]))

            for _, shape in points.iterrows():
                out_file = {}

                if shape["shape_type"] == "rectangle":

                    label = shape["label"]

                    split_label = label.split("_")
                    number = str(split_label[-1])

                    if len(split_label) == 3:

                        [xtl, ytl], [xbr, ybr] = shape["points"]
                        # print(label, split_label, anno, img_path)
                        x_dif = np.abs(xtl - xbr)
                        y_dif = np.abs(ytl - ybr)

                        xtl = int(xtl - math.ceil(alpha * (x_dif / 2)))
                        xbr = int(xbr + math.ceil(alpha * (x_dif / 2)))
                        ytl = int(ytl - math.ceil(alpha * (y_dif / 2)))
                        ybr = int(ybr + math.ceil(alpha * (y_dif / 2)))

                        # Сделаем кроп номера на футболке
                        cropped_image = img.crop((xtl, ytl, xbr, ybr))

                        if str(number) == "5(1)":
                            number = "5"

                        full_path = crop_path + "\\" + str(number)

                        if not os.path.exists(full_path):
                            os.makedirs(full_path)

                        x = file.replace(".json", "")
                        res_path = full_path + "\\" + f"ncaa_{folder}-id{x}-{num}.jpg"
                        num += 1

                        annos_list.append(str(number))
                        pathes_list.append(res_path)
                        anno_dict["text"] = annos_list
                        anno_dict["file_name"] = pathes_list
                        # print(anno, img_path, x[-1], number, label)
                        cropped_image.save(res_path)


if __name__ == "__main__":
    script()
    print()
