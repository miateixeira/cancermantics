from POStags import POS_TAGS
from helper import sum_update

class Sentence:
    # Initialize with article ID and an empty array
    def __init__(self, idn):
        self.id = idn
        self.sentence = []

    # Append on Token object to the sentence
    def add_token(self, token):
        self.sentence.append(token)

    # Returns true if the sentence is "cancer"ous, false otherwise
    def diagnose(self):
        for token in self.sentence:
            if token.lemma == 'cancer':
                return True
            else:
                continue
        return False

    # Returns a dict with counts for each token in the "cancer"ous sentence
    def get_counts(self):
        counts = {}
        weird_output = ['xx_j', 's', 'm', 'xx_r', 'c', 'h', 'l', 'd', 'k', 't', 'xx_p', 'y', 'g', 'res', 'xx_n', 'b', 'e', 'f', 'li']
        for token in self.sentence:
            if token.pos not in POS_TAGS:
                continue
            if token.lemma == 'cancer':
                continue
            if token.lemma == '':
                continue
            if token.lemma in weird_output:
                continue
            if token.lemma in counts:
                counts[token.lemma] += 1
            else:
                counts[token.lemma] = 1
        return counts

    def print(self):
        print("ARTICLE ID: " + str(self.id))
        for tok in self.sentence:
            tok.print()
