from helper import sum_update

class Corpus:
    def __init__(self):
        self.corpus = []
        self.cooccurrence = {}

    def add_sentence(self, sent):
        self.corpus.append(sent)

    def diagnose(self):
        word_count = []
        for sent in self.corpus:
            if sent.diagnose():
                counts = sent.get_counts()
                self.cooccurrence = sum_update(self.cooccurrence, counts)
                word_count.append(sent.get_length())
                # self.cooccurrence.update(counts)
        return word_count

    def printCorpus(self):
        for sent in self.corpus:
            sent.printSentence()

    def sent_count(self):
        print(len(self.corpus))

    def get_pos_tags(self):
        pos_tags =[]
        for sent in self.corpus:
            for token in sent.sentence:
                if token.pos not in pos_tags:
                    pos_tags.append(token.pos)
        print(pos_tags)
