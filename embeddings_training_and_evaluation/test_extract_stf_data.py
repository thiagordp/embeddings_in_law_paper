"""

"""
import glob
import os
import random
import time
from multiprocessing.pool import Pool

import tqdm
import numpy as np

from pre_processing import extract_texts_pdf
from utils.constants import *


def extract_text_pdf(path):
    try:
        digital_text = extract_texts_pdf.digital_pdf_file(path)

        len_digital = len(digital_text)

        if len_digital > 500:
            return digital_text

        ocr_text = extract_texts_pdf.ocr_pdf_file(path)
        len_ocr = len(ocr_text.split())

        if len_ocr > 50:
            return ocr_text
    except:
        pass

    return ""


def move_files_to_splits():
    for type_doc in TJ_SC_CASES_PATH:
        print(type_doc)
        file_list = glob.glob(type_doc + "*.rtf")
        file_list.extend(glob.glob(type_doc + "*.pdf"))
        file_list.extend(glob.glob(type_doc + "*.txt"))
        # Split database
        path_split = np.array_split(file_list, 20)

        for i in tqdm.tqdm(range(20)):
            s = path_split[i]

            dest_path = type_doc + "split_" + str(i + 1)

            for file_path in s:
                token = file_path.split("/")[-1]
                os.rename(file_path, dest_path + "/" + token)


def thread_process(path):
    time.sleep(random.random() * 5)
    th_id = random.randint(0, 100)

    files = glob.glob(path[0] + "/*")
    files = [file for file in files if file.find(".txt") == -1]

    for i in range(len(files)):
        pdf_file = files[i]
        print("Thread ", th_id, ":\t", round(100 * (i + 1) / len(files), 2), "%")

        text = extract_text_pdf(pdf_file)
        file_name = pdf_file.replace(".pdf", ".txt")

        if file_name.find(".txt") == -1:
            file_name += ".txt"
        with open(pdf_file.replace(".pdf", ".txt"), "w+") as f:
            f.write(text)


if __name__ == "__main__":
    print("")

    # move_files_to_splits()

    for doc in STF_CASES_PATH:
        print("Processing ", doc)

        folders = glob.glob(doc + "*")
        folders = [[folder] for folder in folders]

        pool = Pool(1)
        results = pool.map(thread_process, folders)
        pool.close()
        pool.join()
