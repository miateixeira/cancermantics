from Corpus import Corpus
from Sentence import Sentence
from Token import Token

def preprocessing(filename, corpus, subdict, target):
    f = open(filename, encoding='windows-1252')
    raw_data = f.readlines()
    prev_token = None
    sentenceID = raw_data[0].split('\t')[0]

    sentence = Sentence(sentenceID)

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
            if int(subdict[sentenceID]) in target:
                corpus.add_sentence(sentence)

            sentence = Sentence(line[0])

        prev_token = token.lemma

    f.close()


