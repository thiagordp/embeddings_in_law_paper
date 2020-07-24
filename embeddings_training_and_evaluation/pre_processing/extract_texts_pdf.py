import glob

import pytesseract
import time
import pdftotext
import textract

from PIL import Image
from wand.image import Image as Img

from pre_processing import text_preprocessing
from utils.constants import *
from utils.files_utils import clear_dir, write_to_file

tessdata_dir_config = '--tessdata-dir "/usr/share/tesseract-ocr/4.00/tessdata/"'


def ocr_pdf_file(pdf_path):
    # print("\tConverting to images")

    partitions = pdf_path.split("/")
    n_parts = len(partitions)
    file = partitions[n_parts - 1].replace(".pdf", "")

    img_path = "/".join(partitions[:-1]) + "/"
    dest_path = img_path + file + ".jpg"

    clear_dir(img_path)

    with Img(filename=pdf_path, resolution=300) as img:
        for i, image in enumerate(img.sequence):
            img_id = str(i + 1).zfill(4)
            file_name = dest_path[:-4] + "-" + img_id + '.jpg'
            Img(image).save(filename=file_name)

    # time.sleep(1)
    files = glob.glob(img_path + "*.jpg")

    # print("\tLoading images")

    text = ""
    for file in files:
        # print("\t\tProcessing image: ", file)

        img = Image.open(file)
        img = img.convert('L')
        img.save(file)

        # To Use portuguese language it was necessary to download the trained model in:
        # https://github.com/tesseract-ocr/tessdata_best/blob/master/por.traineddata
        # And move it to /usr/share/tesseract-ocr/4.00/tessdata/
        read = pytesseract.image_to_string(Image.open(file), lang='por', config=tessdata_dir_config)
        text += read + "\n"

    text = text_preprocessing.clear_pdf_rtf(text)

    return text


def digital_pdf_file(pdf_path):
    with open(pdf_path, "rb") as file:
        pdf = pdftotext.PDF(file)

    text = "\n".join(pdf)
    # text = text_preprocessing.clear_pdf_rtf(text)

    final_path = pdf_path.replace(".pdf", ".txt")
    with open(final_path, "w+") as f:
        f.write(text)

    return text

def extract_doc_file(doc_path):
    return textract.process(doc_path)
