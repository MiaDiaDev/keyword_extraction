import os
from os import walk
import nltk
import treetaggerwrapper
from collections import Counter
from pathlib import Path
from nltk.corpus import stopwords
import math
from operator import itemgetter, attrgetter, methodcaller
import csv
import codecs
from tfidfvalue import TfIdfValue


class LanguageProcessor:
    def __init__(self):
        self.subfolder = "Rohtext"

    # erstellt Liste der .txt-Dateien mit den vollständigen Tests
    def load_filenames(self, dir_name):
        f = []
        for (dirname, dirpath, filenames) in walk(dir_name):
            f.extend(filenames)
            break

        return f

    # liest eine .txt-Datei ein
    def read_file(self, filename):
        path = os.path.join(Path().absolute(), self.subfolder, filename)
        with codecs.open(path, "r", "utf-8-sig") as f:
            document_content = f.read()
            f.close()

        return document_content

    # Erweiterung der deutschen Stopwords-Liste aus NLTK
    def create_stop_words(self):
        stop_words = set(nltk.corpus.stopwords.words("german"))
        custom_stop_words = [
            "dass",
            "«",
            "»",
            "@card@",
            "zu+die",
            "in+die",
            "bei+die",
            "an+die",
            "&",
            "@",
            "@ord@",
        ]
        stop_words.update(custom_stop_words)
        return stop_words

    # Inhaltsanalyse eines Tests
    def process_files(self):
        tagger = treetaggerwrapper.TreeTagger(TAGLANG="de")

        filenames = self.load_filenames(self.subfolder)

        filenames_wordfrequencies = {}
        document_frequency = Counter()
        document_count = len(filenames)

        for filename in filenames:
            text_freq = Counter()
            text = self.read_file(filename)
            stop_words = self.create_stop_words()

            # Tokenisierung in Sätze und Wörter
            sentences = nltk.sent_tokenize(text, language="german")
            sentences_tok = [
                nltk.word_tokenize(sent, language="german") for sent in sentences
            ]

            # Lemmatisierung und POS-Tagging der Wörter
            text_word_count = 0
            for sent in sentences_tok:
                tags = tagger.tag_text(sent, tagonly=True)
                tags = treetaggerwrapper.make_tags(tags)
                for tag in tags:

                    if not tag.pos[0] == "$" and tag.lemma not in stop_words:
                        # Ermittlung der Häufigkeit jeder Wortform sofern diese kein Stopword ist
                        text_freq.update([tag.lemma])
                        # Anzahl aller Wörter eines Tests
                        text_word_count += 1

            # Berechnung der Term Frequency
            tf = 0
            wordfrequency_text = {}
            for word_key in text_freq:
                number = text_freq[word_key]
                tf = number / text_word_count
                # print("TF für ", word_key, " = ",  tf)
                document_frequency.update([word_key])
                wordfrequency_text[word_key] = tf

            filenames_wordfrequencies[filename] = wordfrequency_text

        sorted_tf_idf_list = self.process_frequency_lists(
            document_frequency, filenames_wordfrequencies, document_count
        )

        self.export_csv(sorted_tf_idf_list)

    # liest Tf aus und definiert nach Tf-Idf-Wert sortierte Liste
    def process_frequency_lists(
        self, document_frequency, filenames_wordfrequency, document_count
    ):
        tf_idf_list = []
        for filename_key in filenames_wordfrequency:
            for word_key in filenames_wordfrequency[filename_key]:
                text_dictionary = filenames_wordfrequency[filename_key]
                tf = text_dictionary[word_key]

                frequency = document_frequency[word_key]

                tf_idf = self.tf_idf_calculator(tf, frequency, document_count)
                tf_idf_list.append(TfIdfValue(filename_key, word_key, tf, tf_idf))

        sorted_tf_idf_list = sorted(
            tf_idf_list, key=attrgetter("filename", "tf_idf"), reverse=True
        )
        return sorted_tf_idf_list

    # schreibt die Ergebnistabelle als csv
    def export_csv(self, sorted_tf_idf_list):
        file = open("results.csv", "w")
        separator = ";"
        header = (
            "Dateiname" + separator + "Wort" + separator + "Tf" + separator + "Tf-Idf"
        )
        file.write(header + "\n")

        for entry in sorted_tf_idf_list:
            row = (
                entry.filename
                + separator
                + entry.word
                + separator
                + str(round(entry.tf, 3)).replace(".", ",")
                + separator
                + str(round(entry.tf_idf, 3)).replace(".", ",")
                + "\n"
            )
            file.write(row)

    # berechnet Tf-Idf
    def tf_idf_calculator(self, tf, document_frequency, document_count):
        idf = math.log10(document_count / document_frequency)
        tf_idf = tf * idf
        return tf_idf
