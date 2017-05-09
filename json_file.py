#!/usr/bin/python2
#
# http://www.forum-raspberrypi.de/Thread-python-neue-datei-erstellen-mit-python-2-7?pid=281304#pid281304
# http://stackoverflow.com/a/37795053/2641799
#
import time
import json
import os
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

gamefilespath = '/tmp/'

def new_gamefile(id, data):
    with io.open(gamefilespath + id + '.json', 'w', encoding='utf8') as outfile:
        str_ = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
        outfile.write(to_unicode(str_))


def read_gamefile(id):
    with open(gamefilespath + id + '.json') as data_file:
        return json.load(data_file)


# Usage:

daten = {
    'Player1': {
        'Name': 'meigrafd',
        'Score': 123,
    },
    'Player2': {
        'Name': 'hamyam',
        'Score': 321,
    },
}

new_gamefile('987', daten)

print time.ctime( os.path.getctime(gamefilespath + '987' + '.json') )

game_data = read_gamefile('987')
print game_data['Player1']
print game_data['Player1']['Name']
print game_data['Player1']['Score']