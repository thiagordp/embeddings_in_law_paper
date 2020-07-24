"""

@author Thiago Dal Pont
"""
import glob
import re

import nltk
import pandas as pd
import tqdm
from nltk.corpus import stopwords

from utils.constants import *
from utils.files_utils import write_dict_to_file


def clear_pdf_rtf(text):
    text = str(text).lower()

    text = text.replace("http://www ", "")

    text = text.replace("\n", " ").replace("\t", "")
    text = re.sub(" +", " ", text, 0)

    return text


def clear_text(text):
    text = str(text)

    text = text.replace("\n", " ").replace("\t", " ")

    url_pattern = r'((http|ftp|https):\/\/)?[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
    text = re.sub(url_pattern, ' ', text)

    chars_df = pd.read_csv(PROJECT_PATH + REMOVE_CHARS_PATH)
    _chars = chars_df["char"].values

    _chars = list(_chars)
    for ch in _chars:
        text = text.replace(ch, " ")

    text = text.replace("http://www ", " ")

    text = re.sub("-+", " ", text)
    text = re.sub("\.+", " ", text)
    text = text.replace("nbsp", " ")

    # Symbols
    for symb in "/,-":
        text = text.replace(symb + " ", " ")

    for symb in "()[]{}!?\"§_“”‘’–'º•|<>$#*@:;":
        text = text.replace(symb, " ")

    for symb in ".§ºª":
        text = text.replace(symb, " ")

    text = text.replace("⁄", "/")

    text = correct_misspellings(text)

    for letter in "bcdfghjklmnpqrstvwxyz":
        text = text.replace(" " + letter + " ", " ")

    for i in range(20):
        text = text.replace("  ", " ")

    return text


def correct_misspellings(text):
    misspellings = {
        " r io ": " rio ",
        "ministrorelator": "ministro relator",
        "im u n izar": "imunizar",
        "fi ceira": "ficeira",
        "igualm ente": "igualmente",
        "m aior": "maior",
        "legitim ação": "legitimação",
        "sentim ento": "sentimento",
        "com plem entar": "complementar",
        " ãû ": " ",
        " ûã ": " ",
        " ù ": " ",
        " ùó ": " ",
        " ûo ": " ",
        " ëù ": " ",
        " ët ": " ",
        " ùi ": " ",
        " üûù ": " ",
        " où ": " ",
        " wû ": " ",
        " ùq ": " ",
        " ëä ": " ",
        " ëé ": " ",
        " ëè ": " ",
        " óë ": " ",
        " íë ": " ",
        "ùnica": "única",
        " ùö ": " ",
        " ãû ": " ",
        " ëù ": " ",
        " ûã ": " ",
        " ùá ": " ",
        " ëú ": " ",
        " û ": " ",
        " ëê ": " ",
        " ù ": " ",
        " óo ": " ",
        " ôo ": " ",
        " öô ": " ",
        " öõ ": " ",
        " õó ": " ",
        " õò ": " ",
        " õõ ": " ",
        " õòï ": " ",
        " öõô ": " ",
        " õôò ": " ",
        " õöõ ": " ",
        " öôóñï": ""
    }

    for key in misspellings:
        text = text.replace(key, misspellings[key])

    return text


def pre_process(text):
    text = str(text)

    # Normalize
    text = text.lower()

    # Stop Words
    tokens = text.split()
    stop_words = set(stopwords.words("portuguese"))
    tokens = [word for word in tokens if word not in stop_words]

    # Stemming
    # stemmer = nltk.stem.RSLPStemmer()
    # text = [stemmer.stem(word) for word in text]

    text = " ".join(tokens)

    return text


def merge_text_files(src_folders, destiny_folder):
    print("Merge text files")

    contents = []

    raw_contents = ""

    for folder in src_folders:
        print("\tGetting Texts from: ", folder)
        file_paths = glob.glob(folder + "*.txt")

        for file_path in file_paths:
            with open(file_path, "r") as file:
                raw_content = file.read()

                # Pré-processing
                clean_text = clear_text(raw_content)
                content = pre_process(clean_text)

                raw_contents += "\n " + content

                src = folder.split("/")[2]
                f = file_path.split("/")[3]
                contents.append([src, f, content])

    vocab = {}
    for sentence in contents:
        text = sentence[2].split()
        for word in text:
            try:
                vocab[word.lower()] += 1
            except KeyError:
                vocab[word.lower()] = 1

    # Create a list of tuples sorted by index 1 i.e. value field
    list_of_tuples = sorted(vocab.items(), key=lambda x: x[1])

    count = 0
    # Iterate over the sorted sequence
    for elem in list_of_tuples:
        print(elem[0], "\t::\t", elem[1])
        count += elem[1]

    print("Vocab size ->", len(vocab))
    print("Count -> ", count)

    final_dataset = pd.DataFrame(columns=["source", "file_name", "content"], data=contents)
    final_dataset.to_csv(destiny_folder + "/final_dataset.csv", encoding="utf-8", sep=";", decimal=",")


