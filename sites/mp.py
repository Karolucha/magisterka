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

        if tag == "h1":
            self.context = "H1"
            #
        if tag == "p" and self.context == "GO-TO-P":
            self.context = "GO-P"

        if tag == "div" and self.context == "GO-TO-P" and attributes.get("class", "") == "date":
            self.context = ""
            self.happening['description'] = self.description
            self.happenings.append(self.happening)
            print(self.happening)

    def handle_data(self, data):
        data = data.strip()
        if self.context == "GO-H2":
            self.happening['title'] = data
            print('title ', data)

        if self.context == "GO-P":
            self.description += data
            self.description += " "

    def handle_endtag(self, tag):

        if self.context == "H1" and tag == "h1":
            self.context = "GO-TO-P"

        if self.context == "GO-P" and tag == "p":
            self.context = "GO-TO-P"


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
        if len(self.happenings) == 1:
            return self.happening
        else:

            return self.happenings

    @classmethod
    def obtain_happenings_details(cls, happenings):
        for happening in happenings:
            if happening.get("source_url") is not None:
                print(happening.get("source_url"))
                happening.update(cls.obtain_happening_details(happening.get("source_url", ""), 1))
        return happenings

    @classmethod
    def extract_nexts(self, content):
        print("content?")
        base_url = "http://mp.pl/cukrzyca"
        content = webutils.read_url(base_url)
        # patternUrl = 'http\:\//www.mp.pl/cukrzyca/aktualnosci/157649,morwa-czy-rzeczywiscie-pomaga-w-leczeniu-cukrzycy'
        patternUrl = 'http\:\//www.mp.pl\/cukrzyca\/aktualnosci\/\d+,.*'
        link_extractor = webutils.LinkExtractor(patternUrl)
        link_extractor.feed(content)
        urls = []
        print('link_extracot', link_extractor.results)
        for result in link_extractor.results:
            print("result ", result)
            happening = {}
            happening = {'source_url': result.get('url')}
            if happening not in urls:
                urls.append(happening)
        urls = urls[:1]
        print('finally')
        return urls

    @classmethod
    def feed_parsers(cls,happening_parser, content):

        happening_parser.feed(content)
        happening_parser.close()
        happening = {}


    @classmethod
    def obtain_happening_details(cls, url, counter):
        counter += 1
        if not url:
            return
        content = webutils.clean_html(webutils.read_url(url, ))
        happening_parser = cls()
        happening_parser.feed_parsers(happening_parser,content)
        urls = happening_parser.extract_nexts(content)
        # for url in urls:
        #     happening = {}
        #     happening = {'source_url': result.get('url')}
        #     if happening not in urls:
        #         urls.append(happening)
        if  counter < 3:
            happening_parser.happenings.extract(happening_parser.obtain_happenings_details(urls))
        try:
            happening = happening_parser.get_happening()
        except :
            print("Błąd parsowania "+url )
        return happening


class HappeningListParser(HTMLParser):
    @classmethod
    def parse_urls(cls, urlList):
        parser = cls()
        # for url in urlList:
        print("content?")
        base_url = "http://mp.pl/cukrzyca"
        content = webutils.read_url(base_url)
        # patternUrl = 'http\:\//www.mp.pl/cukrzyca/aktualnosci/157649,morwa-czy-rzeczywiscie-pomaga-w-leczeniu-cukrzycy'
        patternUrl = 'http\:\//www.mp.pl\/cukrzyca\/aktualnosci\/\d+,.*'
        link_extractor = webutils.LinkExtractor(patternUrl)
        link_extractor.feed(content)
        urls = []

        print('link_extracot', link_extractor.results)
        results = link_extractor.results[:1]
        for result in results:
            print("result ", result)
            happening = {}
            happening = {'source_url': result.get('url')}
            if happening not in urls:
                urls.append(happening)
        print('finally')
        return urls

    # def handle_starttag(self, tag, attrs):
    #     attributes = dict(attrs)
    #     if tag == "div" and attributes.get("class", "") == "list_box":
    #         self.context = "MAIN"
    #     if tag == "a" and self.context == "MAIN":
    #         self.happening = {}
    #         self.happening['source_url'] = "http://www.portalzdrowia.pl/" + attributes.get("href", "")
    #         print(self.happening)
    #         self.context = "GOT IT"
    #
    #     # if tag == "div" and re.search(r"tresc", attributes.get("class", ""), re.I) and self.context == "OD":
    #     #     self.context = "START"
    #
    # def handle_data(self, data):
    #     data = data.strip()
    #     if self.context == "START":
    #         self.date += data
    #         self.date += " "
    #
    # def handle_endtag(self, tag):
    #     if self.context == "GOT IT" and tag == "a":
    #         # self.context = ""
    #         self.context = "MAIN"
    #         self.happenings.append(self.happening)

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
        self.urls = []
        print('ggggggggggg')
        return self.urls


if __name__ == '__main__':
    import run
    run.start('mp', '.')