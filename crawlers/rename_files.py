"""
This process renames downloaded process files from courts as the crawler get them downloaded.
For each execution of this script renames all existing files and new ones, using unique random numbers for each file (Ex. 1234.pdf)

@author Thiago Raulino Dal Pont
"""

from utils.constants import *
import glob
import os
import random
import time
import tqdm

# Paths to process download location.
PATH = [PATH_DOWNLOAD_AC, PATH_DOWNLOAD_MC]


def main():
    # List of renamed files
    list_files = []
    # List of random numbers used to rename files.
    list_numbers = []

    while True:
        for type_doc in PATH:
            # List files
            text_file_paths = glob.glob(type_doc + "*")
            text_file_paths.extend(glob.glob(type_doc + "split*/*"))

            list_download_files = []
            for p in text_file_paths:
                # Ignore incomplete downloads and files already in the list of renamed files.
                if p.find(".part") == -1 and p not in list_files:
                    list_download_files.append(p)

            print("Renaming")
            for pdf_path in tqdm.tqdm(list_download_files):
                try:
                    # Get path to document
                    tokens = pdf_path.split("/")
                    folder = "/".join(tokens[:-1])

                    # Generate a unique random number
                    n = 0
                    while True:
                        n = random.randint(1, 10000000000)
                        if n not in list_numbers:
                            list_numbers.append(n)
                            break

                    # Rename file and insert to list of renamed files
                    file_name = str(n) + ".pdf"
                    os.rename(pdf_path, folder + "/" + file_name)
                    list_files.append(folder + "/" + file_name)
                except:
                    pass
        print("Sleeping")
        time.sleep(5)


if __name__ == "__main__":
    main()
