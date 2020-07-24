"""

@author
"""

# TODO: Descobrir quantas palavras tem na base atual
# TODO: Descobrir quais palavras tem e a ocorrência dela
import glob
import os
import re
import time

import pandas as pd
import tqdm

from pre_processing.text_preprocessing import clear_text, clean_text_ret
from utils.constants import DATASET_PT_CORPUS_PATH


def process_wiki_files():
    print("---------------------------------------------------------------------------------------")
    print("WIKI PROCESS")
    with open(DATASET_PT_CORPUS_PATH + "wikipedia_ptbr/ptwiki.txt", "r") as wiki_file, \
            open(DATASET_PT_CORPUS_PATH + "wikipedia_ptbr/wiki_proc.txt", "w+") as wiki_proc_file:
        count_prev = 0
        count_pos = 0

        for line in tqdm.tqdm(wiki_file):
            if (not line.startswith('<') and not line.startswith('</')) and (not line.endswith(">")) and \
                    len(line.replace("\n", "").split()) >= 1:
                count_prev += len(line.split())
                line = line.replace("Section::::", "").replace("BULLET::::", "").replace("\n\n", "\n")
                line = clear_text(line)
                line = clean_text_ret(line)
                count_pos += len(line.split())

                wiki_proc_file.write(line + "\n")

        print("Prev: ", count_prev)
        print("Pos:  ", count_pos)

    return None


def process_literature_files():
    print("---------------------------------------------------------------------------------------")
    print("BRAZILIAN LITERATURE")
    # walk and merge texts to one file
    count_prev = 0
    count_pos = 0

    lines = list()
    count_files = 0
    count_authors = 0
    for dir_path, dirs, files in os.walk(DATASET_PT_CORPUS_PATH + "corpus-of-brazilian-portuguese-literature/"):
        print(dir_path)
        count_authors += 1
        for filename in tqdm.tqdm([f for f in files if f.endswith(".txt")]):
            file_path = os.path.join(dir_path, filename)
            count_files += 1
            # print(file_path)
            try:
                with open(file_path, "r", encoding="windows-1252") as text_file:
                    line = text_file.read()
                    count_prev += len(line.split())
                    line = clear_text(line)
                    line = clean_text_ret(line)
                    lines.append(line)
                    count_pos += len(line.split())
            except:
                try:
                    with open(file_path, "r", encoding="utf-8") as text_file:
                        line = text_file.read()
                        count_prev += len(line.split())
                        line = clear_text(line)
                        line = clean_text_ret(line)
                        lines.append(line)
                        count_pos += len(line.split())
                except:
                    with open(file_path, "r", errors="ignore") as text_file:
                        line = text_file.read()
                        count_prev += len(line.split())
                        line = clear_text(line)
                        line = clean_text_ret(line)
                        lines.append(line)
                        count_pos += len(line.split())
    print("Writing to output")
    with open(DATASET_PT_CORPUS_PATH + "corpus-of-brazilian-portuguese-literature/literature_proc.txt", "w+") as out_file:
        for line in tqdm.tqdm(lines):
            out_file.write(line + "\n")

    print("Prev:    ", count_prev)
    print("Pos:     ", count_pos)
    print("Authors: ", count_authors)
    print("Files:   ", count_files)


def process_hc():
    print("---------------------------------------------------------------------------------------")
    print("HC")

    hc_df = pd.read_csv(DATASET_PT_CORPUS_PATH + "hc_corpus/hc_corpus.tsv", sep="\t")
    texts = hc_df["content"].values

    count_prev = 0
    count_pos = 0
    count_posts = 0

    with open(DATASET_PT_CORPUS_PATH + "hc_corpus/hc_corpus_proc.txt", "w+") as output_file:
        for line in tqdm.tqdm(texts):
            line = str(line)

            count_prev += len(line.split())
            line = clear_text(line)
            line = clean_text_ret(line)
            splits = line.split()

            line_len = len(splits)
            if line_len >= 25:
                count_posts += 1
                output_file.write(line + "\n")
                count_pos += line_len
    print("Prev: ", str(format(count_prev, ',d')))
    print("Pos:  ", str(format(count_pos, ',d')))
    print("News: ", str(format(count_posts, ',d')))


