"""

"""
import datetime
import random
import re
import time

import pandas as pd
from bs4 import BeautifulSoup

from utils import make_request
from utils.constants import *

visited = [1]
visited_monocratica = [1]
id_monocratica = []
page_flag = 1
curr_page = 1


def get_curr_page(url):
    try:
        ind_1 = url.find("&pagina=")
        url = url.replace("&pagina=", "")
        ind_2 = url.find("&base=")
        return int(url[ind_1:ind_2])
    except:
        return 0


def get_main_urls(content, base_url):
    print("Getting main links")
    page_soup = BeautifulSoup(content, "lxml")
    body = page_soup.body
    pagina_div = body.find("div", id="pagina")
    container_div = pagina_div.find("div", id="conteiner")
    corpo_div = container_div.find("div", id="corpo")
    conteudo_div = corpo_div.find("div", class_="conteudo")
    table_div = conteudo_div.find("table", class_="resultadoLista")

    links = table_div.find_all("a", class_="linkPagina")

    urls = []
    for link in links:
        url = link.get("href")
        urls.append(base_url + url)

    url_df = pd.DataFrame(urls, columns=["url"])
    url_df.to_csv("main_urls.csv")


def get_next_page(bs, url):
    global visited
    global page_flag

    for i in range(2):
        try:
            body = bs.body
            pagina_div = body.find("div", id="pagina")
            container_div = pagina_div.find("div", id="conteiner")
            corpo_div = container_div.find("div", id="corpo")
            conteudo_div = corpo_div.find("div", class_="conteudo")
            nao_impr_div = conteudo_div.find_all("div", id="divNaoImprimir")
            # table_1_div = nao_impr_div.find_all("table")  # .tbody.tr.td.table.tbody.tr
            # tbody_div = table_1_div.find("tbody")

            nao_impr_div = nao_impr_div[1]
            table1_div = nao_impr_div.find("table", width="99%").tr.td.table.tr
            span_div = table1_div.find_all("td")[1].p.span

            split_data = str(span_div).split("|")

            for s in split_data:
                tokens = s.replace("</a>", "").split()

                page = -1
                for token in tokens:

                    try:
                        page = int(token)
                    except:
                        pass

                if page == -1 and s.find("Próximo") != -1:
                    print("Próximo")
                elif page not in visited:

                    a_div = BeautifulSoup(s, "lxml").body.a
                    _url = a_div.get("href")

                    final_url = BASE_URL_STF_JURISPR + _url
                    ############################################
                    if page_flag == 0:
                        page_flag = 1
                        final_url = re.sub("&pagina=[0-9]+&", "&pagina=9998&", final_url)

                        for k in range(2, 9999):
                            visited.append(k)
                    ############################################

                    visited.append(page)

                    return final_url
        except Exception as e:
            print('\tFailed to get next page: ' + str(e))
            print("\tSleeping")
            time.sleep(120)
            print("\tTrying again")
            content = make_request.get_page(url)
            bs = BeautifulSoup(content.text, "lxml")
        time.sleep(2)

    return None


