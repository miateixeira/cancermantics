from Token import Token
from Sentence import Sentence
from Corpus import Corpus
from helper import *
from subgenreDict import createSubgenreDict
import glob
from tqdm import tqdm

#######################################################

DOMAIN = input("Domain of interest (acad/news)? ")

COCA_DIR = "../coca/"
WLP_FILENAME = COCA_DIR + "coca-wlp/" + DOMAIN + "/wlp_" + DOMAIN + "_*.txt"
print(WLP_FILENAME)
all_files = glob.glob(WLP_FILENAME)

# this comes from coca-subgenres.txt
subgenreDict = createSubgenreDict()
medID = "151"

#######################################################

def preprocessing(filename):
    f = open(filename, encoding='windows-1252')
    raw_data = f.readlines()
    prev_token = None
    sentenceID = raw_data[0].split('\t')[0]

    sentence = Sentence(sentenceID)
    # sentence = Sentence(raw_data[0].split('\t')[0])

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
            if DOMAIN == "news":#(DOMAIN == "acad" and sentenceID == medID):
                corpus.add_sentence(sentence)
            if DOMAIN == "acad" and subgenreDict[sentenceID] == medID:
                corpus.add_sentence(sentence)
            # corpus.add_sentence(sentence)
            sentence = Sentence(line[0])

        prev_token = token.lemma

    f.close()

#######################################################

cooccurrence = {}
word_count = 0

for filename in tqdm(all_files):
    print("Processing " + filename + "...")
    corpus = Corpus()
    preprocessing(filename)
    word_count += corpus.diagnose()
    cooccurrence = sum_update(cooccurrence, corpus.cooccurrence)

import operator

cooccurrencenorm = {k:(float(v)/word_count) for (k,v) in cooccurrence.items()}
cooccurrencesorted = dict(sorted(cooccurrence.items(), key=operator.itemgetter(1), reverse=True))
cooccurrencenormsorted = dict(sorted(cooccurrencenorm.items(), key=operator.itemgetter(1), reverse=True))

import csv

OUTPUT_FILENAME = "output/raw_counts_" + DOMAIN + ".csv"
w = csv.writer(open(OUTPUT_FILENAME, "w"))
for key, val in cooccurrencesorted.items():
    w.writerow([key, val])

OUTPUT_FILENAME_NORM = "output/norm_counts_" + DOMAIN + ".csv"
w = csv.writer(open(OUTPUT_FILENAME_NORM, "w"))
for key, val in cooccurrencenormsorted.items():
    w.writerow([key, val])

# import pprint

# pprint.pprint(cooccurrencesorted, sort_dicts=False)

# print("Word count: " + str(word_count))

##############################################################
