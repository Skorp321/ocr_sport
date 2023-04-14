import pandas as pd
from sklearn.model_selection import train_test_split
import os

basketball_path = "numbers\\basketball_numbers"
streetball_path = "numbers\\streetball_numbers"
volleyball_path = "numbers\\volleyball_numbers"
file = "jpg"


def gen_annotations():
    annos_list = []
    pathes_list = []
    anno_dict = {"text": [], "file_name": []}

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

            anno_dict["file_name"] = pathes_list
            anno_dict["text"] = annos_list

    volleyball_df = pd.DataFrame(anno_dict, index=None)

    print("Number of training examples:", basketball_df.shape[0])
    print("Number of testing examples:", streetball_df.shape[0])
    print("Number of validation examples:", volleyball_df.shape[0])

    train_voll, test_voll = train_test_split(volleyball_df, test_size=0.2, shuffle=True)
    train_strit, test_strit = train_test_split(
        streetball_df, test_size=0.2, shuffle=True
    )
    train_basket, test_bascet = train_test_split(
        basketball_df, test_size=0.2, shuffle=True
    )

    test_voll.to_csv("for_test\\test_volleyball.csv")
    test_strit.to_csv("for_test\\test_stritball.csv")
    test_bascet.to_csv("for_test\\test_bascetball.csv")

    train_basket.to_csv("for_train\\train_bascetball.csv")
    train_strit.to_csv("for_train\\train_streetball.csv")
    train_voll.to_csv("for_train\\train_volleyball.csv")
    return


if __name__ == "__main__":
    if not os.path.exists(basketball_path):
        os.makedirs(basketball_path)

    if not os.path.exists(streetball_path):
        os.makedirs(streetball_path)

    if not os.path.exists(volleyball_path):
        os.makedirs(volleyball_path)

    gen_annotations()
    print("Annotations for dataset was generated!!!")
