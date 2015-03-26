#!/usr/bin/env python
from __future__ import print_function

import sys
import base64
import argparse

from compress import *

__author__ = 'anton-goy'


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('compression_method', type=str, choices=['varbyte', 'simple9'])

    args = vars(parser.parse_args())
    return args['compression_method']


def compress_posting_list(posting_list, compression_method):
    posting_list.sort()
    gaps = to_gaps(posting_list)

    if compression_method == 'varbyte':
        encode_string = varbyte_compress(gaps)
    else:
        encode_string = simple9_compress(gaps)

    return encode_string


def main():

    compression_method = parse_arguments()

    current_word = None
    posting_list = set()

    for line in sys.stdin:
        word, doc_id = line.strip().split('\t')

        doc_id = int(doc_id)

        if not current_word:
            current_word = word

        if current_word != word:
            encode_string = compress_posting_list(list(posting_list), compression_method)

            print(current_word, base64.b64encode(encode_string), sep='\t')

            current_word = word
            posting_list = set()

        posting_list.add(doc_id)


if __name__ == '__main__':
    main()
