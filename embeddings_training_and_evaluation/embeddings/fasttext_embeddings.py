"""
Fast Text Embeddings Training
@author Thiago Raulino Dal Pont
"""

import fasttext

from embeddings import fasttext_to_text


def generate_fasttext_cbow(data_file, train_iter, emb_size, output_file):
    model = fasttext.train_unsupervised(input=data_file, model='cbow', dim=emb_size, minCount=5, verbose=2, thread=8)
    model_output = output_file.replace(".txt", ".bin")
    text_output = output_file
    model.save_model(model_output)
    fasttext_to_text.export_to_file(model_output, text_output)


def generate_fasttext_skipgram(data_file, train_iter, emb_size, output_file):
    model = fasttext.train_unsupervised(input=data_file, model='skipgram', dim=emb_size, minCount=5, verbose=2,
                                        thread=8)
    model_output = output_file.replace(".txt", ".bin")
    text_output = output_file
    model.save_model(model_output)
    fasttext_to_text.export_to_file(model_output, text_output)
