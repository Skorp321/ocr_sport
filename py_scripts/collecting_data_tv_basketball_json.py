#!/usr/bin/env python
# coding: utf-8

from PIL import Image
import os
import pandas as pd
import numpy as np
import json
from tqdm import tqdm
import math

anno_pathes_json = []
file_name = ".json"

# For home
absolute_path = "data\\TV_data\\basketball"
crop_path = "numbers\\basketball_numbers"

# For laptop
# absolute_path = 'D:\\Datasets\\TV_data'
# crop_path = 'D:\\Datasets\\basketball_numbers'

alpha = 0.2
num = 0
annos_list = []
anno_dict = {"file_name": [], "text": []}
pathes_list = []

if not os.path.exists(crop_path):
    os.makedirs(crop_path)

for root, dirs, files in os.walk(absolute_path):
    for file in files:
        # проверяем, есть ли заданный файл в списке файлов текущей папки
        if (file_name in file) & (".jsonl" not in file):
            # если есть, то добавляем путь в список
            anno_pathes_json.append(os.path.join(root, file))

for anno in tqdm(anno_pathes_json):
    with open(anno, "r") as f:
        data = json.load(f)

    # Преобразуем json  в dataFrame
    points = pd.read_json(json.dumps(data["shapes"]))

    x = pd.read_json(anno, orient="index")
    frame = x.iloc[3, :][0]
    frame = frame.replace(".", "-")

    img_path = anno.replace("anno", "frames")
    img_path = img_path.replace(".json", ".jpeg")
    img_path = img_path.replace("BallerTV", "TV_data")
    img = Image.open(img_path)

    for j in range(len(points)):
        out_file = {}
        point_obj = pd.DataFrame(points.iloc[j, 0:2])
        point = point_obj.iloc[1, :]
        label = point_obj.iloc[0, :]
        split_label = label[j].split("_")
        number = split_label[-1]

        for box in point:

            if number.isdigit() & (len(split_label) == 3):

                xtl, ytl, xbr, ybr = (
                    int(box[0][0]),
                    int(box[0][1]),
                    int(box[1][0]),
                    int(box[1][1]),
                )

                x_dif = np.abs(xtl - xbr)
                y_dif = np.abs(ytl - ybr)

                xtl = int(xtl - math.ceil(alpha * (x_dif / 2)))
                xbr = int(xbr + math.ceil(alpha * (x_dif / 2)))
                ytl = int(ytl - math.ceil(alpha * (y_dif / 2)))
                ybr = int(ybr + math.ceil(alpha * (y_dif / 2)))

                # Сделаем кроп номера на футболке
                croppped_image = img.crop((xtl, ytl, xbr, ybr))
                full_path = crop_path + "\\" + str(number)

                if not os.path.exists(full_path):
                    os.makedirs(full_path)
                    # print(f'Папка {number} создана')

                res_path = full_path + "\\" + f"TV_data_{str(frame)}_{num}example.jpg"
                num += 1

                croppped_image.save(res_path)
