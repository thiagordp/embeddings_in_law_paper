"""
@author Thiago Raulino Dal Pont
"""
import datetime
import glob
import time

import tqdm

from embeddings.fasttext_embeddings import generate_fasttext_cbow, generate_fasttext_skipgram
from embeddings.glove_embeddings import generate_glove
from embeddings.word2vec_embeddings import generate_word2vec_cbow, generate_word2vec_skipgram
from utils.constants import *
from utils.files_utils import elapsed_time

dict_alg = {
    "word2vec_cbow": generate_word2vec_cbow,
    "word2vec_sg": generate_word2vec_skipgram,
    "glove": generate_glove,
    "fasttext_cbow": generate_fasttext_cbow,
    "fasttext_sg": generate_fasttext_skipgram
}


def train_embeddings(algorithm, context_level, database_size, embeddings_len):
    t1 = time.time()

    print("===========================================================================================================")
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "\tTrain: ", algorithm, context_level, database_size,
          embeddings_len)

    # Load database
    database = glob.glob(context_level + "*_" + str(database_size) + ".txt")

    if len(database) == 0:
        print("Database not found")

        return None

    # Select algorithm
    alg_func = dict_alg[algorithm]

    # Run algorithm
    file_name = context_level.replace("final_dataset/", "embeddings/") + algorithm + "_" + str(
        database_size) + "_" + str(embeddings_len) + ".txt"

    alg_func(database[0], EMBEDDINGS_ITER, embeddings_len, file_name)

    t2 = time.time()
    td = t2 - t1
    elapsed_time(td)

    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "\tSleeping for ", round(td * 0.05, 1), "seconds")
    time.sleep(td * 0.05)
