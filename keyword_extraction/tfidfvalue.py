

# Klasse zum strukturierten Speichern der berechneten Frequenzen
class TfIdfValue:
    def __init__(self, filename, word, tf, tf_idf):
        self.filename = filename
        self.word = word
        self.tf = tf
        self.tf_idf = tf_idf
