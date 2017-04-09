import sqlite3
from collections import OrderedDict
from itertools import islice
import pandas
import re
import io
import codecs
import os


def read_articles(table):
    conn = sqlite3.connect('../sites/example.db')
    c = conn.cursor()
    # c.execute("SELECT description FROM " + table + " Limit 10")
    c.execute("SELECT description FROM " + table)
    print(c.fetchone())
    articles = c.fetchall()
    conn.commit()
    conn.close()
    return articles


def example_article(table):
    conn = sqlite3.connect('../sites/example.db')
    c = conn.cursor()
    c.execute("SELECT description FROM " + table + " Limit 2")
    # c.execute("SELECT description FROM " + table)
    article = c.fetchall()[0]
    conn.commit()
    conn.close()
    return article


def get_train(records):
    records.extend(read_articles('forumzdrowia'))
    # records.extend(read_articles('doz'))
    # records.extend(read_articles('poradnikzdrowie'))
    # records.extend(read_articles('articles'))
    for i, record in enumerate(records):
        records[i] = prepare_article(record)
    # print(records)
    return records

def get_forbiddens():
    forbiddens = ['bo', 'abd', 'się', 'są', 'które', 'który', 'że', 'żeby', 'być', 'stać', 'mieć', 'posiadać',
                  'mogą', 'jeśli', 'też', 'może', 'to',
                  'także', 'również']
    # forbiddens=[]
    f = open('forbidden_stop', 'r', encoding='utf-8-sig')
    forbiddens.extend(f.read().splitlines())
    f.close()
    # import pprint
    # pprint.pprint(forbiddens)
    # print(forbiddens)
    return forbiddens


def prepare_article(article):
    article = re.sub('[().,-:/]', '', article[0]).lower()
    # article = re.sub('y$', 'a', article[0])
    # article = re.sub('\d+', '', article[0])
    article_list = [word.lower() for word in article.split()]

    for forbidden in get_forbiddens():
        if forbidden in article:
            article = article.replace(' ' + forbidden + ' ', ' ')
            # article = re.sub(' ' + forbidden + ' ', ' ', article)

    counter = pandas.value_counts(article.split())
    return article
    # return islice(OrderedDict(counter), 3)


def unify_token(token):
    results = os.system('cat morfologik.txt | less /' + token)
    print(results)


# unify_token('kotek')

# result = get_train(read_articles('doz'))
# print(result)
