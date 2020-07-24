"""
Convert binary files of fasttext trained embeddings to word2vec formatted text files.

@author Thiago
"""

import codecs
import glob

import gensim
import tqdm
from gensim.models import Word2Vec
from utils.constants import EMBEDDINGS_BASE
from gensim.models.wrappers import FastText


def main():
    for embeddings_path in EMBEDDINGS_BASE:
        print(embeddings_path)
        emb_files = glob.glob(embeddings_path + "fasttext*.bin")

        for emb_file in emb_files:
            print("Embedding:\t", emb_file.replace(embeddings_path, ""))
            path_to_model = emb_file
            output_file = emb_file.replace(".bin", ".txt")
            export_to_file(path_to_model, output_file)


def export_to_file(path_to_model, output_file):
    output = codecs.open(output_file, 'w+', 'utf-8')

    print("Converting to text")
    model = FastText.load_fasttext_format(path_to_model)
    vocab = model.wv.vocab
    # output.write(str(len(vocab)) + " " + str(len(model[vocab[0]])))
    header = False
    for mid in tqdm.tqdm(vocab):
        if not header:
            output.write(str(len(vocab)) + " " + str(len(model[mid])) + "\n")
            header = True

        vector = list()
        for dimension in model[mid]:
            vector.append(str(dimension))
        # line = { "mid": mid, "vector": vector  }
        vector_str = " ".join(vector)
        line = mid + " " + vector_str
        # line = json.dumps(line)
        output.write(line + "\n")
    output.close()
    print("Done!")


if __name__ == "__main__":
    main()
