#!/usr/bin/env python
# coding: utf-8

import xml.etree.ElementTree as ET
from PIL import Image
import os
import pandas as pd
import numpy as np
import json
from tqdm import tqdm


anno_pathes_json = []
file_name = ".json"

alpha = 0.1
num = 0
annos_list = []
anno_dict = {"file_name": [], "text": []}
pathes_list = []


# For home
absolute_path = "data\\FIBA3x3\\20-03-2023\\anno"
crop_path = "numbers\\streetball_numbers"

# For laptop
# absolute_path = 'D:\\Datasets\\TV_data\\volleyball\\00-00-00'
# crop_path = 'D:\\Datasets\\crops1'

print("Collecting data fiba new!")
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
    frames = pd.read_json(json.dumps(data))

    for frame in frames["frames"]:
        img_name = frame["img_name"]
        anno_path = anno.replace(".json", "")
        anno_path = anno_path.replace("anno", "jersey_frames")
        jpg_path = os.path.join(anno_path, img_name)

        img = Image.open(jpg_path)

        for det in frame["detections"]:
            if det["ocr_jersey"] != "-1":
                point = det["jersey_bbox_global"]
                number = det["ocr_jersey"]

                xtl, ytl, xbr, ybr = (
                    int(point[0]),
                    int(point[1]),
                    int(point[2]),
                    int(point[3]),
                )

                x_dif = np.abs(xtl - xbr)
                y_dif = np.abs(ytl - ybr)

                xtl = xtl - alpha * (x_dif / 2)
                xbr = xbr + alpha * (x_dif / 2)
                ytl = ytl - alpha * (y_dif / 2)
                ybr = ybr + alpha * (y_dif / 2)

                # Сделаем кроп номера на футболке
                croppped_image = img.crop((xtl, ytl, xbr, ybr))
                full_path = crop_path + "\\" + str(number)

                if not os.path.exists(full_path):
                    os.makedirs(full_path)
                    # print(f'Папка {number} создана')

                name = img_name.replace(".jpeg", "")
                res_path = full_path + "\\" + f"TV_data_{name}_{num}example.jpg"
                num += 1

                croppped_image.save(res_path)
