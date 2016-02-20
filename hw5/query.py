#!/bin/env/python

import urllib2
import sys
import logging
import os
import shutil
import cv2
from centers import get_centers
from combine import combine_images


BASE_URL = 'http://dev.virtualearth.net/REST/v1/Imagery/Map'
KEY = 'AlbGt7PP-W5qWxfB12esT9wOPXLIBfg5uQzOCySOd-DkGo1hw6JAoraf-y2_crxU'
#KEY = 'Aofb3blsrt2vPjZgzj2JoCjyv43a9OsESy7B5-40etee9LSt_0oCXjY62OfUL7eZ'


root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stderr)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)


def url(center):
    return BASE_URL + '/Aerial/' + ','.join(map(str, center)) + \
        '/20/?mapSize=512,572&key=' + KEY


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
    if len(sys.argv) != 6:
        print "usage: python %s lat1 lon1 lat2 lon2 save_name.jpg" % sys.argv[0]
        sys.exit(1)
    centers, size = get_centers(*map(float, sys.argv[1:-1]))
    logging.info('%d centers generated' % len(centers))
    process(centers)
    img = combine_images(size)
    cv2.imwrite(sys.argv[-1], img)


if __name__ == '__main__':
    main()
    #test()
