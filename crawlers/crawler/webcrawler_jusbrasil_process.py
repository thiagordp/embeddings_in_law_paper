"""

"""
import datetime
import glob
import os
import random
import time
import numpy as np
from multiprocessing import Pool

import tqdm
from selenium import webdriver
from utils.constants import *

visited = [1]


def crawler(driver, arg):
    global visited

    th_id, d1, d2 = arg

    visited = [1]
    has_page = 1

    time.sleep(random.random() * 10)

    data = []

    last_len = -1
    for i in range(10000):

        if last_len == len(data):
            now = datetime.datetime.now()
            print(now.strftime('%Y-%m-%d %H:%M:%S'), "\t", d1, "\t", d2,
                  "\tFinishing...\t\tTotal links: ", len(data), "\t", th_id)
            break

        last_len = len(data)

        try:
            new_url = BASE_URL_JUSBRASIL.replace("@date_from", d1).replace("@date_to", d2)
            new_url += "&p=" + str(i + 1)

            driver.get(new_url)
            # time.sleep(3)

            doc_list = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div[2]/div[2]")

            a_childrens = doc_list.find_elements_by_tag_name("a")

            if len(a_childrens) < 10:
                now = datetime.datetime.now()
                print(now.strftime('%Y-%m-%d %H:%M:%S'), "\t", d1, "\t", d2,
                      "\tEmpty page...\t\tTotal links: ", len(data), "\t", th_id)

                continue

            for a_link in a_childrens:

                try:
                    page = int(a_link.text)
                    break

                except:
                    a = a_link.get_attribute('href')

                    if a.find("https:") != -1:
                        if a.find(BASE_URL_JUSBRASIL[0:50]) == -1:
                            data.append(a)
                    else:
                        break

        except Exception as e:
            print(th_id, e)
            time.sleep(30)

        now = datetime.datetime.now()
        print(now.strftime('%Y-%m-%d %H:%M:%S'), "\t", d1, "\t", d2,
              "\tVisiting page: ", i + 1, "\tTotal links: ", len(data), "\t", th_id)
        write_file(th_id, data, d1, d2)


def write_file(th_id, data, d1, d2):
    if len(data) > 0:
        file_path = "data/misto/links/links_" + d1 + "_" + d2 + ".txt"
        with open(file_path, "w+") as f:
            for link in data:
                f.write(link + "\n")


def get_data_from_page(driver, id, link):
    for i in range(5):
        try:
            driver.get(link)
            # time.sleep(1)
            a_links = driver.find_elements_by_tag_name("a")

            for a in a_links:
                try:
                    if a.text.lower().find("inteiro teor") != -1:
                        # print(a.get_attribute("href"))

                        a.click()
                        time.sleep(1)
                        break
                except Exception as e:
                    print(e)

            # print("Getting Text")
            tag_contents = driver.find_elements_by_class_name("unprintable")

            for tag in tag_contents:
                return tag.text

        except Exception as e:
            print("Error L1", e, link)

            time.sleep(60 * (1 + random.random()))


def thread_get_data(arg):
    driver = webdriver.Firefox()
    driver.minimize_window()

    time.sleep(10 * random.random())

    while True:
        th_id = random.randint(0, 100)
        base_path = "data/misto/cases/split_" + str(th_id)

        if not os.path.exists(base_path):
            os.mkdir(base_path)
            break

    try:
        count = 1
        total = len(arg)

        for link, id in arg:
            perc = round(100 * count / total, 2)
            now = datetime.datetime.now()
            print(now.strftime('%Y-%m-%d %H:%M:%S'), "\tThread\t", th_id, ":\t", perc, "%\t", count, "\tof\t", total)
            text = get_data_from_page(driver, id, link)

            file_name = base_path + "/" + str(id) + ".txt"

            with open(file_name, "w+") as f:
                f.write(text)

            count += 1

    except Exception as e:
        print("Error L2:", e)

    driver.close()
    driver.quit()


def next_id(ids):
    id = random.randint(0, 100000)
    while id in ids:
        id = random.randint(0, 100000)

    return id


def download_documents():
    links = []
    ids = []
    with open("../data/misto/final_links.txt", "r") as file_link:
        print("Getting links")
        for line in tqdm.tqdm(file_link):
            link = line.replace("\n", "").replace("\t", "")

            id = random.randint(0, 100000000)
            while id in ids:
                id = random.randint(0, 100000000)
            ids.append(id)

            links.append([link, id])

    splits = np.array_split(links, 15)

    pool = Pool(15)
    results = pool.map(thread_get_data, splits)
    pool.close()
    pool.join()


def merge_links2():
    list_files = glob.glob("data/misto/links/*.txt")
    count = 0
    for file_path in tqdm.tqdm(list_files):
        with open(file_path) as f:
            for line in f:
                print(line.replace("\n", ""))
                count += 1

    print(count)


def thread_crawl(inters):
    driver = webdriver.Firefox()
    driver.minimize_window()

    for interval in inters:
        crawler(driver, interval)

    driver.close()
    driver.quit()

    x = 0
    while x == 0:
        time.sleep(60)


def merge_links():
    file_paths = []
    data_links = []

    for dirName, subdirList, fileList in os.walk("../data/misto/links"):
        for fname in tqdm.tqdm(fileList):
            file_path = os.path.join(dirName, fname)
            if fname.find(".txt") != -1:
                file_paths.append(file_path)

                with open(file_path, "r") as link_file:
                    for line in link_file:
                        data_links.append(line)

    print(len(data_links))
    data_links = list(set(data_links))
    data_links = [link for link in data_links if link.find("https://www.jusbrasil.com.br/") == -1]

    print(len(data_links))

    with open("../data/misto/final_links.txt", "w+") as f:
        for link in data_links:
            f.write(link.replace("\n", "") + "\n")


def jusbrasil_crawl():
    intervals = []
    t = datetime.date.today()
    date_finish = datetime.date(t.year, t.month, t.day)

    th_ids = []
    for i in range(2000):

        th_id = random.randint(0, 10000000000000000000)
        while th_id in th_ids:
            th_id = random.randint(0, 10000000000000000000)
        th_ids.append(th_id)

        date_in = date_finish + datetime.timedelta(days=-7)

        str_in = str(date_in.year) + "-" + str(date_in.month).zfill(2) + "-" + str(date_in.day).zfill(2)
        str_fin = str(date_finish.year) + "-" + str(date_finish.month).zfill(2) + "-" + str(date_finish.day).zfill(2)

        intervals.append([th_id, str_in, str_fin])
        date_finish = date_in + datetime.timedelta(days=-1)

    splits = np.array_split(intervals, 30)

    # for interval in intervals:
    #    crawler(interval)

    pool = Pool(30)
    results = pool.map(thread_crawl, splits)
    pool.close()
    pool.join()

