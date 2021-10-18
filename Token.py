class Token:
    # Initialize with token, lemma, and part-of-speech
    def __init__(self, token, lemma, pos):
        self.token = token
        self.lemma = lemma
        self.pos   = pos

    def print(self):
        print(self.token, self.lemma, self.pos)
