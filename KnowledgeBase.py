class KnowledgeBase:
    def __init__(self):
        self.sentences = []

    def add_sentence(self, sentence_str):
        sentence = sentence_str.split(' OR ')
        self.sentences.append(sentence)
