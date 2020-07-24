import json
import os
import sys
import hashlib


def hashfile(path, blocksize=65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()


def findDup(parentFolder):
    # Dups in format {hash:[names]}
    dups = {}
    for dirName, subdirs, fileList in os.walk(parentFolder):
        print('Scanning %s...' % dirName)
        for filename in fileList:
            # Get the path to the file
            path = os.path.join(dirName, filename)
            # Calculate hash
            file_hash = hashfile(path)
            # Add or append the file path
            if file_hash in dups:
                dups[file_hash].append(path)
            else:
                dups[file_hash] = [path]
    return dups


def main():
    # print(json.dumps(, indent=4))
    dict_duplicates = findDup("data/stf_prison_data/splits_copy/")
    count = 0
    for key in dict_duplicates.keys():
        values = dict_duplicates[key]

        if len(values) > 1:
            count += 1
            print(values)

            for i in range(1, len(values)):
                os.remove(values[i])
    print(count)


if __name__ == "__main__":
    main()