def process_blog():
    print("---------------------------------------------------------------------------------------")
    print("BLOG POSTS")

    count_prev = 0
    count_pos = 0
    count_posts = 0

    i = 0
    for chunk in pd.read_csv(DATASET_PT_CORPUS_PATH + "blogspot-posts/blogposts.csv", chunksize=10 ** 6):
        i += 1
        with open(DATASET_PT_CORPUS_PATH + "blogspot-posts/blogspot_posts_proc_@.txt".replace("@", str(i).zfill(6)), "w+") as output_file:
            contents = chunk["content"].values
            print("Processing chunk ", i)

            for line in tqdm.tqdm(contents):

                line = str(line)
                splits = line.split()

                if len(splits) < 25:
                    continue

                count_prev += len(line.split())
                line = clear_text(line)
                line = clean_text_ret(line)

                splits = line.split()
                line_len = len(splits)
                if line_len >= 25 and line.find("if gte mso") == -1:
                    count_posts += 1
                    output_file.write(line + "\n")
                    count_pos += line_len

            print("Prev: ", str(format(count_prev, ',d')))
            print("Pos:  ", str(format(count_pos, ',d')))
            print("Posts:", str(format(count_posts, ',d')))


def process_instructions():
    print("---------------------------------------------------------------------------------------")
    print("INSTRUCTIONS")

    count_prev = 0
    count_pos = 0
    count_posts = 0

    files = glob.glob(DATASET_PT_CORPUS_PATH + "human-instructions-portuguese-wikihow/*.ttl")

    for i in range(len(files)):
        f = files[i]

        with open(f) as input_file, \
                open(DATASET_PT_CORPUS_PATH + "human-instructions-portuguese-wikihow/rdf_texts_proc_@.txt".replace("@", str(i + 1).zfill(3)), "w+") as output_file:
            print(f)
            print("Reading file")
            text = input_file.read()

            print("Find patterns")
            lines = re.findall(r'"""(.*?)"""', text)

            print("Processing")
            for line in tqdm.tqdm(lines):
                try:
                    if line.find("Main Steps") != -1 or line.find("Requirements") != -1:
                        continue

                    count_prev += len(line.split())
                    line = clear_text(line)
                    line = clean_text_ret(line)
                    splits = line.split()

                    line_len = len(splits)
                    if line_len >= 10 and line.find("div class") == -1:
                        count_posts += 1
                        output_file.write(line + "\n")
                        count_pos += line_len
                except:
                    pass

        print("Prev: ", str(format(count_prev, ',d')))
        print("Pos:  ", str(format(count_pos, ',d')))
        print("News: ", str(format(count_posts, ',d')))


def process_folha():
    print("---------------------------------------------------------------------------------------")
    print("FOLHA UOL")

    count_prev = 0
    count_pos = 0
    count_posts = 0

    folha_df = pd.read_csv(DATASET_PT_CORPUS_PATH + "news-of-the-site-folhauol/articles.csv")

    texts = folha_df["text"].values

    with open(DATASET_PT_CORPUS_PATH + "news-of-the-site-folhauol/folha_proc.txt", "w+") as output_file:
        for line in tqdm.tqdm(texts):
            line = str(line)

            count_prev += len(line.split())
            line = clear_text(line)
            line = clean_text_ret(line)
            splits = line.split()

            line_len = len(splits)
            if line_len >= 10:
                count_posts += 1
                output_file.write(line + "\n")
                count_pos += line_len

    print("Prev: ", str(format(count_prev, ',d')))
    print("Pos:  ", str(format(count_pos, ',d')))
    print("News: ", str(format(count_posts, ',d')))


def process_old_news():
    print("---------------------------------------------------------------------------------------")
    print("OLD NEWS")
    # with open(DATASET_PT_CORPUS_PATH + "old-newspaper/old-newspaper.tsv") as f, \
    #         open(DATASET_PT_CORPUS_PATH + "old-newspaper/pt_old_news.tsv", "w+") as out:
    #     out.write("language\tnewspaper\tdate\ttext")
    #     for line in tqdm.tqdm(f):
    #         if line[0:25].find("Portuguese") != -1:
    #             out.write(line)

    dataset_df = pd.read_csv(DATASET_PT_CORPUS_PATH + "old-newspapers/pt_old_news.tsv", sep="\t")

    text_values = dataset_df["text"].values
    count_prev = 0
    count_pos = 0
    with open(DATASET_PT_CORPUS_PATH + "old-newspapers/pt_old_news_proc.txt", "w+") as f:
        for line in tqdm.tqdm(text_values):
            count_prev += len(line.split())
            line = clear_text(line)
            line = clean_text_ret(line)

            f.write(line + "\n")

            count_pos += len(line.split())

    print("Prev: ", count_prev)
    print("Pos:  ", count_pos)
