"""
In this file, alls the constants and file paths are defined

@author Thiago R. Dal Pont
"""

# Source Paths
DATASET_BASE_PATH = "/media/trdp/Arquivos/Studies/Msc/Thesis/Experiments/Datasets/law_embeddings_database/"
# DATASET_BASE_PATH = "/media/egov/Acer/Experiments/Datasets/law_embeddings_database/"

# PROJECT_PATH = "/media/trdp/Arquivos/Studies/Msc/Thesis/Experiments/Projects/embeddings-training-using-law-texts/"
PROJECT_PATH = "/media/egov/Acer/Experiments/Projects/embeddings-training-using-law-texts/"

STF_CASES_PATH = [
    DATASET_BASE_PATH + "stf/cases/acordaos/",
    DATASET_BASE_PATH + "stf/cases/monocratica/",
    DATASET_BASE_PATH + "stf/cases/repercussao_geral/"
]

STJ_CASES_PATH = [
    DATASET_BASE_PATH + "stj/cases/acordaos/",
]

TJ_SC_CASES_PATH = [
    DATASET_BASE_PATH + "tj_sc/acordaos/cases/",
    DATASET_BASE_PATH + "tj_sc/monocratica/cases/"
]

OTHERS_PATH = [
    DATASET_BASE_PATH + "others/"
]

# Source Paths
SRC_PATH_DATA = "../../../Datasets/corpus-direito/"
SRC_PATH_STF = "acordaos/STF/"
SRC_PATH_STJ = "acordaos/STJ/"
SRC_PATH_TJSC = "acordaos/TJSC/"
SRC_PATH_OTHERS = "others/"
SRC_PATH_JEC_UFSC = "jec_ufsc/"

# Destiny paths
DEST_PATH_DATA = "../data/"
DEST_PATH_STF = "stf/"
DEST_PATH_STJ = "stj/"
DEST_PATH_TJSC = "tjsc/"
DEST_PATH_OTHER = "other/"
DEST_PATH_FINAL = "final_dataset/"
DEST_PATH_OCR = "ocr_files/"
DEST_PATH_JEC_UFSC = "jec_ufsc/"

# Embeddings Constants
EMBEDDINGS_PATH = "embeddings/"
EMBEDDINGS_LEN = 100
EMBEDDINGS_ITER = 100

FULL_BASE_PATH = DATASET_BASE_PATH + "law_fullbase.txt"
CONSUMER_BASE_PATH = DATASET_BASE_PATH + "consumer_base.txt"
AIR_BASE_PATH = DATASET_BASE_PATH + "air_base.txt"

FULL_BASE_CLEAN_PATH = FULL_BASE_PATH.replace(".txt", "_cleaned.txt")

REMOVE_CHARS_PATH = "utils/remove_chars.csv"

#############################
# CONSUMER ALTERNATIVE DATA #
#############################

PATH_CONSUMER_BOOK = "data/other/direito-consumidor_fabricio-bolzan.txt"
PATH_CONSUMER_BOOK_2 = "data/other/manual-do-direito-do-consumidor.txt"
PATH_VADE_MECUM = "data/other/vade-mecum-27ed.txt"

########################
# EMBEDDINGS CONSTANTS #
########################
EMBEDDINGS_SIZES = [100]
# EMBEDDINGS_SIZES = [50, 100, 300, 600, 1000]
EMBEDDINGS_ALGS = [
    "word2vec_cbow",
    "word2vec_sg",
    "glove",
    # "elmo",
    "fasttext_cbow",
    "fasttext_sg"
]

THOUSANDS_MULT = (10 ** 3)
MILLION_MULT = (10 ** 6)
BILLION_MULT = (10 ** 9)
EMBEDDINGS_DATABASE_LEN = [
    1 * THOUSANDS_MULT,
    10 * THOUSANDS_MULT,
    50 * THOUSANDS_MULT,
    100 * THOUSANDS_MULT,
    200 * THOUSANDS_MULT,
    500 * THOUSANDS_MULT,
    1 * MILLION_MULT,
    5 * MILLION_MULT,
    10 * MILLION_MULT,
    25 * MILLION_MULT,
    100 * MILLION_MULT,
    250 * MILLION_MULT,
    500 * MILLION_MULT,
    750 * MILLION_MULT,
    1 * BILLION_MULT,
    3.5 * BILLION_MULT
]

EMBEDDINGS_CONTEXT_BASE = [
    DATASET_BASE_PATH + "final_dataset/standard/",
    DATASET_BASE_PATH + "final_dataset/general/",
    DATASET_BASE_PATH + "final_dataset/consumer/",
    DATASET_BASE_PATH + "final_dataset/air_transport/",
]

EMBEDDINGS_BASE = [p.replace("final_dataset/", "embeddings/") for p in EMBEDDINGS_CONTEXT_BASE]
# EMBEDDINGS_BASE = [DATASET_BASE_PATH + "embeddings/standard/"]
EMBEDDINGS_MIN_COUNT = 2

EMBEDDINGS_RESULT_FILE = PROJECT_PATH + "results/results_training.csv"

#########################
#    GLOVE CONSTANTS    #
#########################
GLOVE_DIR = "embeddings/glove_data/"
MAKE_CMD = "make -C " + PROJECT_PATH + GLOVE_DIR
MAKE_CLEAN_CMD = "make -C " + PROJECT_PATH + GLOVE_DIR + " clean"
GLOVE_TEMPLATE_SCRIPT = GLOVE_DIR + "train_script.sh"
GLOVE_FINAL_SCRIPT = GLOVE_DIR + "final_script.sh"

########################
# EVALUATION CONSTANTS #
########################
# JEC_DATASET_PATH = "/media/trdp/Arquivos/Studies/Msc/Thesis/Experiments/Datasets/processos_transp_aereo/merge_sem_dispositivo/"
JEC_DATASET_PATH = "/media/egov/Acer/Experiments/Datasets/processos_transp_aereo/merge_sem_dispositivo/"

PATH_LAB_PROC = "procedente/"
PATH_LAB_INPROC = "improcedente/"
PATH_LAB_PARC_PROC = "parcialmente_procedente/"
PATH_LAB_EXT = "extincao/"

JEC_DEST_PATH = "data/"
JEC_FINAL_PATH = "final_dataset/"

PROCEDENTE = 0
IMPROCEDENTE = 1
EXTINCAO = 2
PARCIALMENTE_PROCEDENTE = 3

RESULT_COLUMNS = "context,emb_algorithm,emb_len,corpus_size,no_exp,technique,acc,f1_score,auc,precision,recall"

MAX_NUMBER_WORDS = 10000
EMBEDDINGS_MAX_LEN_SEQ = 400

FONT = {'fontname': 'Adobe Garamond Pro'}

####################
# PORTUGUESE TEXTS #
####################
DATASET_PT_CORPUS_PATH = "/media/trdp/Arquivos/Studies/Msc/Thesis/Experiments/Datasets/portuguese_corpus/"
