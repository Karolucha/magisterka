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
        if tag == "div" and attributes.get("id", "") == "encyclopedia-detail":
            self.context = "MAIN"
        if tag == "h1" and self.context == "MAIN":
            self.context = "H2"
            #
        if tag == "p" and (self.context == "GO-TO-P" or self.context == "P-NEXT"):
            self.context = "GO-P"

    def handle_data(self, data):
        data = data.strip()
        if self.context == "H2":
            self.happening['title'] = data

        if self.context == "GO-P":
            self.description += data
            self.description += " "

    def handle_endtag(self, tag):
        if self.context == "H2" and tag == "h1":
            self.context = "GO-TO-P"
        if self.context == "GO-P" and tag == "p":
            self.context = "P-NEXT"
        if self.context == "P-NEXT" and tag == "div":
            self.happening['description'] = self.description
            self.happenings.append(self.happening)
            print(self.happening)
            self.context = ""

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
        if tag == "div" and attributes.get("id", "") == "encyclopedia-list":
            self.context = "MAIN"
        if tag == "a" and self.context == "MAIN":
            self.happening = {}
            self.happening['source_url'] = "http://www.doktor-medi.pl" + attributes.get("href", "")
            print(self.happening)
            self.happenings.append(self.happening)
            self.context = "MAIN"

        if tag == "div" and attributes.get("class", "") == "pagination pagination-centered":
            self.context = ""

    def handle_data(self, data):
        data = data.strip()

    def handle_endtag(self, tag):
        pass

    def __init__(self):
        HTMLParser.__init__(self, strict=False)
        self.date = ""
        self.happenings = []
        self.context = ""

    def get_happenings(self):
        return self.happenings


class GenerateUrls():
    def __init__(self):
        self.base_url = "http://www.doktor-medi.pl/encyklopedia/"
        self.urls = []
        self.days = []

    def get_urls(self):
        self.days = ['http://www.doktor-medi.pl/encyklopedia/']
        for i in range(1, 7):
            self.days.append('http://www.doktor-medi.pl/encyklopedia/' + str(i))
        print('ggggggggggg')
        return self.days


if __name__ == '__main__':
    import run
    run.start('doktor_medi', '.')