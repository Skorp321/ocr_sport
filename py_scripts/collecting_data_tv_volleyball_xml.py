#!/usr/bin/env python
# coding: utf-8

import xml.etree.ElementTree as ET
from PIL import Image
import os
import pandas as pd
import numpy as np
from tqdm import tqdm
import math

# for pc
crop_path = "numbers\\volleyball_numbers"
absolute_path = "data\\TV_data\\volleyball"

# for laptop
# crop_path = "D:\\Datasets\\crops"
# absolute_path = "D:\\Datasets\\TV_data"

if not os.path.exists(crop_path):
    os.makedirs(crop_path)

file_name = "annotations.xml"
jpeg_name = ".jpeg"

nums = []
num = 0
folder_pathes = []
pathes_list = []
annos_list = []
anno_dict = {"file_name": [], "text": []}
num = 0
alpha = 0.2
res = {}

anno_pathses = {}
img_pathses = {}
# пройдемся рекурсивно по всем папкам, начиная с absolute_path
for root, dirs, files in os.walk(absolute_path):

    # проверяем, есть ли заданный файл в списке файлов текущей папки
    folder_name = os.path.split(root)
    # (folder_name[1] in root) & ('frames' in root)  &

    if file_name in files:
        # если есть, то добавляем путь в список
        anno_pathses[folder_name[1]] = os.path.join(root, file_name)

    for file in files:

        if (
            (jpeg_name in file)
            & (folder_name[1] not in img_pathses)
            & ("0_processed" not in root)
            & ("00-00-00" not in root)
        ):
            img_pathses[folder_name[1]] = root

for key in tqdm(anno_pathses.keys()):

    # Загрузим XML файл
    tree = ET.parse(anno_pathses[key])

    # Получим корневой элемент XML файла
    root = tree.getroot()

    # Проитерируемся по дочерним элементам корня
    for image in root.findall("image"):

        image_id = image.get("id")
        file_name = image.get("name")

        file_name = os.path.split(file_name)
        folder_name = os.path.split(file_name[0])
        file_name = os.path.join(img_pathses[key], file_name[1])

        if key not in file_name:
            file_name = file_name.replace(key, folder_name)

        # Переберем все baundingbox`s
        for box in image.findall("box"):

            image = Image.open(file_name)

            label = box.get("label")

            # Проверим является ли метка меткой номера
            if label == "Jersey":
                xtl = int(float(box.get("xtl")))
                ytl = int(float(box.get("ytl")))
                xbr = int(float(box.get("xbr")))
                ybr = int(float(box.get("ybr")))
                number = box.find('attribute[@name="number"]').text
                if number == "-1":
                    continue

                x_dif = np.abs(xtl - xbr)
                y_dif = np.abs(ytl - ybr)

                xtl = int(xtl - math.ceil(alpha * (x_dif / 2)))
                xbr = int(xbr + math.ceil(alpha * (x_dif / 2)))
                ytl = int(ytl - math.ceil(alpha * (y_dif / 2)))
                ybr = int(ybr + math.ceil(alpha * (y_dif / 2)))

                # Сделаем кроп номера на футболке
                croppped_image = image.crop((xtl, ytl, xbr, ybr))
                full_path = crop_path + "\\" + str(number)
                num += 1

                if not os.path.exists(full_path):
                    os.makedirs(full_path)
                    # print(f'Папка {number} создана')

                res_path = full_path + "\\" + f"TV_data_{str(key)}_id-{image_id}.jpg"

                croppped_image.save(res_path)
