import subprocess
import pandas as pd
from sklearn.model_selection import train_test_split
import os

basketball_path = "numbers\\basketball_numbers"
streetball_path = "numbers\\streetball_numbers"
volleyball_path = "numbers\\volleyball_numbers"
file = "jpg"

annos_list = []
pathes_list = []
anno_dict = {"text": [], "file_name": []}


def gen_dataset():
    subprocess.run(["python", "py_scripts\\collecting_data_tv_basketball_json.py"])
    subprocess.run(["python", "py_scripts\\collecting_data_tv_basketball_xml.py"])
    subprocess.run(["python", "py_scripts\\collecting_data_tv_volleyball_xml.py"])
    subprocess.run(["python", "py_scripts\\collecting_data_tv_volleyball_new_json.py"])
    subprocess.run(["python", "py_scripts\\collecting_data_fiba.py"])
    subprocess.run(["python", "py_scripts\\collecting_data_ncaa_basketball_json.py"])
    subprocess.run(["python", "py_scripts\\collecting_data_basketball.py"])
    return


def gen_annotations():
    for root, dirs, files in os.walk(basketball_path):
        for file in files:
            label = os.path.split(root)[-1]
            path = os.path.join(root, file)

            annos_list.append(str(label))
            pathes_list.append(path)
            anno_dict["text"] = annos_list
            anno_dict["file_name"] = pathes_list

    basketball_df = pd.DataFrame(anno_dict, index=None)

    annos_list = []
    pathes_list = []
    anno_dict = {"text": [], "file_name": []}

    for root, dirs, files in os.walk(streetball_path):
        for file in files:
            label = os.path.split(root)[-1]
            path = os.path.join(root, file)

            annos_list.append(str(label))
            pathes_list.append(path)
            anno_dict["text"] = annos_list
            anno_dict["file_name"] = pathes_list

    streetball_df = pd.DataFrame(anno_dict, index=None)

    annos_list = []
    pathes_list = []
    anno_dict = {"text": [], "file_name": []}

    for root, dirs, files in os.walk(volleyball_path):
        for file in files:
            label = os.path.split(root)[-1]
            path = os.path.join(root, file)

            annos_list.append(str(label))
            pathes_list.append(path)
            anno_dict["text"] = annos_list
            anno_dict["file_name"] = pathes_list

    volleyball_df = pd.DataFrame(anno_dict, index=None)

    train_voll, test_voll = train_test_split(volleyball_df, 0.2)
    train_strit, test_strit = train_test_split(streetball_df, 0.2)
    train_basket, test_bascet = train_test_split(basketball_df, 0.2)

    test_voll.to_csv("for_test\\test_volleyball.csv")
    test_strit.to_csv("for_test\\test_stritball.csv")
    test_bascet.to_csv("for_test\\test_bascetball.csv")

    train_basket.to_csv("for_train\\train_bascetball.csv")
    train_strit.to_csv("for_train\\train_streetball.csv")
    train_voll.to_csv("for_train\\train_volleyball.csv")
    return


if __name__ == "__main__":
    gen_dataset()
    gen_annotations()
