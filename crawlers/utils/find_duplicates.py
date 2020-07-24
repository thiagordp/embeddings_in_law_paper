"""
Given a folder, walk through all files within the folder and subfolders
and get list of all files that are duplicates
The md5 checcksum for each file will determine the duplicates
"""

import os
import hashlib
from collections import defaultdict
import csv
from operator import itemgetter

import tqdm

from utils.constants import *

# src_folder = PATH_DOWNLOAD_AC.replace("acordaos/", "")
src_folder = "/data/misto/cases"


def keep_older_file(list_files):
    dict_file = {}
    for f in list_files:
        dict_file[f] = os.stat(f).st_mtime
    sorted_files = sorted(dict_file.items(), key=itemgetter(1))

    delete = len(sorted_files) - 1
    for x in range(0, delete):
        os.remove(sorted_files[x][0])


def generate_md5(fname, chunk_size=1024):
    """
    Function which takes a file name and returns md5 checksum of the file
    """
    hash = hashlib.md5()
    with open(fname, "rb") as f:
        # Read the 1st block of the file
        chunk = f.read(chunk_size)
        # Keep reading the file until the end and update hash
        while chunk:
            hash.update(chunk)
            chunk = f.read(chunk_size)

    # Return the hex checksum
    return hash.hexdigest()


if __name__ == "__main__":
    """
    Starting block of script
    """

    # The dict will have a list as values
    md5_dict = defaultdict(list)

    file_types_in_scope = ["pdf", "txt", "rtf"]

    # Walk through all files and folders within directory
    for path, dirs, files in os.walk(src_folder):
        print("Analyzing {}".format(path))
        for each_file in tqdm.tqdm(files):
            if each_file.split(".")[-1].lower() in file_types_in_scope:
                # The path variable gets updated for each subfolder
                file_path = os.path.join(os.path.abspath(path), each_file)
                # If there are more files with same checksum append to list
                md5_dict[generate_md5(file_path)].append(file_path)

    # Identify keys (checksum) having more than one values (file names)
    duplicate_files = (val for key, val in md5_dict.items() if len(val) > 1)

    print("Logging.")

    # Write the list of duplicate files to csv file
    with open("../duplicates.csv", "w") as log:
        # Lineterminator added for windows as it inserts blank rows otherwise
        csv_writer = csv.writer(log, quoting=csv.QUOTE_MINIMAL, delimiter=",", lineterminator="\n")
        header = ["File Names"]
        csv_writer.writerow(header)

        for file_name in duplicate_files:
            csv_writer.writerow(file_name)

    print("Removing Duplicates")

    duplicates = [val for key, val in md5_dict.items() if len(val) > 1]
    for duplicate in tqdm.tqdm(duplicates):
        keep_older_file(duplicate)

    print("Done")
