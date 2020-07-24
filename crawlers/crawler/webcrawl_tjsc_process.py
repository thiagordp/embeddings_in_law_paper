"""

@author Thiago Raulino Dal Pont
"""
import datetime
import glob
import os
import random
import shutil
import time
from multiprocessing.pool import Pool

import numpy as np
import pandas as pd
import tqdm
import wget
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from utils import file_utils
from utils.constants import *

visited = [1]
total_count = 0


def save_links(path, links, date_init, date_finish):
    df = pd.DataFrame(links, columns=["url"])
    df.to_csv(path + date_init.replace("/", ".") + "_" + date_finish.replace("/", ".") + "_" + str(len(links)) + ".csv")


def next_page(driver):
    global visited
    flag = 0

    num_page = None
    pages_div = driver.find_elements_by_id("paginacao")[0]

    links = pages_div.find_elements_by_tag_name("a")

    for link in links:
        try:
            num_page = int(link.text)
            if num_page not in visited:
                link.click()
                visited.append(num_page)

                return num_page
        except:
            pass
    return None


def merge_database(path_links):
    dfs = []

    for link in tqdm.tqdm(path_links):
        df = pd.read_csv(link, index_col=0)
        dfs.append(df)

    df_final = pd.concat(dfs, ignore_index=True)

    print(df_final.describe())
    df_final.drop_duplicates(subset="url", inplace=True)
    print(df_final.describe())

    tokens = path_links[0].split("/")

    final_path = "/".join(tokens[:-1]) + "/final_links.csv"

    df_final.to_csv(final_path)


def web_crawl_tj_sc(dt_init, dt_finish):
    global visited
    global total_count

    visited = [1]
    has_page = 1

    links_ac = []
    links_mn = []

    # Selenium driver
    driver = webdriver.Firefox()
    driver.minimize_window()
    try:
        driver.get("http://busca.tjsc.jus.br/jurisprudencia/#formulario_ancora")
        print("Filling dates")
        driver.find_element_by_xpath(X_PATH_TJ_DT_INIT).send_keys(dt_init)
        driver.find_element_by_xpath(X_PATH_TJ_DT_FINISH).send_keys(dt_finish)

        print("Marking Checkboxes")
        driver.find_element_by_xpath(X_PATH_TJ_CHECK_INTEIRO_TEOR).click()

        select = Select(driver.find_element_by_xpath(X_PATH_CBOX_NUM_RES))
        select.select_by_visible_text('50')

        # driver.find_element_by_xpath(X_PATH_TJ_CHECK_DESPACHO_VP).click()
        driver.find_element_by_xpath(X_PATH_TJ_CHECK_AC_CONSELHO).click()
        driver.find_element_by_xpath(X_PATH_TJ_CHECK_AC_TURMAS_REC).click()

        driver.find_element_by_xpath(X_PATH_TJ_CHECK_MC_TJ).click()
        driver.find_element_by_xpath(X_PATH_TJ_CHECK_MC_REC).click()

        time.sleep(1)
        print("Searching")
        driver.find_element_by_xpath(X_PATH_TJ_BT_SEARCH).click()

        while has_page:
            time.sleep(1)

            if random.random() < 0.005:
                print("\tSleeping")
                time.sleep(60)
            try:
                results_list = driver.find_elements(
                    By.CLASS_NAME, "resultados")

                for result in results_list:
                    a_childrens = result.find_element_by_tag_name('a')

                    link = a_childrens.get_attribute('href')

                    if link.find("tipo=acordao") != -1:
                        links_ac.append(link)
                    else:
                        links_mn.append(link)

                    total_count += 1

                if len(links_ac) > 0:
                    save_links(PATH_TJ_FILES_AC + "links/", links_ac, dt_init, dt_finish)
                if len(links_mn) > 0:
                    save_links(PATH_TJ_FILES_MN + "links/", links_mn, dt_init, dt_finish)

                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "\tPagina:\t", has_page + 1,
                      "\tFiles till now:\t", len(links_ac), "\t", len(links_mn), "\t", len(links_ac) + len(links_mn),
                      "\t", total_count)
            except Exception as e:
                print("\tErro ao processar página:\n\n", e)

            has_page = next_page(driver)
        print("Finishing")
    except Exception as e:
        print(e)
    driver.close()


def crawler():
    intervals = []
    inter_count = 5000

    date_fin = datetime.date(2013, 10, 1)

    for i in range(inter_count):
        date_in = date_fin + datetime.timedelta(days=-7)

        intervals.append([date_in, date_fin])
        date_fin = date_in + datetime.timedelta(days=-1)

    for interval in intervals:
        date_in = str(interval[0].day).zfill(2) + "/" + str(interval[0].month).zfill(2) + "/" + str(interval[0].year)
        date_fin = str(interval[1].day).zfill(2) + "/" + str(interval[1].month).zfill(2) + "/" + str(interval[1].year)

        print("-----------------------------------------------------------------")
        print("INTERVAL: [", date_in, " -> ", date_fin, "]")

        web_crawl_tj_sc(date_in, date_fin)


