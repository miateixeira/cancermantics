import re
import operator
import pprint
import glob
from tqdm import tqdm

DOMAIN = input("Domain of interest (acad/news/mag/web/blog)? ")
FILENAME = "coca/full-text/" + DOMAIN + "/text_" + DOMAIN + "_*.txt"
all_files = glob.glob(FILENAME)

NGRAM_SIZE = int(input("Size of ngram window: "))
stop_words = ['of', 'and', 'the', 'in', 'to', 'for', 'a', 'with',
              'is', 'vol', 'that', 'as', 'on', 'j', 'or', 'from', 'p',
              'by', 'are', 'was', 'res', 's', 'were', 'have', 'be', 'at',
              'has', 'it', 'this', 'not', 'an', 'among', 'their', 'about',
              'had', 'other', 'most', 'such', 'can', 'et', 'who', 'al',
              'more', 'been', 'than', 'we', 'but', 'http', 'also', 'all',
              'between', 'after', 'may', 'including', 'uk', 'which', 'one', 
              'these', 'they', 'no', 'int', 'will', 'some', 'however', 'there',
              'he', 'she', 'i', 'his', 'her', 'when', 'nt', 'cancer']

##############################################################

def preprocessing(filename):
    f = open(filename)
    raw_text = f.readlines()
    clean_text = []

    for line in raw_text:
        # Get rid of paragraph markers and newline
        line = line.replace('<p>', ' ')
        line = line.replace('\n', ' ')

        # Convert to lowercases
        line = line.lower()

        # Replace all non-alphanumeric chars with spaces
        # line = re.sub(r'[^a-zA-Z0-9\'\s]', '', line)
        line = re.sub(r'[^a-zA-Z0-9\s]', '', line)

        # Tokenize, remove empty tokens
        tokens = [token for token in line.split(" ") if token != ""]

        clean_text.append(tokens)

    f.close()
    return clean_text

##############################################################

def update_counts(entry, d, n):
    idxs = entry[0]
    text = entry[1]
    for idx in idxs:
        to_update = text[idx-n+1:idx] + text[idx+1:idx+n]
        for word in to_update:
            if word in stop_words:
                continue

            if word in d:
                d[word] += 1
            else:
                d[word] = 1

##############################################################

ngram_counts = {}

for filename in tqdm(all_files):

    print("Processing " + filename)

    all_text = preprocessing(filename)
    cancer_idxs = [[i for i in range(len(line)) if line[i] == 'cancer'] for line in all_text]
    cancer_text = [(idxs, text) for (idxs, text) in list(zip(cancer_idxs, all_text)) if idxs != []]

    for entry in cancer_text:
        update_counts(entry, ngram_counts, NGRAM_SIZE)

ngram_counts_top50 = {k:v for (k,v) in ngram_counts.items() if float(v) >= 100}
ngram_counts_sorted = dict(sorted(ngram_counts_top50.items(),
                                         key=operator.itemgetter(1),
                                         reverse=True))
pprint.pprint(ngram_counts_sorted, sort_dicts=False)

##############################################################
