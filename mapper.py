#!/usr/bin/env python
from __future__ import print_function

import re
import sys

from base64 import b64decode
from zlib import decompress

__author__ = 'anton-goy'


def html_to_text(data):
    # remove the newlines
    data = data.replace("\n", " ")
    data = data.replace("\r", " ")

    # replace consecutive spaces into a single one
    data = " ".join(data.split())

    # get only the body content
    bodyPat = re.compile(r'<body[^<>]*?>(.*?)</body>', re.I)
    result = re.findall(bodyPat, data)
    data = result[0]

    # now remove the java script
    p = re.compile(r'<script[^<>]*?>.*?</script>')
    data = p.sub('', data)

    # remove the css styles
    p = re.compile(r'<style[^<>]*?>.*?</style>')
    data = p.sub('', data)

    # remove html comments
    p = re.compile(r'')
    data = p.sub('', data)

    # remove all the tags
    p = re.compile(r'<[^<]*?>')
    data = p.sub('', data)

    p = re.compile(r'&[^;]+;')
    data = p.sub(' ', data)

    return data


def without_lxml_main():
    split_regexp = re.compile('\w+', re.U)

    for line in sys.stdin:
        doc_id, document = line.strip().split('\t')

        document = unicode(decompress(b64decode(document)), encoding='utf-8')
        document = html_to_text(document)

        words = [word.lower() for word in re.findall(split_regexp, document)]
        print(*[('%s\t%s' % (word, doc_id)).encode('utf-8') for word in words], sep='\n')


def main():
    try:
        from lxml.etree import XPath
        from lxml.html import document_fromstring
        from lxml.html.clean import Cleaner
    except ImportError:
        without_lxml_main()
        return

    split_regexp = re.compile('\w+', re.U)
    cleaner = Cleaner(style=True)

    for line in sys.stdin:
        doc_id, document = line.strip().split('\t')

        document = unicode(decompress(b64decode(document)), encoding='utf-8')
        document = document_fromstring(cleaner.clean_html(document))
        document = ' '.join(XPath('.//text()')(document))

        words = [word.lower() for word in re.findall(split_regexp, document)]
        print(*[('%s\t%s' % (word, doc_id)).encode('utf-8') for word in words], sep='\n')


if __name__ == '__main__':
    main()