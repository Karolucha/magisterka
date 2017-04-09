'''
Created on 12 mar 2015

@author: karolina
'''
from html.parser import HTMLParser

import sqlite3

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
        # if tag == "p":
        #     print(tag)
        if tag == "div" and attributes.get("class", "") == "box_content":
            self.context = "MAIN"
        if tag == "h2" and self.context == "MAIN":
            self.context = "GO-H2"
            #
        if tag == "p" and (self.context == "GO-TO-P" or self.context == "P-NEXT") and attributes.get("class", "") != "info":
            self.context = "GO-P"

    def handle_data(self, data):
        data = data.strip()
        if self.context == "GO-H2":
            self.happening['title'] = data
            print('title ', data)

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
            # try:
            content = webutils.clean_html(webutils.read_url(url, "utf-8"))
            print("before feed ", url)
            parser.feed(content)
            parser.fit_url(url)
            parser.close()
            # except Exception as e:
            #     print("error ", e)
        return parser.get_happenings()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "b" and self.context == "BEF-ALL":
            print("IS B")
            self.context = "TITLE"
        if self.context == "TITLE":
            print(tag)
            print(attributes)
        if tag == "div" and self.context == "MAIN" and attributes.get("id", "") == "toc":
            self.context = "TOC"
            # print("toc")
        if (tag == "p" or tag == "li") and self.context == "MAIN":
            self.context = "DSC"
        if tag == "span" and self.context == "MAIN" and any(attributes.get("id", "") == breaki for breaki in self.breaks) :
            self.context = ""
            # print("NEVER HERE?")
            self.happening['description'] = self.description
            self.happenings.append(self.happening)
            self.happening = {}
            self.no_more = False
            print("koniec obiektu")
            return
        if attributes.get("class", "") == "mw-headline" and self.context == "MAIN":
            self.context = "DSC"

        if attributes.get("class", "") == "external text" and self.context == "TITLE":
            self.context = ""

        # if attributes.get("class", "") == "mw-editsection" and self.context == "MAIN":
        #     self.context = "DSC"

        if self.context == "TOC" and tag == "p":
            self.context = "MAIN"

        if self.context == "" and tag == "p":
            self.context = "BEF-ALL"


    def handle_data(self, data):
        data = data.strip()
        if self.context == "TITLE":
            print("is title ", data)
            self.happening['title'] = data
            self.context = "DSC"

        if self.context == "DSC":
            # print("data dsc")
            if data and not data.isspace():
                self.description += data
                self.description += ' '

    def handle_endtag(self, tag):
        if self.context == "DSC" and (tag == "p" or tag == "li" or tag == "span"):
            # print("more dsc")
            self.context = "MAIN"


    def prepare_happening(self):
        for happening in self.happenings:
            if happening["name"] == self.happening["name"]:
                break

    def __init__(self):
        HTMLParser.__init__(self, strict=False)
        self.date = ""
        self.description = ""
        self.happenings = []
        self.happening = {}
        self.breaks = ["Przypisy", "Zobacz_te.C5.BC", "Bibliografia", "Linki_zewn.C4.99trzne"]

        self.context = ""
        self.no_more = False

    def fit_url(self, url):
        print('fit url ', url)
        if len(self.happenings) > 0:
            happening = self.happenings.pop()
            if happening.get('title', None):
                happening['source_url'] = url
                self.happenings.append(happening)

    def get_happenings(self):
        return self.happenings


class GenerateUrls():
    def __init__(self):
        self.base_url = "https://pl.wikipedia.org/"
        self.urls = []
        self.days = []

    def get_urls(self):
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute("SELECT title FROM dr_medi")
        all_articles = c.fetchall()
        # all_articles = all_articles[0]
        # all_articles = c.fetchone()
        for article in all_articles:
            article = "_".join(article[0].split())
            print("new url is  https://pl.wikipedia.org/wiki/" + article)
            self.days.append("https://pl.wikipedia.org/wiki/" + article)
        print('ggggggggggg')
        return self.days


if __name__ == '__main__':
    import run
    run.start('wiki', '.')