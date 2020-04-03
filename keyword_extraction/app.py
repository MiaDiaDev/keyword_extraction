from websitedownload import WebsiteDownload
from linkanalysis import LinkAnalysis
from languageprocessor import LanguageProcessor


# 1. Initialisierung des Downloads der Testseiten (nur 1 Mal nötig, um Daten lokal zu speichern)
# print("Sollte ein SSL-Fehler auftreten, bitte Programm erneut starten.")
downloader = WebsiteDownload()
downloader.get_all_testpages("https://www.gamestar.de/tests/")

# 2. Zugriff auf die lokalen HTML-Dokumente und Vorbereitung auf NLP-Analysen
# analyzer = LinkAnalysis()
# analyzer.process_files()

# 3. Durchführung der sprachlichen Analyse der Daten und Ermittlung der Frequenzen und Ergebnisse
# language_processor = LanguageProcessor()
# language_processor.process_files()
