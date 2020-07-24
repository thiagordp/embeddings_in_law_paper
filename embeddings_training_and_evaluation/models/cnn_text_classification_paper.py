"""

@author Thiago
"""
import sys

from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.test.utils import datapath, get_tmpfile
import keras
from keras import Input, Model, metrics, regularizers, backend
from keras.callbacks import EarlyStopping
from keras.layers import Embedding, Reshape, Conv2D, MaxPooling2D, concatenate, Flatten, Dropout, Dense, Convolution1D, MaxPooling1D, Concatenate
from keras.optimizers import Adam
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from sklearn.model_selection import KFold

import pandas as pd
import numpy as np

from evaluation import classifier_evaluation
from evaluation.classifier_evaluation import full_evaluation
from utils.constants import MAX_NUMBER_WORDS, EMBEDDINGS_MAX_LEN_SEQ
from utils.data_utils import split_train_test
from utils.training_utils import reset_keras

import importlib


def train_cnn(train_data, test_data, val_data, word_vectors, emb_len):
    backend.clear_session()

    x_train, y_train, x_test, y_test, x_val, y_val = split_train_test(train_data, test_data, val_data)

    tokenizer = Tokenizer(num_words=MAX_NUMBER_WORDS, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n\'', lower=True)
    tokenizer.fit_on_texts(x_train)
    word_index = tokenizer.word_index
    # print('Found %s unique tokens.' % len(word_index))

    # Convert train and val to sequence
    sequences_train = tokenizer.texts_to_sequences(x_train)
    x_train = pad_sequences(sequences_train, maxlen=EMBEDDINGS_MAX_LEN_SEQ)

    sequences_val = tokenizer.texts_to_sequences(x_val)
    x_val = pad_sequences(sequences_val, maxlen=EMBEDDINGS_MAX_LEN_SEQ)

    y_train = np.asarray(y_train)
    y_train = to_categorical(y_train)
    y_val = np.asarray(y_val)
    y_val = to_categorical(y_val)

    # print('Shape of X train and X validation tensor:', x_train.shape)
    # print('Shape of label train and validation tensor:', y_train.shape)

    # if embeddings.find("glove") != -1:
    #     glove_file = datapath(embeddings)
    #     embeddings = get_tmpfile("glove2word2vec.txt")
    #     glove2word2vec(glove_file, embeddings)
    #
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
            vec = np.random.rand(emb_len)
            embedding_matrix[i] = vec

    # physical_devices = tf.config.experimental.list_physical_devices("GPU")
    # tf.config.experimental.set_memory_growth(physical_devices[0], True)

    # Define Embedding function using the embedding_matrix
    embedding_layer = Embedding(vocabulary_size, emb_len, weights=[embedding_matrix], trainable=False)

    sequence_length = x_train.shape[1]
    filter_sizes = [2, 3, 4, 5]
    num_filters = 10
    drop = 0.5
    drop2 = 0.8
    hidden_dims = 50

    inputs = Input(shape=(sequence_length,))
    embedding = embedding_layer(inputs)
    reshape = Reshape((sequence_length, emb_len, 1))(embedding)

    z = Dropout(drop)(reshape)

    convs = []
    maxpools = []

    conv_blocks = []
    for sz in filter_sizes:
        conv = Conv2D(num_filters, (sz, emb_len), activation='relu',
                      kernel_regularizer=regularizers.l2(0.01))(reshape)

        maxpool = MaxPooling2D(
            (sequence_length - sz + 1, 1), strides=(1, 1))(conv)

        maxpools.append(maxpool)
        conv_blocks.append(conv)
    merged_tensor = concatenate(maxpools, axis=1)
    flatten = Flatten()(merged_tensor)
    z = Dropout(drop2)(flatten)
    z = Dense(hidden_dims, activation="relu")(z)
    model_output = Dense(4, activation="sigmoid")(z)

    # this creates a model that includes
    model = Model(inputs, model_output)

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=[metrics.categorical_accuracy])

    print("Training...")
    hist_adam = model.fit(x_train, y_train, batch_size=32, epochs=50, verbose=0, validation_data=(x_val, y_val), shuffle=True)

    print("Evaluating....")
    sequences_test = tokenizer.texts_to_sequences(x_test)
    x_test = pad_sequences(sequences_test, maxlen=x_train.shape[1])
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

    return _acc, _f1, _auc_roc, _precision, _recall
