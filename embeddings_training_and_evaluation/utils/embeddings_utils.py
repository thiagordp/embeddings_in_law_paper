"""

@author Thiago
"""
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.test.utils import datapath, get_tmpfile
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt
plt.rcParams['font.family'] = 'serif'
plt.rc('xtick', labelsize=16)
plt.rc('ytick', labelsize=16)

def visualize_embeddings(model):
    """
    Visualize Embeddings vocabulary in two dimensions with PCA.

    :param model: Trained Model
    :return: None
    """

    x = model[model.wv.vocab]

    print("PCA")
    pca = PCA(n_components=2)
    result = pca.fit_transform(x)
    print("PLot")
    plt.figure(figsize=(9, 6), dpi=300)
    plt.scatter(result[:400, 0], result[:200, 1])
    words = list(model.wv.vocab)

    x = 0
    for i, word in enumerate(words):
        x += 1

        if x >= 400:
            break
        plt.annotate(word, xy=(result[i, 0], result[i, 1]))
    plt.tight_layout()
    plt.savefig("projection.pdf")
    plt.show()


def main():
    print("")
    glove_file = datapath("/media/trdp/Arquivos/Studies/Msc/Thesis/Experiments/Datasets/law_embeddings_database/embeddings/general/glove_1000000000_100.txt")
    embeddings = get_tmpfile("glove2word2vec.txt")
    glove2word2vec(glove_file, embeddings)

    word_vectors = KeyedVectors.load_word2vec_format(embeddings, binary=False)
    visualize_embeddings(word_vectors)


if __name__ == "__main__":
    main()
