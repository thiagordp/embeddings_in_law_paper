"""

@author Thiago Raulino Dal Pont
"""
import datetime
import glob
import os
import time
import random

import pandas as pd
from selenium import webdriver

from multiprocessing.pool import Pool

from utils.constants import *

total_count = 0
visited = [1]

thread_count = 0


def save_links(path, links, date_init, date_finish):
    df = pd.DataFrame(links, columns=["url"])
    df.to_csv(path + date_init.replace("/", ".") + "_" +
              date_finish.replace("/", ".") + "_" + str(len(links)) + ".csv")


def next_page(driver):
    global visited
    flag = 0


def layout_small(driver, path):
    print("Trying Layout Small")
    results_list = driver.find_element_by_xpath("//*[@id=\"listadocumentos\"]")
    documents_links = results_list.find_elements_by_class_name("linkdocumento")

    for doc_link in documents_links:
        print("doc_link")

    time.sleep(30)


def layout_big(driver, path, date_in, date_fin):
    # print("Trying Layout Big")

    th_id = random.randint(0, 100)
    has_page = 1
    cur_page = 0
    total_doc = 0
    first_link = ""

    while has_page:
        # print("Page: ", cur_page + 1, end="\t")
        list_links = driver.find_elements_by_partial_link_text("Íntegra do")

        curr_handle = "None"
        handle_pt1 = "None"
        new_handle = "None"

        for link in list_links:
            try:
                curr_handle = None
                handle_pt1 = None
                new_handle = None

                curr_handle = driver.current_window_handle
                link.click()
                time.sleep(3)
                handle_pt1 = driver.window_handles[-1]
                driver.switch_to.window(handle_pt1)
                driver.minimize_window()
                file_name = ""

                bt1 = None
                bt2 = None

                try:
                    bt1 = driver.find_element_by_xpath(X_PATH_STJ_IT_PT_1)
                except:
                    pass

                try:
                    bt2 = driver.find_element_by_xpath(X_PATH_STJ_IT_PT_12)
                except:
                    pass

                if bt2 is not None:
                    driver.close()
                    driver.switch_to.window(curr_handle)
                    continue

                file_name = bt1.text

                if link == list_links[0]:
                    if first_link == file_name:
                        has_page = 0
                    first_link = file_name

                first_link = file_name
                bt1.click()
                time.sleep(3)
                list_of_files = glob.glob(path + "*.pdf")  # * means all if need specific format then *.csv
                latest_file = max(list_of_files, key=os.path.getctime)
                new_path = path + str(random.randint(0, 1000000000)) + ".pdf"
                # print(latest_file)
                # print(new_path)
                if latest_file.find(".part") == -1:
                    os.rename(latest_file, new_path)

                new_handle = driver.window_handles[-1]
                driver.switch_to.window(new_handle)
                driver.minimize_window()
                time.sleep(3)
                driver.close()
                driver.switch_to.window(handle_pt1)
                driver.close()

                time.sleep(2)

                driver.switch_to.window(curr_handle)

                total_doc += 1

                print("Thread\t", th_id, ":\t", date_in, date_fin, "\t", total_doc)

                new_path = path + str(random.randint(0, 1000000000)) + ".pdf"
                # print(latest_file)
                # print(new_path)
                os.rename(latest_file, new_path)

            except Exception as e:
                pass

        try:
            bt = None
            if cur_page == 1:
                bt = driver.find_element_by_xpath(X_PATH_STJ_BT_NEXT_PAGE_1)
            else:
                bt = driver.find_element_by_xpath(X_PATH_STJ_BT_NEXT_PAGE_2)

            if bt.is_enabled():
                bt.click()
                time.sleep(3)
            else:
                break
        except Exception as e:
            print(e)
            break

        cur_page += 1
        if cur_page > 20:
            break


def discover_layout(driver):
    # print("Discover layout")

    try:
        driver.find_element_by_xpath(X_PATH_STJ_PRINT)
        return 2
    except:
        return 1


def process_page(driver, path, date_in, date_fin):
    global visited
    global total_count

    has_page = 1
    visited = [1]

    layout = discover_layout(driver)

    if layout == 1:
        layout_small(driver, path)
    elif layout == 2:
        layout_big(driver, path, date_in, date_fin)


def web_crawl_stj(arg):
    global visited
    global total_count
    global thread_count

    date_in, date_fi = arg

    links_ac = []
    links_mn = []

    x_paths = {
        "acordao": X_PATH_STJ_BT_AC,
        "dec_mono": X_PATH_STJ_BT_MONO
    }

    download_paths = {
        "acordao": PATH_DOWNLOAD_AC,
        "dec_mono": PATH_DOWNLOAD_MC
    }

    for key in x_paths.keys():
        x_path = x_paths[key]

        # print("Searching for", key)

        download_dir = download_paths[key]

        mime_types = "application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml"

        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.panel.shown", False)
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", download_dir)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
        fp.set_preference("plugin.disable_full_page_plugin_for_types", mime_types)
        fp.set_preference("pdfjs.disabled", True)

        if thread_count <= 20:
            thread_count += 1

            time.sleep(random.random() * 60)
        else:
            time.sleep(random.random() * 10)

        driver = webdriver.Firefox(firefox_profile=fp)
        driver.minimize_window()

        time.sleep(random.random() * 3 + 1)

        try:
            driver.get("https://scon.stj.jus.br/SCON/")
            time.sleep(5)
            # print("Fillings dates")
            driver.find_element_by_xpath(X_PATH_STJ_DT_INIT).send_keys(date_in)
            driver.find_element_by_xpath(X_PATH_STJ_DT_FINISH).send_keys(date_fi)

            driver.find_element_by_xpath(X_PATH_STJ_CHECK_TODAS).click()
            driver.find_element_by_xpath(X_PATH_STJ_BT_SEARCH).click()
            # print("Searching")

            time.sleep(5)

            driver.find_element_by_xpath(x_path).click()

            time.sleep(5)

            process_page(driver, download_dir, date_in, date_fi)

            time.sleep(5)

        except Exception as e:
            print("Error:", e)

        try:
            driver.close()
        except:
            pass

        driver.quit()


def crawler():
    intervals = []
    date_finish = datetime.date(2020, 4, 3)

    for i in range(2000):
        # date_in = datetime.date(date_finish.year - 1, date_finish.month, date_finish.day)
        date_in = date_finish + datetime.timedelta(days=-1)

        str_in = str(date_in.day).zfill(2) + str(date_in.month).zfill(2) + str(date_in.year)
        str_fi = str(date_finish.day).zfill(2) + str(date_finish.month).zfill(2) + str(date_finish.year)

        intervals.append([str_in, str_fi])

        # Update
        date_finish = date_in + datetime.timedelta(days=-1)

    # web_crawl_stj_sc(str_in, str_fi)
    pool = Pool(20)
    results = pool.map(web_crawl_stj, intervals)
    pool.close()
    pool.join()
