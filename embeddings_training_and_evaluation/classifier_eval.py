"""

@author Thiago R. Dal Pont
"""

import glob
import random
import time

import pandas as pd
import numpy as np
import tqdm
import datetime

from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.test.utils import datapath, get_tmpfile
from sklearn.model_selection import train_test_split

from models.cnn_text_classification import train_cnn
from models.lstm_text_classification import train_lstm
from pre_processing import text_preprocessing
from utils.constants import *
from utils.files_utils import elapsed_time


def save_data(x_data, y_data, path_data):
    x = pd.DataFrame(data=x_data, columns=["file_name", "content"])
    y = pd.DataFrame(data=y_data, columns=["label"])
    train_set = np.concatenate((x, y), axis=1)
    _train_df = pd.DataFrame(train_set, columns=["file_name", "content", "label"])
    _train_df.to_csv(path_data, encoding="utf-8")


def setup_data():
    # Load "procedentes"
    print("Loading text files...")
    data = []

    dict_classes = {
        PATH_LAB_PROC: PROCEDENTE,
        PATH_LAB_INPROC: IMPROCEDENTE,
        PATH_LAB_EXT: EXTINCAO,
        PATH_LAB_PARC_PROC: PARCIALMENTE_PROCEDENTE
    }

    regression_df = pd.read_csv("data/attributes.csv")
    print(regression_df.describe())

    for path_class in dict_classes.keys():

        folder = JEC_DATASET_PATH + path_class
        file_paths = glob.glob(folder + "*.txt")

        for file_path in file_paths:
            with open(file_path) as f:
                raw_content = f.read()
                file_name = file_path.replace(folder, "").replace(".txt", "")

                found_df = np.array(regression_df.loc[regression_df['sentenca'] == int(file_name)])
                # print(np.array(found_df))

                if len(found_df) == 0:
                    arr = [file_name, raw_content, dict_classes[path_class], 0.0]
                    data.append(arr)
                else:
                    for fdf in found_df:
                        arr = [file_name, raw_content, dict_classes[path_class], float(str(fdf[1]).replace("R$ ", "").replace(".", "").replace(",", "."))]
                        data.append(arr)

    print("Pre-processing...")
    processed_data = []

    for file_name, content, label, valor in tqdm.tqdm(data):
        clean_text = text_preprocessing.clear_text(content)
        processed_text = text_preprocessing.pre_process(clean_text)
        processed_data.append([file_name, processed_text, label, valor])

    df = pd.DataFrame(data=processed_data, columns=["file_name", "content", "label", "indenizacao"])
    df.to_csv(PROJECT_PATH + JEC_DEST_PATH + JEC_FINAL_PATH + "jec_ufsc_dataset.csv")

    print(df.describe())

    x = df[["file_name", "content"]]
    y = df["label"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=(int(time.time()) % 2 ** 32), stratify=y)

    x_test, x_val, y_test, y_val = train_test_split(x_test, y_test, test_size=0.5, random_state=(int(time.time()) % 2 ** 32), stratify=y_test)

    print(x_train.shape, x_test.shape, x_val.shape, y_train.shape, y_test.shape, y_val.shape)

    _path = PROJECT_PATH + JEC_DEST_PATH + JEC_FINAL_PATH + "jec_ufsc_train.csv"
    # save_data(x_train, y_train, _path)

    _path = PROJECT_PATH + JEC_DEST_PATH + JEC_FINAL_PATH + "jec_ufsc_test.csv"
    # save_data(x_test, y_test, _path)

    _path = PROJECT_PATH + JEC_DEST_PATH + JEC_FINAL_PATH + "jec_ufsc_val.csv"
    # save_data(x_val, y_val, _path)


def run_classifier():
    print("Classifier")


def get_embeddings():
    x = 0


def initialize_results_file():
    with open(EMBEDDINGS_RESULT_FILE, "w+") as f:
        f.write(RESULT_COLUMNS + "\n")


def get_data_from_file(context, embeddings):
    _tokens = context.split("/")
    _context_name = _tokens[-2]

    # Get Algorithm
    _file_name = embeddings.split("/")[-1].replace(".txt", "").replace("_str", "")
    _tokens = _file_name.split("_")
    _alg = _tokens[0]

    if _alg == "glove" or _alg == "elmo":
        _corpus_size = int(_tokens[1])
        _emb_len = int(_tokens[2])
    else:
        # Type of algorithm
        _alg += "_" + _tokens[1]
        # Get Corpus Size
        _corpus_size = int(_tokens[2])
        # Get Embeddings Length
        _emb_len = int(_tokens[3])

    return _context_name, _alg, _emb_len, _corpus_size


