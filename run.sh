#!/bin/bash

#NUMBER_OF_PROCESING_PAGES=$1
SAMPLE=$1
INPUT="./lenta.ru/$SAMPLE/docs-000.txt"

cat ${INPUT} | ./mapper.py | sort | ./reducer.py simple9 > "../raw_inverted_index.txt"
python  build_dictionary.py simple9