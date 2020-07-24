"""

@author Thiago
"""
import fitz
import tqdm


def check_line_length(text):
    tokens = text.split("\n")

    sum_len = 0
    for token in tokens:
        sum_len += len(token)

    if len(tokens) == 0:
        return 0

    return sum_len / len(tokens)


def extract_text_from_files(list_files):

    print("Extract text from PDF")
    for file in tqdm.tqdm(list_files):
        # print("File: ", file)
        doc = fitz.open(file)
        text = ""

        for page in doc:
            text += page.getText().replace("  ", " ")

        len_line = check_line_length(text)

        if len_line < 2:
            text = text.replace("\n", "")

        text = text.replace("\n", " ").replace("  ", " ")
        dest_file = file.replace(".pdf", ".txt")
        with open(dest_file, "w+") as f:
            f.write(text)

    return None
