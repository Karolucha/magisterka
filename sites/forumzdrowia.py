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
    username = "forumzdrowiaplBot"
    item_name = "happening"

    @classmethod
    def get_urls(cls):
        generate = GenerateUrls()
        return generate.get_urls()


class HappeningDetailParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "p":
            print(self.context)
        if tag == "div" and attributes.get("id", "") == "artykul":
            self.context = "MAIN"
        if tag == "div" and self.context == "MAIN" and attributes.get("class", "") == "autor_info":
            self.context = "BZDURA"

        if tag == "div" and self.context == "MAIN" and attributes.get("class", "") == "afil":
            self.context = "BZDURA"

        if tag == "p" and self.context == "MAIN":
            self.context = "P"
        if tag == "h1" and self.context == "MAIN":
            self.context = "H1"
            #
        if tag == "script" and self.context == "MAIN":
            self.context = ""
            #
        if tag == "p" and (self.context == "GO-TO-P" or self.context == "P-NEXT") and attributes.get("class", "") != "info":
            self.context = "GO-P"

    def handle_data(self, data):
        data = data.strip()
        if self.context == "H1":
            print('TITLE ', data)
            self.happening['title'] = data

        if self.context == "P":
            print('dsc ', data)
            self.description += data
            self.description += " "

    def handle_endtag(self, tag):
        if self.context == "H1" and tag == "h1":
            self.context = "MAIN"
        if self.context == "BZDURA" and tag == "div":
            self.context = "MAIN"
        if self.context == "P" and tag == "p":
            self.happening['description'] = self.description
            self.happenings.append(self.happening)
            self.context = "MAIN"
            print("append")

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
                print('teraz parsujemy: ', happening.get("source_url", "EE"))
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
            print("Błąd parsowania "+url)
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
        if tag == "div" and attributes.get("class", "") == "aktualnosci":
            self.context = "MAIN"
        if self.context == "MAIN" and tag == "a":
            self.happening = {}
            self.happening['source_url'] = "http://www.forumzdrowia.pl/" + attributes.get("href", "")
            self.context = "GOT IT"
            print('source is ', self.happening)
            self.happenings.append(self.happening)

        if tag == "div" and self.context == "MAIN" and attributes.get("id", "") == "numery_stron":
            self.context = ""
        # if tag == "div" and re.search(r"tresc", attributes.get("class", ""), re.I) and self.context == "OD":
        #     self.context = "START"

    def handle_data(self, data):
        data = data.strip()
        if self.context == "START":
            self.date += data
            self.date += " "

    def handle_endtag(self, tag):
        if self.context == "GOT IT" and tag == "a":
            # self.context = ""
            self.context = "MAIN"


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
        self.base_url = "http://www.forumzdrowia.pl/"
        self.urls = []
        self.days = []

    def get_urls(self):
        # self.days = ['http://www.forumzdrowia.pl/id,216,strona,4']
        # [215, 257,216,218,606,320,184,183,283,185,373,375,320]
        cats = [353, 189,233,322,338,373,612,620,566,567,568,402,403,577,447,497,530]
        for cat in cats:
            for i in range(1,5):
                self.days.append('http://www.forumzdrowia.pl/id,'+str(cat) + ',strona,' + str(i))
        print('ggggggggggg', self.days)
        return self.days


if __name__ == '__main__':
    import run
    run.start('forumzdrowia', '.')