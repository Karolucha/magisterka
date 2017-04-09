'''
Created on 12 mar 2015

@author: karolina
'''
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

        if tag == "div" and attributes.get("id", "") == "art_tresc":
            self.context = "MAIN"

        if tag == "div" and attributes.get("align", "") == "right" and self.context == "MAIN":
            self.context = ""
            self.happening['description'] = self.description
            self.happenings.append(self.happening)
            print(self.happening)

        if tag == "h1" and self.context == "MAIN":
            self.context = "GO-H2"

        if self.context == "GO-TO-P":
            print("tag ", tag)
        if (tag == "p" or tag == "strong") and (self.context == "GO-TO-P" or self.context == "P-NEXT"):
            print("is p")
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
        if self.context == "GO-H2" and tag == "h1":
            self.context = "GO-TO-P"
        if self.context == "GO-P" and (tag == "p" or tag == "strong"):
            self.context = "P-NEXT"

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
        content = webutils.clean_html(webutils.read_url(url, "iso-8859-2"))
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
            print("content?")
            content = webutils.clean_html(webutils.read_url(url, "iso-8859-2"))
            print("before feed ", url)
            print("content ", content)
            parser.feed(content)
        parser.close()
        return parser.get_happenings()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        print(tag)
        if tag == "div" and attributes.get("id", "") == "art_tresc":
            self.context = "MAIN"

        if tag == "a" and self.context == "MAIN":
            self.happening = {}
            self.happening['source_url'] = attributes.get("href", "")
            print(self.happening)
            self.context = "MAIN"
            self.happenings.append(self.happening)

    def handle_data(self, data):
        pass

    def handle_endtag(self, tag):
        if self.context == "MAIN" and tag == "ul":
            self.context = ""

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
        self.urls = []
        self.days = []

    def get_urls(self):
        self.days = ['http://www.medisa.pl/spis_p.html']
        print('ggggggggggg')
        return self.days


if __name__ == '__main__':
    import run
    run.start('medisa', '.')