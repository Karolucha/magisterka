'''
Created on 12 mar 2015

@author: karolina
'''
import re
from html.parser import HTMLParser
import common.webutils as webutils
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
        # print(attributes)
        # if re.search(r"tresc", attributes.get("class", ""), re.I):
        if tag == "h1":
            print("JEST  ")
            self.context = "GO-H2"
        # if tag == "div" and attributes.get("class", "") == "sort-menu sort-menu--medium collapse__wrapper":
        #     self.context = "MAIN"
        #     print("is main")
        # if tag == "h1" and self.context == "MAIN":
        #     self.context = "GO-H2"
            #
        if (tag == "p" or tag == "b") and (self.context == "GO-TO-P" or self.context == "NEXT-P") and attributes.get("class", "") != "info":
            self.context = "GO-P"


    def handle_data(self, data):
        data = data.strip()
        if self.context == "GO-H2":
            self.happening['title'] = data
            print('title ', data)

        if self.context == "GO-P":
            self.description += data
            self.description += " "
            print('data dsc ', data)

    def handle_endtag(self, tag):
        if self.context == "GO-H2" and tag == "h1":
            self.context = "NEXT-P"
            print("go to p")
        if self.context == "GO-P" and (tag == "p" or tag == "b"):
            self.context = "GO-TO-P"
        if tag == "div" and self.context == "GO-TO-P":
            self.context = ""
            self.happenings.append(self.happening)
            self.happening['description'] = self.description


    def prepare_happening(self):
        self.description = ""

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
        # happenings = happenings[:2]
        for happening in happenings:
            if happening.get("source_url") is not None:
                print("source url:", happening.get("source_url"))
                happening.update(cls.obtain_happening_details(happening.get("source_url", "")))
        return happenings

    @classmethod
    def obtain_happening_details(cls, url):
        if not url:
            return
        content = webutils.clean_html(webutils.read_url(url,  "iso-8859-2"))
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
            content = webutils.clean_html(webutils.read_url(url, "iso-8859-2"))
            parser.feed(content)
        parser.close()
        return parser.get_happenings()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "div" and attributes.get("class", "") == "sort-menu sort-menu--medium collapse__wrapper open":
            self.context = "BEF-MAIN"
        if tag == "div" and self.context == "BEF-MAIN" and attributes.get("class", "") == "row":
            self.context = "MAIN"
        if tag == "nav" and self.context == "MAIN" and attributes.get("class", "") == "pagination-center":
            self.context = ""
        if tag == "a" and self.context == "MAIN":
            happening = {}
            happening['source_url'] = attributes.get("href", "")
            self.happenings.append(happening)
            print(happening)
            self.context = "MAIN"

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
        self.days = ['https://www.doz.pl/ziola/w_1-wszystkie']
        # for i in range(20,98):
        #     self.days.append('https://www.doz.pl/zdrowie/w0_' + str(i) + '-wszystkie')
        #     print('https://www.doz.pl/zdrowie/w0_' + str(i) + '-wszystkie')
        return self.days


if __name__ == '__main__':
    import run
    run.start('doz', '.')