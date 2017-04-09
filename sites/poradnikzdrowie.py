'''
Created on 12 mar 2015

@author: karolina
'''
from html.parser import HTMLParser
import re
import common.webutils as webutils
import hashlib
from common.happeningwriter import HappeningWriter as XmlWriter


class Config:
    username = "portalzdrowiaplBot"
    item_name = "happening"

    @classmethod
    def get_urls(cls):
        generate = GenerateUrls()
        return generate.get_urls()


class HappeningDetailParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        # if tag == "p":
        #     print(tag)
        if tag == "div" and attributes.get("id", "") == "main_column":
            self.context = "MAIN"
            print('main')
            return

        if tag == "div" and attributes.get("id", "") == "right_column":
            self.context = ""
            self.happening['description'] = self.description
            self.happenings.append(self.happening)
            print('end ', self.happening)
            return

        if tag == "h1" and self.context == "MAIN":
            self.context = "H1"
            print('h1')
            return

        if (tag == "div" and self.context == "MAIN" and ((attributes.get("class", "") == "lead_article") or
                attributes.get("class", "") == "text_article dp_autolink")):
            self.context = "GO-P"
            return

        if (tag == "p" or tag == "li") and self.context == "GO-P":
            self.context = "P"
            return

    def handle_data(self, data):
        data = data.strip()
        if self.context == "H1":
            self.happening['title'] = data
            print('title', data)
            return

        if self.context == "P":
            if "Aktualizacja: " in data or not data:
                return
            self.description += data
            self.description += " "
            # print('p', data)
            self.context = "GO-P"

    def handle_endtag(self, tag):
        if self.context == "P" and tag == "div":
            self.context = "MAIN"
        if self.context == "H1" and tag == "h1":
            self.context = "MAIN"

    def prepare_happening(self):
        self.description = ""
        self.happenings.append(self.happening)

    def __init__(self):
        HTMLParser.__init__(self, strict=False)
        self.happenings = []
        self.happening = {}
        self.context = ""
        self.description = ""

    def get_happenings(self):
        return self.happenings

    def get_happening(self):
        if len(self.happenings) == 0:
            return self.happening
        else:

            return self.happenings[0]

    @classmethod
    def obtain_happenings_details(cls, happenings):
        for happening in happenings:
            if happening.get("source_url") is not None:
                print(happening.get("source_url"))
                happening.update(cls.obtain_happening_details(happening.get("source_url", "")))
        return happenings

    @classmethod
    def obtain_happening_details(cls, url):
        if not url:
            return
        content = webutils.clean_html(webutils.read_url(url, ))
        happening_parser = cls()
        happening_parser.feed(content)
        happening_parser.close()
        happening = {}
        try:
            happening = happening_parser.get_happening()
        except :
            print("Błąd parsowania "+url )
        return happening


class HappeningListParser(HTMLParser):
    @classmethod
    def parse_urls(cls, urlList):
        parser = cls()
        for url in urlList:
            content = webutils.clean_html(webutils.read_url(url, "utf-8"))
            parser.feed(content)
        parser.close()
        return parser.get_happenings()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "div" and attributes.get("id", "") == "main_column":
            self.context = "MAIN"

        if tag == "div" and attributes.get("id", "") == "right_column":
            self.context = ""

        if tag == "h3":
            self.context = "H3"

        if tag == "a" and self.context == "H3":
            self.context = "GOT IT"
            sources = [source['source_url'] for source in self.happenings]
            if "http://www.poradnikzdrowie.pl/" + attributes.get("href", "") not in sources:
                self.happening = {}
                self.happening['source_url'] = "http://www.poradnikzdrowie.pl/" + attributes.get("href", "")
                self.happenings.append(self.happening)
                print('jakie połączenia ', self.happening['source_url'])

        # if tag == "div" and re.search(r"tresc", attributes.get("class", ""), re.I) and self.context == "OD":
        #     self.context = "START"

    def handle_data(self, data):
        data = data.strip()
        if self.context == "START":
            self.date += data
            self.date += " "

    def handle_endtag(self, tag):
        if self.context == "GOT IT" and tag == "a":
            self.context = "MAIN"
            # self.happenings.append(self.happening)

    def prepare_happening(self):
        for happening in self.happenings:
            if happening["name"] == self.happening["name"]:
                break

    def __init__(self):
        HTMLParser.__init__(self, strict=False)
        self.date = ""
        self.happenings = []
        self.context = ""


    def get_happenings(self):
        return self.happenings


class GenerateUrls():
    def __init__(self):
        self.base_url = "http://www.poradnikzdrowie.pl/"
        self.urls = []
        self.days = []

    def get_urls(self):
        cats = ['bol', 'alergie', 'cukrzyca', 'hormony', 'laryngologia', 'nowotwory', 'zeby',
                'choroby-meskie', 'choroby-kobiece', 'choroby-genetyczne', 'choroby-pasozytnicze', 'choroby-zakazne',
                'domowa-apteczka', 'uklad-moczowy', 'uklad-nerwowy', 'uklad-krwionosny', 'uklad-oddechowy',
                'uklad-odpornosciowy', 'uklad-pokarmowy', 'urazy-wypadki', 'grypa-i-przeziebienia']
        # cats = ['oczy', 'skora']
        for cat in cats:
            for i in range(1, 6):
                self.days.append('http://www.poradnikzdrowie.pl/zdrowie/' + cat + '/?page=' + str(i))
                print('http://www.poradnikzdrowie.pl/zdrowie/' + cat + '/?page=' + str(i))

        print('ggggggggggg')
        return self.days


if __name__ == '__main__':
    import run
    run.start('poradnikzdrowie', '.')