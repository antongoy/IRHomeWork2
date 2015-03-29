#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
import base64

from compress import *

__author__ = 'anton-goy'


def compress_posting_list(posting_list, compression_method):
    posting_list.sort()
    gaps = to_gaps(posting_list)

    return compression_method(gaps)


def main():
    if sys.argv[1] == 'varbyte':
        compression_method = varbyte_compress
    elif sys.argv[1] == 'simple9':
        compression_method = simple9_compress
    else:
        print('Wrong compression method')
        return

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
