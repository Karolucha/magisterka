'''
Created on 12 mar 2015

@author: karolina
'''

import os
import importlib
import sys
import getopt
from sites.insert_db import insert_records

thisdir = os.path.dirname(__file__)
libdirs = (os.path.join(thisdir, '../'), os.path.join(thisdir, '../common'))
for libdir in libdirs:
    if libdir not in sys.path:
        sys.path.insert(0, libdir)
# from common.logger import Logger
#
# log_level = Logger.DEBUG


def start(name, path):
    # log = Logger(name, log_level)

    module = importlib.import_module(name)

    items = module.HappeningListParser.parse_urls(module.Config.get_urls())
    items = module.HappeningDetailParser.obtain_happenings_details(items)
    print('items', items)
    # for item in items:
    #     print('item', item)
    proceed_items = []
    for single_happening in items:
        if single_happening and len(single_happening.keys()) > 1 and len(single_happening.get('description','').split()) > 5:
            proceed_items.append(single_happening)
    print(len(items))
    print(len(proceed_items))
    # insert_records(proceed_items)
    #
    # module.XmlWriter.write_to_file(proceed_items, module.Config.item_name, module.Config.username, path)

def start(name, database):
    module = importlib.import_module(name)
    items = module.HappeningListParser.parse_urls(module.Config.get_urls())
    proceed_items = module.HappeningDetailParser.obtain_happenings_details(items)
    insert_records(database, proceed_items)
    module.XmlWriter.write_to_file(proceed_items, module.Config.item_name, module.Config.username, path)

# start('portalzdrowia', '.')





if __name__ == '__main__':
    argv = sys.argv
    try:
        opts, args = getopt.getopt(argv[1:], "n:b:")
    except getopt.GetoptError:
        sys.exit(2)
    options = dict(opts)
    name = options.get("-n")
    path = options.get("-b")
    print(name)
    if (name is not None and path is not None):
        start(name, path)
    elif (name is not None):
        start(name, "./")
    else:
        print("Należy podać nazwę modułu syndykatora np.\n python3 run.py -n piotrkowpl")
        print(
            "Można również podać ścieżkę zapisu pliku za pomocą argumentu -b np.  python3 run.py -n merlin.merlinBook -b /home/imports/book/input")
        sys.exit(2)

