import datetime
import glob
import time
import pandas as pd
import sys

from classifier_eval import get_data_from_file, save_results
from models.cnn_text_classification import train_cnn
from models.lstm_text_classification import train_lstm
from utils.constants import PROJECT_PATH, JEC_DEST_PATH, JEC_FINAL_PATH
from utils.files_utils import elapsed_time

if len(sys.argv) < 3:
    print("Error")
    exit()

context_path = sys.argv[1]
emb_path = sys.argv[2]

print("=======================================================================================================")
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "\tContext\t", context_path)

time.sleep(1)

# Load train, test data

train_df = pd.read_csv(PROJECT_PATH + JEC_DEST_PATH + JEC_FINAL_PATH + "jec_ufsc_train.csv")
test_df = pd.read_csv(PROJECT_PATH + JEC_DEST_PATH + JEC_FINAL_PATH + "jec_ufsc_test.csv")

train_data = train_df
test_data = test_df

cnn_results = []
lstm_results = []

_, _, emb_len, _ = get_data_from_file(context_path, emb_path)

print("=========  CNN TRAINING  ==========")
for i in range(20):
    print("################################## EXPERIMENT ", i, " ##################################")
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "\t", emb_path)
    t1 = time.time()
    acc = f1_score = auc_roc = precision = recall = 0
    acc, f1_score, auc_roc, precision, recall = train_cnn(train_data, test_data, emb_path, emb_len)
    cnn_results.append([acc, f1_score, auc_roc, precision, recall])
    t2 = time.time()
    elapsed_time(t2 - t1)
    time.sleep((t2 - t1) * 0.05)

print("=========  LSTM TRAINING  ==========")
for i in range(20):
    print("################################## EXPERIMENT ", i, " ##################################")
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "\t", emb_path)
    t1 = time.time()
    acc = f1_score = auc_roc = precision = recall = 0
    acc, f1_score, auc_roc, precision, recall = train_lstm(train_data, test_data, emb_path, emb_len)
    lstm_results.append([acc, f1_score, auc_roc, precision, recall])
    t2 = time.time()
    elapsed_time(t2 - t1)
    time.sleep((t2 - t1) * 0.05)

save_results(c, emb_path, cnn_results, lstm_results)
