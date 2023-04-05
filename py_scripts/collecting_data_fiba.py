#!/usr/bin/env python
# coding: utf-8

import xml.etree.ElementTree as ET
from PIL import Image
import os
import pandas as pd
import numpy as np

from tqdm import tqdm
import math

crop_path = "numbers\\streetball_numbers"
absolute_path = "data\\FIBA3x3\\fiba3x3_tracking_135"

if not os.path.exists(crop_path):
    os.makedirs(crop_path)

file_name = "annotations.xml"

nums = []
num = 0
folder_pathes = []
pathes_list = []
annos_list = []
anno_dict = {"file_name": [], "text": []}

alpha = 0.2

anno_pathses = []

print("Collecting data fiba!")
# пройдемся рекурсивно по всем папкам, начиная с absolute_path
for root, dirs, files in os.walk(absolute_path):
    # проверяем, есть ли заданный файл в списке файлов текущей папки
    if file_name in files:
        # если есть, то добавляем путь в список
        anno_pathses.append(os.path.join(root, file_name))

for path in tqdm(anno_pathses):

    # Загрузим XML файл
    tree = ET.parse(path)

    # Получим корневой элемент XML файла
    root = tree.getroot()

    # Проитерируемся по дочерним элементам корня
    for image in root.findall("image"):

        image_id = image.get("id")
        file_name = image.get("name")
        # file_name = file_name.replace('/', '\\')
        file_name = os.path.join(absolute_path, file_name)
        if "fiba3x3/images/331/" in file_name:
            file_name = file_name.replace("fiba3x3/images/331", "frames")
        file_name = file_name.replace("frames", "frames_135")
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

                if str(number) == "-1":
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

                res_path = full_path + "\\" + f"fiba_{str(num)}example.jpg"

                croppped_image.save(res_path)

print()