def process_acordao_repercussao(url=None):
    global visited

    documents_links = []

    next_page = url


    while next_page:
        print("Processing acordao / repercussao URL")  # , next_page)
        result = make_request.get_page(next_page)
        page_soup = BeautifulSoup(result.text, "lxml")
        if len(documents_links) > 50:
            break
        try:
            body_div = page_soup.body
            pagina_div = body_div.find("div", id="pagina")
            container_div = pagina_div.find("div", id="conteiner")
            corpo_div = container_div.find("div", id="corpo")
            conteudo_div = corpo_div.find("div", class_="conteudo")
            impressao_div = conteudo_div.find("div", id="divImpressao")

            print("\tProcessing page:", len(visited))
            for processo_div in impressao_div.find_all("div", class_="abasAcompanhamento"):

                try:
                    abas_div = processo_div.ul

                    for li_div in abas_div.find_all("li"):
                        a_div = li_div.a
                        if a_div.text.find("Inteiro Teor") != -1:
                            complete_link = a_div.get("href")

                            url = BASE_URL_INTEIRO_TEOR + \
                                  complete_link.replace("../", "")
                            url = url.replace("\n", "")
                            documents_links.append([url])
                            # Uncomment lines below if you want to download the document and you navigate through search results
                            #
                            # print("\tDownloading file")
                            # doc = make_request.get_page(url)
                            #
                            # print(url)
                            # file_name = "data/doc" + str(url[-8:]) + ".pdf"
                            # print("\tWriting to", file_name)
                            # i += 1
                            #
                            # with open(file_name, "wb+") as f:
                            #     f.write(doc.content)

                            # time.sleep(2)
                except Exception as e:
                    print("Erro ao processar documento: ", str(e))

            df = pd.DataFrame(data=documents_links, columns=["url"])
            file_name = "data/link_stf_" + str(len(documents_links)) + ".csv"
            df.to_csv(file_name)
        except Exception as e:
            print("Erro ao processar página: ", str(e))

        print("\tGetting next page")
        next_page = get_next_page(page_soup, next_page)
        print("\tLinks till now:", len(documents_links))

    print("\tTotal Links:", len(documents_links))

    df = pd.DataFrame(data=documents_links, columns=["url"])
    print(df.head())
    print(df.describe())

    file_name = "data/link_stf_" + \
                str(random.randint(0, 50)) + "_" + \
                str(int(time.time() % 2 ** 32)) + ".csv"
    df.to_csv(file_name)

    time.sleep(5)


def process_monocratica(url=None):
    global visited_monocratica
    global id_monocratica

    next_page = url

    print("Processing monocratica")

    while next_page:
        time.sleep(10)

        result = make_request.get_page(next_page)
        page_soup = BeautifulSoup(result.text, "lxml")

        try:
            body_div = page_soup.body
            pagina_div = body_div.find("div", id="pagina")
            container_div = pagina_div.find("div", id="conteiner")
            corpo_div = container_div.find("div", id="corpo")
            conteudo_div = corpo_div.find("div", class_="conteudo")
            impressao_div = conteudo_div.find("div", id="divImpressao")

            for aba in impressao_div.find_all("div", class_="abasAcompanhamento"):
                div_processo = aba.find("div", class_="processosJurisprudenciaAcordaos")
                text = div_processo.text.replace("\n\n", "\n").replace("fim do documento", "")

                # Save
                id_file = -1
                while id_file == -1 or id_file in id_monocratica:
                    id_file = random.randint(10000000, 100000000)
                id_monocratica.append(id_file)

                path = "../data/stf/cases/monocratica/"
                path += str(id_file)
                path += ".txt"

                with open(path, "w+") as f:
                    f.write(text)

        except Exception as e:
            print("Erro ao processar pagina:", str(e))

        next_page = get_next_page(page_soup, next_page)
        num_page = get_curr_page(next_page)
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "\tPagina: ", num_page, "\tFiles till now:",
              len(id_monocratica))


def get_process_links():
    # Search keywords:  justiça$ ou julgador$ ou stf ou lei$ ou processo$ ou juiz$ ou tribuna$ ou consumidor$ ou
    #                   constituciona$ ou inconstituciona$ ou recurso$ ou acórdão$ ou repercussão ou réu ou juizad$

    # Get base URL for searching
    # These urls correspond to the first page of search results using the given keywords.
    # Then the crawler will navigate through the following pages to get the links to the files
    urls_df = pd.read_csv("../main_urls.csv", index_col=0)

    for url in urls_df.values:
        # Search for "Acordaos" or "Repercusão Geral"
        if url[0].find("baseAcordaos") != -1 or url[0].find("baseRepercussao"):
            process_acordao_repercussao(url[0])
        # Search for "Decisões Monocráticas"
        if url[0].find("baseMonocraticas") != -1:
            process_monocratica(url[0])
