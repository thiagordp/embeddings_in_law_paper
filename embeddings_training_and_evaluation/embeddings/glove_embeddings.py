"""

"""
import os
from utils.constants import MAKE_CLEAN_CMD, MAKE_CMD, GLOVE_TEMPLATE_SCRIPT, PROJECT_PATH, GLOVE_DIR, GLOVE_FINAL_SCRIPT


def setup_glove():
    # Make clean
    os.system(MAKE_CLEAN_CMD)
    # Make
    os.system(MAKE_CMD)


def generate_glove(data_file, train_iter, emb_size, output_file):
    setup_glove()

    text = ""
    # Edit train script
    with open(GLOVE_TEMPLATE_SCRIPT, "r") as template_file:
        text = template_file.read()

    text = text.replace("@file_name", data_file)
    text = text.replace("@output_file", output_file)
    text = text.replace("@emb_size", str(emb_size))
    text = text.replace("@emb_iter", str(train_iter))
    text = text.replace("@make_cmd", MAKE_CMD)
    text = text.replace("@make_dir", GLOVE_DIR)

    with open(GLOVE_FINAL_SCRIPT, "w+") as out_file:
        out_file.write(text)

    os.system("chmod +x " + GLOVE_FINAL_SCRIPT)
    os.system("./" + GLOVE_FINAL_SCRIPT)
