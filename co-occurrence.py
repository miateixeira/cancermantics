from Token import Token
from Sentence import Sentence
from Corpus import Corpus
from helper import *
import glob
from tqdm import tqdm

#######################################################

def preprocessing(filename):
    f = open(filename, encoding='windows-1252')
    raw_data = f.readlines()
    prev_token = None
    sentence = Sentence(raw_data[0].split('\t')[0])

    for line in raw_data:
        line = line.rstrip().split('\t')
        if len(line) < 2:
            continue
        if '@' in line[1]:
            continue
        if '#' in line[1]:
            continue

        token = Token(line[1], line[2], line[3])
        sentence.add_token(token)

        if prev_token == '.':
            corpus.add_sentence(sentence)
            sentence = Sentence(line[0])

        prev_token = token.lemma

    f.close()

#######################################################

DOMAIN = input("Domain of interest (acad/news)? ")
FILENAME = "coca/wlp/" + DOMAIN + "/wlp_" + DOMAIN + "_*.txt"
all_files = glob.glob(FILENAME)

cooccurrence = {}

for filename in tqdm(all_files):
    print("Processing " + filename + "...")
    corpus = Corpus()
    preprocessing(filename)
    corpus.diagnose()
    cooccurrence = sum_update(cooccurrence, corpus.cooccurrence)

import operator

cooccurrence100 = {k:v for (k,v) in cooccurrence.items() if float(v) >= 100}
cooccurrence100sorted = dict(sorted(cooccurrence100.items(), key=operator.itemgetter(1), reverse=True))

import csv

OUTPUT_FILENAME = "co-occurrence_counts_" + DOMAIN + ".csv"
w = csv.writer(open(OUTPUT_FILENAME, "w"))
for key, val in cooccurrence100sorted.items():
    w.writerow([key, val])

import pprint

pprint.pprint(cooccurrence100sorted, sort_dicts=False)

##############################################################
