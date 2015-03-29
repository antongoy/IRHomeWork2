# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
import base64
import pickle


from compress import *


def parse_arguments():
    compression_method = sys.argv[1]
    return compression_method


def main():
    compression_method = parse_arguments()

    if compression_method == 'varbyte':
        uncompress = varbyte_uncompress
    elif compression_method == 'simple9':
        uncompress = simple9_uncompress
    else:
        raise AttributeError("Wrong compression method")

    dictionary = {}

    with open('../raw_inverted_index.txt', 'r') as raw_inverted_index_file, \
         open('../inverted_index', 'wb') as inverted_index_file:
        for i, line in enumerate(raw_inverted_index_file):
            term, posting_list = line.strip().split('\t')

            frequency = len(uncompress(base64.b64decode(posting_list)))
            offset = inverted_index_file.tell()
            length = len(posting_list)

            dictionary[term] = (frequency, offset, length)

            inverted_index_file.write(posting_list)

    with open('../dictionary', 'wb') as dictionary_file:
        pickle.dump(dictionary, dictionary_file, 2)



if __name__ == '__main__':
    main()