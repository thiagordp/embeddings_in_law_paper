"""

@author Thiago
"""
import importlib
import sys
import time

import keras
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.test.utils import datapath, get_tmpfile
from keras import Sequential, metrics, backend
from keras.layers import Embedding, SpatialDropout1D, LSTM, Dense, Bidirectional
from keras_preprocessing.sequence import pad_sequences
from keras_preprocessing.text import Tokenizer
import tensorflow as tf

from evaluation import classifier_evaluation
from evaluation.classifier_evaluation import full_evaluation
from utils.constants import MAX_NUMBER_WORDS, EMBEDDINGS_MAX_LEN_SEQ
from utils.data_utils import split_train_test

import pandas as pd
import numpy as np
import gc
import os
import logging

from utils.training_utils import reset_keras

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # FATAL
logging.getLogger('tensorflow').setLevel(logging.FATAL)


def train_lstm(train_data, test_data, val_data, word_vectors, emb_len):
    backend.clear_session()
    # print("LSTM Training")

    x_train, y_train, x_test, y_test, x_val, y_val = split_train_test(train_data, test_data, val_data)

    tokenizer = Tokenizer(
        num_words=MAX_NUMBER_WORDS,
        filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n\'',
        lower=True
    )

    tokenizer.fit_on_texts(x_train)
    word_index = tokenizer.word_index
    # print('\tFound %s unique tokens.' % len(word_index))

    x_train = tokenizer.texts_to_sequences(x_train)
    x_train = pad_sequences(x_train, maxlen=EMBEDDINGS_MAX_LEN_SEQ)
    x_val = tokenizer.texts_to_sequences(x_val)
    x_val = pad_sequences(x_val, maxlen=EMBEDDINGS_MAX_LEN_SEQ)
    # print('\tShape of data tensor:', x_train.shape)

    y_train = pd.get_dummies(y_train).values
    y_val = pd.get_dummies(y_val).values

    # if embeddings.find("glove") != -1:
    #     glove_file = datapath(embeddings)
    #     embeddings = get_tmpfile("glove2word2vec.txt")
    #     glove2word2vec(glove_file, embeddings)
    #
    # print("Loading embeddings", embeddings)
    # word_vectors = KeyedVectors.load_word2vec_format(embeddings, binary=False)

    vocabulary_size = min(len(word_index) + 1, MAX_NUMBER_WORDS)
    embedding_matrix = np.zeros((vocabulary_size, emb_len))

    vec = np.random.rand(emb_len)
    for word, i in word_index.items():
        if i >= MAX_NUMBER_WORDS:
            continue
        try:
            embedding_vector = word_vectors[word]
            embedding_matrix[i] = embedding_vector
        except KeyError:
            embedding_matrix[i] = vec

    del word_vectors

    model = Sequential()
    model.add(
        Embedding(MAX_NUMBER_WORDS, emb_len, input_length=x_train.shape[1], weights=[embedding_matrix],
                  trainable=False))
    model.add(SpatialDropout1D(0.2))
    model.add(LSTM(200, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(4, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=[metrics.categorical_accuracy])

    epochs = 25
    batch_size = 32
    print("\tTraining...")
    history = model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, verbose=0, validation_data=(x_val, y_val), shuffle=True)
    print("\tEvaluating....")
    sequences_test = tokenizer.texts_to_sequences(x_test)
    x_test = pad_sequences(sequences_test, maxlen=EMBEDDINGS_MAX_LEN_SEQ)
    y_pred = model.predict(x_test)
    y_pred = [np.argmax(y) for y in y_pred]
    print(np.array(y_test))
    print(np.array(y_pred))

    _acc = classifier_evaluation.evaluate_accuracy(y_test, y_pred)
    _f1 = classifier_evaluation.evaluate_f_score(y_test, y_pred)
    _auc_roc = classifier_evaluation.evaluate_roc_auc(y_test, y_pred)
    _precision = classifier_evaluation.evaluate_precision(y_test, y_pred)
    _recall = classifier_evaluation.evaluate_recall(y_test, y_pred)
    classifier_evaluation.full_evaluation(y_test, y_pred)

    del embedding_matrix, embedding_vector, x_train, y_train, x_test, y_test, y_pred, history

    return _acc, _f1, _auc_roc, _precision, _recall
