#!/bin/bash

SAMPLE=$1
METHOD=$2
INPUT="./lenta.ru/$SAMPLE/docs*.txt"

cat ${INPUT} | ./mapper.py | sort -s -k1,1 | ./reducer.py ${METHOD} > "../raw_inverted_index.txt"

./build_dictionary.py ${METHOD} "../raw_inverted_index.txt" "../inverted_index" "dictionary"