def save_results(context, embeddings, results_cnn, result_lstm):
    _context_name, _alg, _emb_len, _corpus_size = get_data_from_file(context, embeddings)

    # For each experiment
    data_result = []
    for i in range(len(results_cnn)):
        cnn_acc, cnn_f1_score, cnn_auc_roc, cnn_precision, cnn_recall = cnn_results[i]

        data_result.append(
            [
                _context_name, _alg, _emb_len, _corpus_size, i + 1, "cnn",
                cnn_acc, cnn_f1_score, cnn_auc_roc, cnn_precision, cnn_recall
            ])

    for i in range(len(result_lstm)):
        lstm_acc, lstm_f1_score, lstm_auc_roc, lstm_precision, lstm_recall = lstm_results[i]

        data_result.append(
            [
                _context_name, _alg, _emb_len, _corpus_size, i + 1, "lstm",
                lstm_acc, lstm_f1_score, lstm_auc_roc, lstm_precision, lstm_recall
            ])

    with open(EMBEDDINGS_RESULT_FILE, "a+") as result_f:
        for result in data_result:
            text = ",".join([str(item) for item in result])
            print(text)
            result_f.write(text + "\n")


if __name__ == "__main__":
    print("Classifier eval")

    setup_data()

    # initialize_results_file()
    #
    # # Current context
    # total_time_1 = time.time()
    # for c in EMBEDDINGS_BASE:
    #
    #     print("=======================================================================================================")
    #     print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "\tContext\t", c)
    #
    #     context_path = c + "glove*.txt"
    #     emb_paths = glob.glob(context_path)
    #     # emb_paths.reverse()
    #
    #     time.sleep(1)
    #
    #     # Load train, test data
    #     train_df = pd.read_csv(PROJECT_PATH + JEC_DEST_PATH + JEC_FINAL_PATH + "jec_ufsc_train.csv")
    #     test_df = pd.read_csv(PROJECT_PATH + JEC_DEST_PATH + JEC_FINAL_PATH + "jec_ufsc_test.csv")
    #     val_df = pd.read_csv(PROJECT_PATH + JEC_DEST_PATH + JEC_FINAL_PATH + "jec_ufsc_val.csv")
    #
    #     train_data = train_df
    #     test_data = test_df
    #     val_data = val_df
    #
    #     # Filter embeddings
    #     final_emb = []
    #     for emb_path in emb_paths:
    #         final_emb.append(emb_path)
    #
    #     # random.shuffle(final_emb)
    #
    #     for emb_path in tqdm.tqdm(final_emb):
    #         cnn_results = []
    #         lstm_results = []
    #
    #         _, _, emb_len, _ = get_data_from_file(context_path, emb_path)
    #
    #         print("Loading Embeddings")
    #         if emb_path.find("glove") != -1:
    #             glove_file = datapath(emb_path)
    #             embeddings = get_tmpfile("glove2word2vec.txt")
    #             glove2word2vec(glove_file, embeddings)
    #
    #         word_vectors = KeyedVectors.load_word2vec_format(embeddings, binary=False)
    #
    #         print("=========  CNN TRAINING  ==========")
    #         for i in range(500):
    #             print("################################## EXPERIMENT ", i, " CNN  ##################################")
    #             print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "\t", emb_path)
    #             t1 = time.time()
    #             acc, f1_score, auc_roc, precision, recall = train_cnn(train_data, test_data, val_data, word_vectors, emb_len)
    #             cnn_results.append([acc, f1_score, auc_roc, precision, recall])
    #             t2 = time.time()
    #             elapsed_time(t2 - t1)
    #             time.sleep((t2 - t1) * 0.05)
    #
    #         print("=========  LSTM TRAINING  ==========")
    #         for i in range(0):
    #             print("################################## EXPERIMENT ", i, " LSTM  ##################################")
    #             print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "\t", emb_path)
    #             t1 = time.time()
    #             acc, f1_score, auc_roc, precision, recall = train_lstm(train_data, test_data, val_data, word_vectors, emb_len)
    #             lstm_results.append([acc, f1_score, auc_roc, precision, recall])
    #             t2 = time.time()
    #             elapsed_time(t2 - t1)
    #             time.sleep((t2 - t1) * 0.05)
    #
    #         save_results(c, emb_path, cnn_results, lstm_results)
    # total_time_2 = time.time()
    # print("FINISHED!")
    # elapsed_time(total_time_2 - total_time_1)
