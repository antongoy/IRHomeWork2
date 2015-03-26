#!/bin/bash

#NUMBER_OF_PROCESING_PAGES=$1
SAMPLE=$1
INPUT="./zr.ru/$SAMPLE/docs-000.txt"

cat ${INPUT} | ./mapper.py | sort | ./reducer.py varbyte > "../inverted_index.txt"
