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
        if tag == "div" and attributes.get("class", "") == "box_content":
            self.context = "MAIN"
        if tag == "h2" and self.context == "MAIN":
            self.context = "GO-H2"
            #
        if tag == "p" and (self.context == "GO-TO-P" or self.context == "P-NEXT") and attributes.get("class", "") != "info":
            self.context = "GO-P"
        if tag == "l" and (self.context == "GO-TO-P" or self.context == "P-NEXT"):
            self.context = "GO-P"

        if tag == "em" and (self.context == "GO-TO-P" or self.context == "P-NEXT"):
            self.context = "P-NEXT"

    def handle_data(self, data):
        data = data.strip()
        if self.context == "GO-H2":
            self.happening['title'] = data

        if self.context == "GO-P":
            self.description += data
            self.description += " "

    def handle_endtag(self, tag):
        if self.context == "GO-H2" and tag == "h2":
            self.context = "GO-TO-P"
        if self.context == "GO-P" and tag == "p":
            self.context = "P-NEXT"
        if self.context == "P-NEXT" and tag == "div":
            self.happening['description'] = self.description
            # self.happenings.append(self.happening)
            self.context = ""

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
        print('happenings obtain', len(happenings))
        for happening in happenings:
            if happening.get("source_url") is not None:
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
            print("Błąd parsowania " + url )
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
        if tag == "div" and attributes.get("class", "") == "list_box":
            self.context = "MAIN"
        if tag == "h3" and self.context == "MAIN":
            self.context = "h3"
        if tag == "a" and self.context == "MAIN":
            self.happening = {}
            self.happening['source_url'] = "http://www.portalzdrowia.pl/" + attributes.get("href", "")
            self.context = "GOT IT"
        if self.context == "MAIN" and tag == "div " and attributes.get("class", "") == "pagination":
                self.context = ""
        # if tag == "div" and re.search(r"tresc", attributes.get("class", ""), re.I) and self.context == "OD":
        #     self.context = "START"

    def handle_data(self, data):
        data = data.strip()
        if self.context == "START":
            self.date += data
            self.date += " "

    def handle_endtag(self, tag):

        if self.context == "h3" and tag == "h3":
            self.context = "MAIN"
        if self.context == "GOT IT" and tag == "a":
            # self.context = """
            self.context = "MAIN"
            self.happenings.append(self.happening)

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
        self.base_url = "http://www.portalzdrowia.pl/"
        self.urls = []
        self.days = []

    def get_urls(self):
        self.days = ['http://www.portalzdrowia.pl/category.html,37,1,30']
        print('ggggggggggg')
        return self.days


if __name__ == '__main__':
    import run
    run.start('portalzdrowia', '.')