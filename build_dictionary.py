from __future__ import print_function

import sys
import base64
import pickle
import argparse

from compress import *


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('compression_method', type=str, choices=['varbyte', 'simple9'])

    args = vars(parser.parse_args())
    return args['compression_method']


def main():
    compression_method = parse_arguments()

    if compression_method == 'varbyte':
        compress = varbyte_compress
        uncompress = varbyte_uncompress
    else:
        compress = simple9_compress
        uncompress = simple9_uncompress

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