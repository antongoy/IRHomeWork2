# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
import base64
import pickle


from compress import *


def parse_arguments():
    compression_method = sys.argv[1]
    raw_inverted_index_filename = sys.argv[2]
    output_clean_inverted_index = sys.argv[3]
    output_dictionary_filename = sys.argv[4]

    if compression_method == 'varbyte':
        return varbyte_uncompress, \
               raw_inverted_index_filename, \
               output_clean_inverted_index, \
               output_dictionary_filename
    elif compression_method == 'simple9':
        return simple9_uncompress, \
               raw_inverted_index_filename, \
               output_clean_inverted_index, \
               output_dictionary_filename
    else:
        raise AttributeError("Wrong compression method")


def main():
    uncompress, \
    raw_inverted_index_filename, \
    output_clean_inverted_index, \
    output_dictionary_filename = parse_arguments()

    dictionary = {}

    with open(raw_inverted_index_filename, 'r') as raw_inverted_index_file, \
         open(output_clean_inverted_index, 'wb') as inverted_index_file:

        for i, line in enumerate(raw_inverted_index_file):
            term, posting_list = line.strip().split('\t')

            frequency = len(uncompress(base64.b64decode(posting_list)))
            offset = inverted_index_file.tell()
            length = len(posting_list)

            dictionary[term] = (frequency, offset, length)

            inverted_index_file.write(posting_list)

    with open(output_dictionary_filename, 'wb') as dictionary_file:
        pickle.dump(dictionary, dictionary_file, 2)



if __name__ == '__main__':
    main()