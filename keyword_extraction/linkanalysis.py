from glob import glob
import os
from os import walk
from bs4 import BeautifulSoup
import codecs
import io


class LinkAnalysis:
    # Hauptmethode, die den Verarbeitungsprozess der lokalen HTML-Dateien startet
    def process_files(self):
        test_folders = self.get_test_folders("Tests\\*\\")
        for tf in test_folders:
            subpages = self.get_test_html_files(tf)
            document = self.compose_testpage_from_subpages(subpages, tf)
            title = tf.replace("Tests", "Rohtext")
            title = title.rstrip("\\")
            self.save_document(document, title)

    # gibt jeden Unterordner wieder, der einen Test repräsentiert
    def get_test_folders(self, tests_folder):
        print("Suche Unterodner")
        return glob(tests_folder)

    # erhält einen Pfad zu einem Test und gibt Liste an enthalten Dateien/Seiten zurück
    def get_test_html_files(self, test_folder):
        f = []
        for (dirname, dirpath, filenames) in walk(test_folder):
            f.extend(filenames)
            break

        return f

    # setzt aus Unterseiten komplette Testseite zusammen
    def compose_testpage_from_subpages(self, subpages, tf):
        document = ""
        for subpage in subpages:
            sp = codecs.open(os.path.join(tf, subpage), "r", "utf-8-sig")
            subpage_string = self.extract_text_from_html(sp)
            document += subpage_string
            # sp.close()

        return document

    # erhält HTML als String und wird mit BS von Tags und irrelevantem Content befreit
    def extract_text_from_html(self, html_string):
        soup = BeautifulSoup(html_string, "lxml")
        soup.prettify()
        raw_content = soup.find("div", {"class": "article col-xs-12"}).find_all("p")
        content = ""
        for paragraph in raw_content:
            content += paragraph.text
        content = self.clean_text(content)

        return content

    # Leere Zeilen vermeiden
    def clean_text(self, content):
        stream_reader = io.StringIO(content)
        clean_content = ""
        for line in stream_reader.readlines():
            if line != "\n" and line != "":
                clean_content += line

        return clean_content

    # speichert den kompletten Test als Textdatei
    def save_document(self, document, title):
        if not os.path.exists("Rohtext"):
            os.makedirs("Rohtext")
        with codecs.open(title + ".txt", "w", "utf-8-sig") as f:
            f.write(document)
            f.close()
