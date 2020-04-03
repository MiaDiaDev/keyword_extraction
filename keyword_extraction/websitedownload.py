import requests
from bs4 import BeautifulSoup
import re
import io
import os.path
import time
import codecs
from os import walk


class WebsiteDownload:
    # Seite komplett runterladen
    def download_testpage(self, url):
        time.sleep(0.5)
        result = requests.get(url)
        return result.content

    # Webseite speichern
    def save_content_as_file(self, website_content, file_path):
        file_path = self.remove_invalid_chars(file_path)
        with open(file_path, "wb") as f:
            f.write(website_content)
            f.close()

    # ruft Testübersicht auf und sammelt Links zu den ersten Seiten der Tests
    def url_collector(self, seed_url):
        soup = BeautifulSoup(self.download_testpage(seed_url), "lxml")

        # aus der Übersichtseite alle Testlinks herausfiltern
        urls = []
        # Gamestar-Crawler
        for link in soup.find_all("a", {"class": "btn btn-link m-t-1"}):
            urls.append("http://www.gamestar.de" + link.attrs["href"])

        return urls

    # Download aller Testunterseiten
    def get_all_testpages(self, url):
        for firstpage_url in self.url_collector(url):
            complete_test = []
            complete_test.append(self.download_testpage(firstpage_url))
            sub_page_urls = self.find_next_page_of_test(complete_test[0])
            for test_sub_url in sub_page_urls:
                complete_test.append(self.download_testpage(test_sub_url))
            self.save_logic(complete_test)

    # findet die Links zu allen Unterseiten in der ersten Seite eines Tests
    def find_next_page_of_test(self, content):
        soup = BeautifulSoup(content, "lxml")
        pages = []
        for page in soup.find_all("a", {"data-scroll-offset": "-100"}):
            r1 = re.compile("seite[0-9].html")
            current_link = page.attrs["href"]

            if r1.search(current_link):
                pages.append("https://www.gamestar.de" + current_link)
                continue

            r1 = re.compile("fazit.html")
            current_link = page.attrs["href"]

            if r1.search(current_link):
                pages.append("https://www.gamestar.de" + current_link)

        return pages

    # speichert einen Test in einem gleichnamigen Ordner und die HTML-Dokumente entsprechen ihrer Seitenzahl
    def save_logic(self, complete_test):
        name = self.get_website_title(complete_test[0])
        name = self.remove_invalid_chars(name)
        print("Speichere " + name)
        full_path = os.path.join("Tests", name)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        for page, test_page in enumerate(complete_test):
            path = os.path.join(full_path, str(page) + ".html")
            self.save_content_as_file(test_page, path)

    # extrahiert den Titel aus einem HTML-Dokument
    def get_website_title(self, content):
        soup = BeautifulSoup(content, "lxml")
        title = soup.select("h1")[0].text

        return title

    # entfernt inkompatible Zeichen aus dem Test-Titel
    def remove_invalid_chars(self, path):
        deletechars = ':*?"<>|'
        for c in deletechars:
            path = path.replace(c, "")
        return path
