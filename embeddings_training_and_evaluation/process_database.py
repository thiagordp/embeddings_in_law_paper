"""

@author Thiago R. Dal Pont
"""
from pre_processing.text_preprocessing import check_database, clean_text, remove_stopwords, split_by_context, \
    split_by_size
from utils.constants import *

if __name__ == "__main__":
    print("Process database")

    # check_database(FULL_BASE_PATH)
    # clean_text(FULL_BASE_PATH)
    # check_database(FULL_BASE_PATH.replace(".txt", "_cleaned.txt"))
    # remove_stopwords(FULL_BASE_PATH.replace(".txt", "_cleaned.txt"))

    # print("Cleaning alternate texts")
    # clean_text(PATH_CONSUMER_BOOK)
    # clean_text(PATH_CONSUMER_BOOK_2)
    # clean_text(PATH_VADE_MECUM)

    # split_by_context()

    ##########################
    # Database split by size #
    ##########################
    bases = [
        # FULL_BASE_PATH,
        # CONSUMER_BASE_PATH,
        AIR_BASE_PATH
    ]

    for i in range(3):
        split_by_size(EMBEDDINGS_DATABASE_LEN, bases[i], EMBEDDINGS_CONTEXT_BASE[i])
