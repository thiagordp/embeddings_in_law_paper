"""

@author Thiago Raulino Dal Pont
"""
import time

from embeddings.glove_embeddings import generate_glove
from embeddings.train_embeddings import train_embeddings
from utils.constants import *

if __name__ == "__main__":
    print("TRAINING")

    # EMBEDDINGS_DATABASE_LEN.reverse()

    for context_level in EMBEDDINGS_CONTEXT_BASE:
        for embedding_len in EMBEDDINGS_SIZES:
            for database_size in EMBEDDINGS_DATABASE_LEN:

                if (context_level.find("air_transport") != -1 and database_size > 100 * MILLION_MULT) or \
                        (context_level.find("general") == -1 and database_size > 1 * BILLION_MULT):
                    continue

                for alg in EMBEDDINGS_ALGS:
                    train_embeddings(alg, context_level, database_size, embedding_len)
