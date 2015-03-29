#!/bin/bash

SAMPLE=$1
INPUT="./lenta.ru/$SAMPLE/docs*.txt"
METHOD=$2

cat ${INPUT} | ./mapper.py | sort -s -k1,1 | python reducer.py ${METHOD} > "../raw_inverted_index.txt"
python  build_dictionary.py ${METHOD}