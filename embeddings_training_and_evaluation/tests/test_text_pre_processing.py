"""

@author Thiago R. Dal Pont
"""

from utils.constants import *
from pre_processing import text_preprocessing

if __name__ == "__main__":
    print("Testing Pre-processing")

    print("Merge Database")

    src_paths = [DEST_PATH_DATA + DEST_PATH_STF,
                 DEST_PATH_DATA + DEST_PATH_STJ,
                 DEST_PATH_DATA + DEST_PATH_TJSC,
                 DEST_PATH_DATA + DEST_PATH_JEC_UFSC,
                 DEST_PATH_DATA + DEST_PATH_OTHER]
    dest_path = DEST_PATH_DATA + DEST_PATH_FINAL

    text_preprocessing.merge_text_files(src_folders=src_paths, destiny_folder=dest_path)
