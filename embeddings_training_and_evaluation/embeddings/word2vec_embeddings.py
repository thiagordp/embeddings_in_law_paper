"""

@author Thiago
"""

from gensim.models import Word2Vec


from utils.constants import *
from utils.embeddings_utils import visualize_embeddings
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def generate_word2vec_skipgram(data_file, train_iter, emb_size, output_file):
    # print("Training Word Embeddings w/ Word2Vec Skipgram")
    model = Word2Vec(
        corpus_file=data_file,
        size=emb_size,
        workers=8,
        sg=1,
        min_count=EMBEDDINGS_MIN_COUNT)

    model.wv.save_word2vec_format(output_file, binary=False)

    try:
        result = model.most_similar("processo", topn=20)
        print(result)
        result = model.most_similar("procedente", topn=20)
        print(result)
    except:
        pass


def generate_word2vec_cbow(data_file, train_iter, emb_size, output_file):
    # print("Training Word Embeddings w/ Word2Vec C-BOW")
    model = Word2Vec(
        corpus_file=data_file,
        size=emb_size,
        workers=8,
        sg=0,
        min_count=EMBEDDINGS_MIN_COUNT)

    model.wv.save_word2vec_format(output_file, binary=False)

    try:
        result = model.most_similar("processo", topn=20)
        print(result)
        result = model.most_similar("procedente", topn=20)
        print(result)
    except:
        pass