def check_database(path):
    # Dicts
    chars_dict = {}
    words_dict = {}

    # Iterate through file.
    with open(path, "r") as f:
        for line in tqdm.tqdm(f):
            tokens = line.lower().split()

            # Count char
            for char in line:
                try:
                    chars_dict[char] += 1
                except:
                    chars_dict[char] = 1

            # Count words
            for token in tokens:
                try:
                    words_dict[token] += 1
                except:
                    words_dict[token] = 1

    write_dict_to_file("chars_dict.csv", chars_dict)
    write_dict_to_file("words_dict.csv", words_dict)


def remove_stopwords(path):
    with open(path, "r") as raw_file, open(path.replace(".txt", "_sw.txt")) as dest_file:
        sw = nltk.corpus.stopwords.words('portuguese')
        for line in tqdm.tqdm(raw_file):
            tokens = [token for token in line.split() if token not in sw]
            text = " ".join(tokens).replace("\n", "")
            dest_file.write(text + "\n")


def clean_text(file_p):
    with open(file_p, "r") as raw_file, open(file_p.replace(".txt", "_cleaned.txt"), "w+") as dest_file:

        for line in tqdm.tqdm(raw_file):

            line = re.sub("[0-9]+/[0-9]+/[0-9]+", " ", line)
            line = re.sub("[0-9]+-[0-9]+-[0-9]+", " ", line)

            for char in _chars:
                line = line.replace(str(char), " ")

            # line = line.replace("SUPREMO TRIBUNAL FEDERAL", " ")
            line = re.sub("Supremo +Tribunal +Federal", " ", line)
            line = line.lower()

            line = re.sub("página +[0-9]+ +de +[0-9]+", "", line)
            line = re.sub("ementa +e +acórdão +inteiro +teor +do +acórdão", " ", line)

            t = line.split()

            r = []
            for token in t:
                try:
                    if _dict_word[token] > 20:
                        r.append(token)
                except:
                    pass

            line = " ".join(r)

            # Remove extra spaces
            dest_file.write(line + "\n")


def clean_text_ret(text):
    text = re.sub("[0-9]+/[0-9]+/[0-9]+", " ", text)
    text = re.sub("[0-9]+-[0-9]+-[0-9]+", " ", text)

    for char in _chars:
        text = text.replace(str(char), " ")

    # line = line.replace("SUPREMO TRIBUNAL FEDERAL", " ")
    # text = re.sub("Supremo +Tribunal +Federal", " ", text)
    text = text.lower()

    text = re.sub("página +[0-9]+ +de +[0-9]+", "", text)
    text = re.sub("ementa +e +acórdão +inteiro +teor +do +acórdão", " ", text)

    for char in "bcdfghjklmqrtvwxyz":
        text = text.replace(" " + char + " ", " ")

    t = text.split()

    r = []
    # for token in t:
    #     try:
    #         if _dict_word[token] > 20:
    #             r.append(token)
    #     except:
    #         pass

    text = " ".join(t)

    return text


def split_by_context():
    print("Split by context")

    with open(CONSUMER_BASE_PATH, "w+") as consumer_file, \
            open(FULL_BASE_CLEAN_PATH, "r") as full_base_file, \
            open(AIR_BASE_PATH, "w+") as air_file:

        ###################################
        # Open full base and filter data. #
        ###################################

        for line in tqdm.tqdm(full_base_file):

            if line.find("direito do consumidor") != -1 or \
                    line.find("consumidor") != -1 or \
                    line.find("relação de consumo") != -1 or \
                    line.find("direito consumidor") != -1 or \
                    line.find("relação consumo") != -1:

                # Write to consumer file
                consumer_file.write(line.replace("\n", "") + "\n")

                if line.find("aéreo") != -1 or \
                        line.find("companhia aérea") != -1:
                    # Write to air transport file
                    air_file.write(line.replace("\n", "") + "\n")

        ######################
        # Consumer law books #
        ######################

        with open(PATH_CONSUMER_BOOK.replace(".txt", "_cleaned.txt")) as c, \
                open(PATH_CONSUMER_BOOK_2.replace(".txt", "_cleaned.txt")) as c2, \
                open(PATH_VADE_MECUM.replace(".txt", "_cleaned.txt")) as v:
            consumer_text = c.read().replace("\n", "")
            consumer_text2 = c2.read().replace("\n", "")
            vade_mecum_text = v.read().replace("\n", "")

        consumer_file.write(consumer_text + "\n")
        consumer_file.write(consumer_text2 + "\n")

    ###############
    # Other texts #
    ###############

    with open(FULL_BASE_CLEAN_PATH, "a") as full_base_file:
        full_base_file.write(vade_mecum_text + "\n")
        full_base_file.write(consumer_text + "\n")
        full_base_file.write(consumer_text2 + "\n")


def split_by_size(emb_data_size, database_path, dest_path):
    print("Split by size:\t", database_path)

    for data_size in emb_data_size:
        print("Data Size:\t", data_size)

        src_name = database_path.split("/")[-1]
        dest_file_path = dest_path + src_name.replace(".txt", "_" + str(data_size) + ".txt")

        with open(database_path, "r") as src_file, open(dest_file_path, "w+") as dest_file:
            count = 0

            for line in tqdm.tqdm(src_file):

                tokens = line.replace("\n", "").split()
                sel_tokens = []
                for token in tokens:
                    if count > data_size:
                        break
                    sel_tokens.append(token)
                    count += 1

                result = " ".join(sel_tokens)

                dest_file.write(result.replace("\n", "") + "\n")

                if count > data_size:
                    break
