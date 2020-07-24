"""

@author Thiago Raulino Dal Pont
"""
import csv
import os
import shutil
import time
from os import listdir
from os.path import isfile, join


def list_files_in_dir(path, ext=""):
    files = [f for f in listdir(path) if isfile(join(path, f))]

    print("Files in: ", path)
    for file in files:
        print("\t", file)


def clear_dir(path):
    file_list = [f for f in os.listdir(path) if f.endswith(".jpg")]
    for f in file_list:
        os.remove(os.path.join(path, f))


def write_to_file(file, content):
    with open(file, "w+") as file_w:
        file_w.write(content)


def copy_file(file, dest):
    shutil.copy2(file, dest)


def write_dict_to_file(file, dict_content):
    w = csv.writer(open(file, "w+"))
    for key, val in dict_content.items():
        w.writerow([key, val])


def elapsed_time(time_dt):
    t = int(time_dt * 1000)
    t_millis = t % 1000
    t_secs = int(t / 1000) % 60
    t_mins = int(t / (1000 * 60)) % 60
    t_hours = int(t / (1000 * 60 * 60)) % 24

    text = str(t_hours).zfill(2) + ":" + str(t_mins).zfill(2) + ":" + str(t_secs).zfill(2) + "." + \
           str(t_millis).zfill(3)
    print("Elapsed time:\t", text)

