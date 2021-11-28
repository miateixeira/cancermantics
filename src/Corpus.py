from helper import sum_update

class Corpus:
    def __init__(self):
        self.corpus = []
        self.cooccurrence = {}
        self.sent_lens = []
        self.cancer_sent_lens = []
        self.cancer_count = 0
        self.norm_factor = 0

    def add_sentence(self, sent):
        self.corpus.append(sent)
        self.sent_lens.append(sent.get_length())

    def diagnose(self):
        for sent in self.corpus:
            if sent.diagnose():
                counts = sent.get_counts()
                self.cooccurrence = sum_update(self.cooccurrence, counts)

                self.cancer_sent_lens.append(sent.get_length())
                self.norm_factor += sent.get_length()
                self.cancer_count += 1

    def printCorpus(self):
        for sent in self.corpus:
            sent.printSentence()

    def getNumSens(self):
        return len(self.corpus)

    def getSentLens(self):
        return self.sent_lens

    def getCancerSentLens(self):
        return self.cancer_sent_lens

    def getCancerCount(self):
        return self.cancer_count

    def getNormFactor(self):
        return self.norm_factor

    def get_pos_tags(self):
        pos_tags =[]
        for sent in self.corpus:
            for token in sent.sentence:
                if token.pos not in pos_tags:
                    pos_tags.append(token.pos)
        print(pos_tags)
