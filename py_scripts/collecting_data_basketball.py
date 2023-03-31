from PIL import Image
import os
import pandas as pd
import numpy as np
import json
from tqdm import tqdm

anno_pathes_json = []
file_name = ".json"

absolute_path = "data\\basketball\\16-11-2022"
crop_path = "numbers\\basketball_numbers"

num = 0
alpha = 0.2
annos_list = []
anno_dict = {"file_name": [], "text": []}
pathes_list = []
xx = []

if not os.path.exists(crop_path):
    os.makedirs(crop_path)

for root, dirs, files in os.walk(absolute_path):
    for file in files:
        # проверяем, есть ли заданный файл в списке файлов текущей папки
        if (file_name in file) & (".jsonl" not in file):
            # если есть, то добавляем путь в список
            anno_pathes_json.append(os.path.join(root, file))

for i, anno in enumerate(anno_pathes_json):
    with open(anno, "r") as f:
        data = json.load(f)

    frames = pd.read_json(json.dumps(data["frames"]))
    print(f"{i + 1}ая папка из {len(anno_pathes_json)}")

    for i in tqdm(range(len(frames))):

        img_name = frames["img_name"][i]
        bboxes = frames["detections"][i]

        anno_path = anno.replace("anno", "frames")
        anno_path = anno_path.replace(".json", "\\")
        anno_path_fin = anno_path + str(img_name)
        xx.append(anno_path)

        img = Image.open(anno_path_fin)

        # Создание объекта ImageDraw для рисования

        for detection in bboxes:

            ocr_jersey = detection["ocr_jersey"]

            if ocr_jersey != "-1":
                jersey_bbox_global = detection["jersey_bbox_global"]
                xtl = int(jersey_bbox_global[0])
                ytl = int(jersey_bbox_global[1])
                xbr = int(jersey_bbox_global[2])
                ybr = int(jersey_bbox_global[3])

                x_dif = np.abs(xtl - xbr)
                y_dif = np.abs(ytl - ybr)

                xtl = xtl - alpha * (x_dif / 2)
                xbr = xbr + alpha * (x_dif / 2)
                ytl = ytl - alpha * (y_dif / 2)
                ybr = ybr + alpha * (y_dif / 2)

                croppped_image = img.crop((xtl, ytl, xbr, ybr))
                full_path = crop_path + "\\" + str(ocr_jersey)
                res_path = full_path + "\\" f"basketball_{num}example.jpg"
                num += 1

                if not os.path.exists(full_path):
                    os.makedirs(full_path)

                croppped_image.save(res_path)
