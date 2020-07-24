"""

"""
import glob

from utils.constants import *
from utils.files_utils import *
from pre_processing import extract_texts_pdf

if __name__ == '__main__':
    # unittest.main()
    print("================================================")
    print("Test extract texts from PDF")

    src_paths = [SRC_PATH_DATA + SRC_PATH_STF,
                 SRC_PATH_DATA + SRC_PATH_STJ,
                 SRC_PATH_DATA + SRC_PATH_TJSC,
                 SRC_PATH_DATA + SRC_PATH_JEC_UFSC,
                 SRC_PATH_DATA + SRC_PATH_OTHERS]
    dest_paths = [DEST_PATH_DATA + DEST_PATH_STF,
                  DEST_PATH_DATA + DEST_PATH_STJ,
                  DEST_PATH_DATA + DEST_PATH_TJSC,
                  DEST_PATH_DATA + DEST_PATH_JEC_UFSC,
                  DEST_PATH_DATA + DEST_PATH_OTHER]

    for i in range(len(src_paths)):
        src_path = src_paths[i]
        dest_path = dest_paths[i]

        print("Search in path:\t", src_path)
        # list_files_in_dir(src_path)

        # Digitalized PDF files
        files = glob.glob(src_path + "*d.pdf")
        for file in files:
            print("Applying OCR in: ", file)
            text = extract_texts_pdf.ocr_pdf_file(file)
            dest_file = dest_path + file.replace(src_path, "").replace(".pdf", ".txt")
            print("\tWriting to file")
            write_to_file(dest_file, text)

        # Remaining PDF files
        remaining_files = glob.glob(src_path + "*.pdf")

        for file in remaining_files:

            # Skip PDFs which OCR was applied
            if file in files:
                continue

            print("Applying Digital Text Extraction in: ", file)
            text = extract_texts_pdf.digital_pdf_file(file)
            dest_file = dest_path + file.replace(src_path, "").replace(".pdf", ".txt")
            print("\tWriting to file")
            write_to_file(dest_file, text)

        # Text Files
        text_files = glob.glob(src_path + "*.txt")

        for text_file in text_files:
            dest_file = dest_path + text_file.replace(src_path, "")
            copy_file(text_file, dest_file)
