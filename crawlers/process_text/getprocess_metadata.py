#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Usando Python 3.7

import os
import platform
import io
import re
# precisa instalar
import jsonlines

ROOT_DIR = "/media/pabloernesto/WorkDisk/Work/BigDBs/Processos/STJ/acordaos"
RESULT_FILE = "../data/metadata/metadados.jsonl"


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def main():
    pattern = re.compile(r"((\d{7})-(\d{2}).(\d{4}).(\d{3}).(\d{4}))")

    print("Python version: {}".format(platform.python_version()))

    files = [{"file_name": os.path.join(path, name)} for path, subdirs, files in os.walk(ROOT_DIR) for name in files if
             name.endswith('.txt')]
    total_files = len(files)
    printProgressBar(0, total_files, prefix='Progress:', suffix='Complete', length=50)
    for index, file_data in enumerate(files):
        # print("({}) - {}".format(index, file_data["file_name"]))
        with io.open(file_data["file_name"], "r", encoding="utf8") as processo:
            text = processo.read()

        result = pattern.search(text)
        if result:
            num_processo = result.group(0)
        else:
            num_processo = None
        files[index]["num_processo"] = num_processo
        printProgressBar(index + 1, total_files, prefix='Progress:', suffix='Complete', length=50)

    with jsonlines.open(os.path.join(ROOT_DIR, RESULT_FILE), mode="w") as metadados:
        metadados.write(files)


if __name__ == "__main__":
    main()
