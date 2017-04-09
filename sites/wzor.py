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
            print("content?")
            content = webutils.clean_html(webutils.read_url(url, "utf-8"))
            print("before feed ", url)
            parser.feed(content)
        parser.close()
        return parser.get_happenings()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "div" and attributes.get("class", "") == "list_box":
            self.context = "MAIN"
        if tag == "a" and self.context == "MAIN":
            self.happening = {}
            self.happening['source_url'] = "http://www.portalzdrowia.pl/" + attributes.get("href", "")
            print(self.happening)
            self.context = "GOT IT"

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
        self.days = ['http://www.portalzdrowia.pl/category.html,9,name,dieta_i_odchudzanie']
        print('ggggggggggg')
        return self.days


if __name__ == '__main__':
    import run
    run.start('portalzdrowia', '.')