def split_databases():
    print("Split database")
    paths = [
        "data/tj_sc/acordaos/links/final_links.csv",
        "data/tj_sc/monocratica/links/final_links.csv"
    ]

    for file_path in paths:
        df = pd.read_csv(file_path, index_col=0)

        arrays = np.array_split(df["url"], 16)

        for i in tqdm.tqdm(range(len(arrays))):
            df_split = pd.DataFrame(arrays[i], columns=["url"])

            tmp_path = file_path.replace("final_links.csv", "split_links_" + str(i + 1) + ".csv")
            df_split.to_csv(tmp_path)


def replace_first_line():
    """
    Insert a header line into link files
    :return:
    """
    print("Replace fist line")
    files = glob.glob("data/tj_sc/acordaos/links/*.csv")
    files2 = glob.glob("data/tj_sc/monocratica/links/*.csv")

    for file_path in tqdm.tqdm(files):
        with open(file_path) as f:
            lines = f.readlines()
            lines[0] = ",url\n"

        with open(file_path, "w") as f:
            f.writelines(lines)
    for file_path in tqdm.tqdm(files2):
        with open(file_path) as f:
            lines = f.readlines()
            lines[0] = ",url\n"

        with open(file_path, "w") as f:
            f.writelines(lines)


def download_thread(data):
    th_id, path = data

    df = pd.read_csv(path, index_col=0)
    len_df = len(df)

    tokens = path.split("/")
    base_path = "/".join(tokens[:-2]) + "/cases/"

    for i in range(len_df):
        for j in range(5):
            try:
                time.sleep(random.random() * 5 + 1)
                url = df["url"].iloc[i]

                wget.download(url, base_path)

                print("Thread", th_id, ":\t ", str(i + 1), " of ", len_df)
                break
            except Exception as e:
                print("Thread ", th_id, " Exception: ", e)
                time.sleep(30)


def download(files):
    print("Download TJ-SC fiels")

    s = [[i, files[i]] for i in range(len(files))]

    pool = Pool(len(files))
    results = pool.map(download_thread, s)
    pool.close()
    pool.join()


def fix_rtf_encoding(paths):
    print("Fixing enconding in RTF files")
    for path in paths:
        with open(path, encoding="windows-1252", errors="ignore") as f:
            content = f.read()

        result = content.encode("windows-1252").decode("windows-1252")

        with open(path, mode="w") as f:
            f.write(result)


def split_files_in_folder(paths):
    splits = np.array_split(paths, 20)

    for i in range(len(splits)):
        curr_split = splits[i]

        curr_path = curr_split[0]
        tokens = curr_path.split("/")[:-1]
        new_folder = "/".join(tokens) + "/split_" + str(i + 1)
        os.mkdir(new_folder)

        print("Moving to folder :", new_folder)
        for j in tqdm.tqdm(range(len(curr_split))):
            file_path = curr_split[j]
            shutil.move(file_path, new_folder + "/")


def remove_rtf_pdf_files():
    # path = "/media/trdp/Arquivos/Studies/Msc/Thesis/Experiments/Datasets/law_embeddings_database/tj_sc/cases/"
    path = "/home/egov/Documentos/Experiments/Datasets/law_embeddings_database/tj_sc/acordaos/cases/"
    for dirName, subdirList, fileList in os.walk(path):
        print('Found directory: %s' % dirName)

        for fname in fileList:
            file_path = os.path.join(dirName, fname)
            if fname.find(".rtf") != -1 or fname.find(".pdf") != -1:
                os.remove(file_path)

            print('\t%s' % fname)


def extract_pdf_text(paths):
    for file in tqdm.tqdm(paths):
        pass


def extract_rtf_text(paths):
    print("Extract text from rtf")
    for file in tqdm.tqdm(paths):
        try:
            with open(file, "r", encoding="windows-1252", errors="ignore") as f:
                text = f.read()

            text = file_utils.strip_rtf(text)
            dest_file = file.replace(".rtf", ".txt")
            with open(dest_file, "w+", encoding="windows-1252", errors="ignore") as f:
                f.write(text)
        except:
            pass


def download_files_tj_sc():
    paths = glob.glob("data/tj_sc/acordaos/links/*.csv")
    merge_database(paths)
    paths = glob.glob("data/tj_sc/monocratica/links/*.csv")
    merge_database(paths)
    replace_first_line()
    split_databases()

    download(glob.glob("data/tj_sc/acordaos/links/split*.csv"))
    download(glob.glob("data/tj_sc/monocratica/links/split*.csv"))
