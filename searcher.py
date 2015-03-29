#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import sys

from compress import *
from base64 import b64decode
from pickle import load

__author__ = 'anton-goy'


def parse_arguments():
    compression_method = sys.argv[1]

    if compression_method == 'varbyte':
        return varbyte_uncompress, sys.argv[2], sys.argv[3], sys.argv[4]
    elif compression_method == 'simple9':
        return simple9_uncompress, sys.argv[2], sys.argv[3], sys.argv[4]
    else:
        raise AttributeError("Wrong compression method")


def get_posting_list(word):
    global inverted_index_file, uncompress, dictionary

    try:
        offset, length = dictionary[word]
    except KeyError:
        raise KeyError("There is no the word '%s' in dictionary" % word)

    inverted_index_file.seek(offset)

    return from_gaps(uncompress(b64decode(inverted_index_file.read(length))))


def intersect_posting_lists(ordinaries_posting_lists, with_not_posting_lists):
    global n_documents
    doc_ids = list(reduce(lambda x, y: x & y, [set(posting_list) for posting_list in ordinaries_posting_lists]))

    # No results for positive results and there are negative results
    if not doc_ids and with_not_posting_lists:
        doc_ids = range(n_documents)

    for posting_list in with_not_posting_lists:
        for doc_id in doc_ids:
            if doc_id in posting_list:
                doc_ids.remove(doc_id)

    return doc_ids


def main_loop():
    global url_dictionary

    print('Start working...')
    while True:
        print('Enter your query: ', end='')
        line = sys.stdin.readline()

        if line == '':
            print('\nExiting...')
            return

        tokens = [s.strip() for s in line.strip().split('AND')]
        ordinaries = []
        with_not = []

        for token in tokens:
            if token.startswith('NOT'):
                with_not.append(token[4:])
            else:
                ordinaries.append(token)

        try:
            ordinaries_posting_lists = [get_posting_list(word) for word in ordinaries]

            with_not_posting_lists = [get_posting_list(word) for word in with_not]
        except KeyError as e:
            print(e.message)
            continue

        doc_ids = intersect_posting_lists(ordinaries_posting_lists, with_not_posting_lists)

        if not len(doc_ids):
            print('There is no documents for your query...')

        for doc_id in doc_ids:
            print(url_dictionary[doc_id])


def building_dictionaries():
    global file_with_urls, dictionary_file, dictionary, url_dictionary, n_documents

    print('Loading the dictionary from file....')
    dictionary = load(dictionary_file)
    url_dictionary = {}

    print('Make the url dictionary...')
    for line in file_with_urls:
        doc_id, url = line.strip().split('\t')
        doc_id = int(doc_id)
        url_dictionary[doc_id] = url

    n_documents = len(url_dictionary)


if __name__ == '__main__':
    uncompress, inverted_index_filename, dictionary_filename, with_urls_filename = parse_arguments()

    with open(dictionary_filename, 'rb') as dictionary_file, \
         open(inverted_index_filename, 'rb') as inverted_index_file, \
         open(with_urls_filename) as file_with_urls:

        url_dictionary = {}
        dictionary = {}
        n_documents = 0
        building_dictionaries()
        main_loop()
