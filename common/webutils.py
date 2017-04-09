# -*- coding: utf-8 -*-
'''
Created on 26-11-2013

@author: michal
'''
from html.parser import HTMLParser
from socket import error
import time
import re
import urllib.request

MAX_TRIALS = 5


def read_url(url, codec='utf-8', trial=MAX_TRIALS):
    request = urllib.request.Request(url)
    request.add_header("User-Agent", "Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1")
    opener = urllib.request.build_opener();
    try:
        content = opener.open(request, timeout=30).read().decode(codec)
    except error as e:
        erno = MAX_TRIALS - trial + 1
        print("Błąd(%r): %r" % (erno, e))
        if trial > 0:
            time.sleep(2)
            return read_url(url, codec, trial - 1)
        # raise Exception("Błąd połączenia %r" % e)
        print("BŁĄD POŁĄCZENIA")
        return ''
    except Exception as e:
        print("return empty becouse ", e)
        return ''
    # print("content is ", content)
    return content


def clean_html(content):
    content = HTMLParser().unescape(content)
    content = content.replace('\xa0', ' ')
    return content


class LinkExtractor(HTMLParser):
    '''
    Klasa wyciągająca linki z podanego feedu.
    Podczas inicjalizacji klasy podajemy wzór wyrażenia regularnego w postaci łańcucha znaków
    Podane wyrażenie jest używane do rozposnanie oczekiwanych urli oraz identyfikatora imprezy
    W zwiąsku z powyższym wyrażenie powinno zawierać nazwaną grupę <event_id> np.
    '^http.+view_detail\\&agid=(?P<event_id>\\d+)'
    '''

    def handle_starttag(self, tag, attrs):
        #        pattern = re.compile('^http.+view_detail\\&agid=(?P<event_id>\\d+)')
        attr = dict(attrs)
        if ((tag == "a") and self.pattern.match(attr.get('href', ''))):
            res = self.pattern.match(attr['href'])
            self.results.append({'url': attr['href'], 'event_id': res.groupdict().get('event_id')})
            #             print ("attr: %s" % attr['href'])
            #            print "EventId: %(event_id)s \n"% res.groupdict()

    def reset_results(self):
        self.results = []

    def __init__(self, patternString):
        HTMLParser.__init__(self)
        self.pattern = re.compile(patternString)
        self.results = list()


