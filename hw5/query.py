#!/bin/env/python

import urllib2
import sys
import logging
import os
import shutil
from centers import get_centers


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
    with open(output,'wb+') as o:
        o.write(image.read())


def process(centers):
    for i in range(len(centers)):
        query(url(centers[i]), './tmp/' + str(i) + '.jpeg')


def create_temp_dir():
    if os.path.exists('./tmp'):
        shutil.rmtree('./tmp')
    os.mkdir('./tmp')


def test():
    create_temp_dir()
    centers = [(47.678559869527817, -122.13099449872971),
               (47.45223343, -122.2323354)]
    process(centers)


def main():
    create_temp_dir()
    if len(sys.argv) != 2:
        logging.info("Wrong number of arguments, exiting ...")
        sys.exit(1)
    bound = map(float, sys.argv[1].split(','))
    centers = get_centers(*bound)
    logging.info('%d centers generated' % len(centers))
    process(centers)


if __name__ == '__main__':
    main()
    #test()
