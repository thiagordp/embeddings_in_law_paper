"""


"""
import pandas as pd

from embeddings import word2vec_embeddings
from utils.constants import *

if __name__ == "__main__":
    path = DEST_PATH_DATA + DEST_PATH_FINAL + "final_dataset.csv"

    dataset_df = pd.read_csv(path, sep=";")
    content = dataset_df["content"].values

    for i in range(len(content)):
        content[i] = content[i].split()

    word2vec_embeddings.generate_word2vec_skipgram(content)
    word2vec_embeddings.generate_word2vec_cbow(content)
