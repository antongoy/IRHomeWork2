# -*- coding: utf-8 -*-
from __future__ import print_function

import argparse

from compress import *
from base64 import b64decode
from pickle import load

__author__ = 'anton-goy'


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('compression_method', type=str, choices=['varbyte', 'simple9'])

    args = vars(parser.parse_args())
    if args['compression_method'] == 'varbyte':
        return varbyte_uncompress
    else:
        return simple9_uncompress


def main():
    uncompress = parse_arguments()

    with open('../dictionary', 'rb') as dictionary_file, \
         open('../inverted_index', 'r') as inverted_index_file:
        dictionary = load(dictionary_file)
        frequency, offset, length = dictionary[u'антон'.encode('utf-8')]

        inverted_index_file.seek(offset)
        posting_list = from_gaps(uncompress(b64decode(inverted_index_file.read(length))))

        print(posting_list)
if __name__ == '__main__':
    main()
