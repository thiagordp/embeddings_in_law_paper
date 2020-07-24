"""

@authors Thiago Raulino Dal Pont
"""
import glob
import os
import random
import time

from multiprocessing.pool import Pool

import pandas as pd

from utils import make_request

PATH_CASES = "cases/"
PATH_LINKS = "links/"
PATH_ACORDAOS = "acordaos/"
PATH_REP_GERAL = "repercussao_geral/"

used_ids = []


def split_download_links(path, chunk_size):
    df = pd.read_csv(path, index_col=0)

    len_df = len(df)
    if chunk_size > len_df:
        chunk_size = len_df

    dfs = list()
    number_chunks = len_df // chunk_size + 1
    for i in range(number_chunks):
        dfs.append(df[i * chunk_size:(i + 1) * chunk_size])

    token = path.split("/")
    part_path = "/".join(token[:-1])

    for i in range(number_chunks):
        p = part_path + "/split_" + str(i + 1) + ".csv"
        if len(dfs[i]) > 0:
            dfs[i].to_csv(p)

    return dfs


def download_thread(arg):
    th_id, path = arg

    df = pd.read_csv(path, index_col=0)
    len_df = len(df)

    tokens = path.split("/")
    base_path = "/".join(tokens[:-1]) + "/"

    for i in range(len_df):
        for j in range(1, 5):
            try:
                time.sleep(random.randint(1, 5) / 2)
                url = df["url"].iloc[i]

                doc = make_request.get_page(url)

                new_id = -1
                while new_id == -1 or new_id in used_ids:
                    new_id = random.randint(1, 10000000000)

                used_ids.append(new_id)

                file_name = base_path + str(new_id) + ".pdf"

                print("Thread", th_id, ":\t ", str(i + 1), " of ", len_df, ":\tWriting to:\t", file_name)
                with open(file_name, "wb+") as f:
                    f.write(doc.content)
                break
            except:
                time.sleep(10)
            time.sleep(random.randint(5, 7))

    print("Finished: ", path)

    return None


def get_links_from_files(files, tribunal, type_doc):
    if len(files) == 0:
        return None

    pds = []
    for file in files:
        print(file)
        df = pd.read_csv(file, index_col=0)
        pds.append(df)

    concat_df = pd.concat(pds, ignore_index=True)
    # tokens = files[0].split("/")

    concat_path = "data/" + tribunal + "/" + PATH_CASES + type_doc + "/" + "merged.csv"
    print(concat_path)

    try:
        concat_df["url"] = concat_df["url"].apply(lambda x: x.replace("\r\n", "").replace("\n", ""))
    except:
        pass
    concat_df.to_csv(concat_path)

    return concat_path


def download():
    print("\n\nDOWNLOAD CASES\n\n")

    print("STF")
    print("\tDownloading acordaos:")

    tribunais = os.listdir("../data/")

    print("\n\nMERGE FILES\n===================")
    # Merge files
    for tribunal in tribunais:
        print("TRIBUNAL:", tribunal.upper())
        type_documents = os.listdir("data/" + tribunal + "/" + PATH_LINKS)

        for type_doc in type_documents:
            base_path = "data/" + tribunal + "/" + PATH_LINKS + type_doc + "/*.csv"

            files = glob.glob(base_path)
            get_links_from_files(files, tribunal, type_doc)

    # Split dataframe in equal parts
    print("\n\nSPLIT DATAFRAME\n====================")
    for tribunal in tribunais:
        print("TRIBUNAL:", tribunal.upper())
        type_documents = os.listdir("data/" + tribunal + "/" + PATH_LINKS)

        for type_doc in type_documents:
            base_path = "data/" + tribunal + "/" + PATH_CASES + type_doc + "/*.csv"

            files = glob.glob(base_path)
            for file in files:
                split_download_links(file, 15000)

    for tribunal in tribunais:
        print("Tribunal:", tribunal.upper())

        type_documents = os.listdir("data/" + tribunal + "/" + PATH_LINKS)
        type_documents.sort()

        for type_doc in type_documents:
            base_path = "data/" + tribunal + "/" + PATH_CASES + type_doc + "/*.csv"

            files = glob.glob(base_path)

            files = [x for x in files if "merged" not in x]
            s = [[i, files[i]] for i in range(len(files))]

            pool = Pool(len(files))
            results = pool.map(download_thread, s)
            pool.close()
            pool.join()
