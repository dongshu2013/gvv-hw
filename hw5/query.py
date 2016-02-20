#!/bin/env/python

import urllib2
import sys
import logging


BASE_URL = 'http://dev.virtualearth.net/REST/v1/Imagery/Map'
KEY = 'AlbGt7PP-W5qWxfB12esT9wOPXLIBfg5uQzOCySOd-DkGo1hw6JAoraf-y2_crxU'


root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stderr)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)


def url(center):
    return BASE_URL + '/Aerial/' + ','.join(map(str, center)) + \
        '/20/?mapSize=512,512&key=' + KEY


def query(url, output):
    logging.info("Url:" + url)
    image = urllib2.urlopen(url)
    with open(output,'wb') as o:
        o.write(image.read())


def test():
    center = (47.678559869527817, -122.13099449872971)
    query(url(center), 'test.jpeg')


def main():
    if len(sys.argv) != 2:
        print "Wrong number of arguments, exiting ..."
        sys.exit(1)
    center = tuple(sys.argv[1].split(','))
    query(url(center), sys.argv[1] + '.jpeg')


if __name__ == '__main__':
    #main()
    test()
