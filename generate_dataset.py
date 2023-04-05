import subprocess


def gen_dataset():
    subprocess.run(["python", "py_scripts\\collecting_data_tv_basketball_json.py"])
    subprocess.run(["python", "py_scripts\\collecting_data_tv_basketball_xml.py"])
    subprocess.run(["python", "py_scripts\\collecting_data_tv_volleyball_xml.py"])
    subprocess.run(["python", "py_scripts\\collecting_data_tv_volleyball_new_json.py"])
    subprocess.run(["python", "py_scripts\\collecting_data_fiba.py"])
    subprocess.run(["python", "py_scripts\\collecting_data_ncaa_basketball_json.py"])
    subprocess.run(["python", "py_scripts\\collecting_data_basketball.py"])
    subprocess.run(["python", "py_scripts\\collecting_data_fiba_new.py"])
    return


if __name__ == "__main__":
    gen_dataset()
