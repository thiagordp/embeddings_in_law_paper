"""

@author Thiago Raulino Dal Pont
"""
import os
import re

import tqdm

from pre_processing import extract_texts_rtf, extract_texts_pdf
from pre_processing.text_preprocessing import clean_text, clean_text_ret
from utils.constants import *
import glob

tribunals = [
    #TJ_SC_CASES_PATH,
    # STJ_CASES_PATH,
    #STF_CASES_PATH,
    # OTHERS_PATH
    #JUSBRASIL_PATH
]


def convert_process_to_txt(tribunal_path):
    print("Convert processes to TXT")
    print("=======================================================================================================")

    for type_doc in tribunal_path:

        print("-------------------------------------------------------------------------------------------------------")
        print(type_doc)

        # print("Extracting texts from PDF files")
        # file_paths_pdf = glob.glob(type_doc + "/*.pdf")
        # file_paths_pdf.extend(glob.glob(type_doc + "/split*/*pdf"))
        #
        # print("PDF files found:\t", len(file_paths_pdf))
        # for f in tqdm.tqdm(file_paths_pdf):
        #     try:
        #         extract_texts_pdf.digital_pdf_file(f)
        #     except Exception as e:
        #         print("Error", e)

        print("Extracting texts from RTF files")
        file_paths_rtf = []
        # file_paths_rtf = glob.glob(type_doc + "/*.rtf")
        # file_paths_rtf.extend(glob.glob(type_doc + "/split*/*.rtf"))
        file_paths_rtf.extend(glob.glob(type_doc + "/*.XXX"))
        file_paths_rtf.extend(glob.glob(type_doc + "/split*/*.XXX"))

        print("RTF files found:\t", len(file_paths_rtf))

        for file in tqdm.tqdm(file_paths_rtf):
            extract_texts_rtf.extract_text_rtf(file)

        file_paths_doc = glob.glob(type_doc + "/*.doc*")
        file_paths_doc.extend(glob.glob(type_doc + "/split*/*.doc*"))
        file_paths_doc.extend(glob.glob(type_doc + "/split*/*.odt"))
        file_paths_doc.extend(glob.glob(type_doc + "/*.odt"))

        print("DOC files found:\t", len(file_paths_doc))

        for f in tqdm.tqdm(file_paths_doc):
            extract_texts_rtf.extract_text_doc(f)


def merge_air_transport():
    tribunal_path = DATASET_BASE_PATH + "misto/cases/"

    count = 0
    tokens = 0
    with open("temp.txt", "w+") as air_file:
        for dir_path, dir_names, filenames in os.walk(tribunal_path):
            print(dir_path)

            for filename in tqdm.tqdm([f for f in filenames if f.endswith(".txt")]):
                file_path = os.path.join(dir_path, filename)

                with open(file_path, "r") as text_file:
                    text = text_file.read().replace("\n", " ").replace("  ", " ")
                    low_text = re.sub(" +", " ", text)

                    low_text = clean_text_ret(low_text)

                    if len(low_text) < 100:
                        continue

                    tokens += len(low_text.split())
                    # air_file.write(low_text + "\n")
                    count += 1

    print("Count:", count)
    print("Tokens:", tokens)


def check_size_context():
    total_docs = 0
    consumer_docs = 0
    air_transport_docs = 0

    total_tokens = 0
    consumer_tokens = 0
    air_transport_tokens = 0

    for dir_path, dir_names, filenames in os.walk(DATASET_BASE_PATH):
        print(dir_path)
        for filename in tqdm.tqdm([f for f in filenames if f.endswith(".txt")]):
            file_path = os.path.join(dir_path, filename)
            with open(file_path) as f:
                text = f.read().lower()
                tokens = text.split()
                total_tokens += len(tokens)
                total_docs += 1

                if text.find("consumidor") != -1 or \
                        text.find("cdc") != -1 or \
                        text.find("código de defesa do consumidor") != -1:
                    consumer_tokens += len(tokens)
                    consumer_docs += 1

                    if text.find("aéreo") != -1 or text.find("aérea") != -1:
                        air_transport_tokens += len(tokens)
                        air_transport_docs += 1

    print("Total tokens:         ", total_tokens)
    print("Consumer tokens:      ", consumer_tokens)
    print("Air transport tokens: ", air_transport_tokens)

    print("Total docs:         ", total_docs)
    print("Consumer docs:      ", consumer_docs)
    print("Air transport docs: ", air_transport_docs)


def merge_text_files(tribunal_path):
    print("Merge text files")
    print("=======================================================================================================")

    print(tribunal_path)
    c = 0
    a = 0
    f = 0

    with open(FULL_BASE_PATH, "a+") as full_file, \
            open(CONSUMER_BASE_PATH, "a+") as cdc_file, \
            open(AIR_BASE_PATH, "a+") as air_file:

        for dir_path, dir_names, filenames in os.walk(tribunal_path):
            print(dir_path)

            for filename in tqdm.tqdm([f for f in filenames if f.endswith(".txt")]):
                file_path = os.path.join(dir_path, filename)

                with open(file_path, "r") as text_file:
                    text = text_file.read().replace("\n", " ").replace("  ", " ")
                    low_text = re.sub(" +", " ", text)

                    low_text = clean_text_ret(low_text)
                    len_split = len(low_text.split())

                    if len(low_text) < 100:
                        continue

                    f += len_split
                    # f += 1
                    # full_file.write(low_text + "\n")

                    if low_text.find("direito do consumidor") != -1 or \
                            low_text.find("consumidor") != -1 or \
                            low_text.find("relação de consumo") != -1 or \
                            low_text.find("direito consumidor") != -1 or \
                            low_text.find("relação consumo") != -1:

                        # cdc_file.write(low_text + "\n")

                        c += len_split
                        # c += 1

                        if low_text.find("companhia aérea") != -1 or \
                                low_text.find("linha aérea") != -1 or \
                                low_text.find("aérea") != -1 or \
                                low_text.find("aéreo") != -1:

                            # air_file.write(low_text + "\n")
                            a += len_split
                            # a += 1

        print("Count:\t", f, c, a)

    return f, c, a


if __name__ == "__main__":
    print("DATABASE ASSEMBLY")
    merge_air_transport()

    for tribunal in tribunals:
        c1 = c2 = c3 = 0
        print(tribunal)

        for type_doc in tribunal:
            _f, _c, _a = merge_text_files(type_doc)

            print("type_doc: ", _f, _c, _a)
            c1 += _f
            c2 += _c
            c3 += _a

        print("tribunal: ", c1, c2, c3)
