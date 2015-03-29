#!/bin/bash

SAMPLE=$1
METHOD=$2

cat ${SAMPLE} | ./mapper.py | sort -s -k1,1 | ./reducer.py ${METHOD} > "../raw_inverted_index.txt"

./build_dictionary.py "../raw_inverted_index.txt" "../inverted_index" "../dictionary"