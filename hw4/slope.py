#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import csv
import os.path
from utils import save_data, load_data


def cpt_slope(match_point, link):
    ref_alt = link[0]
    point_alt = match_point[1]

    dist = match_point[2]
    if ref_alt is None or dist == 0:
        return dist, None
    else:
        diff_alt = point_alt - ref_alt
        return dist, math.degrees(math.atan(diff_alt/dist))


def process(matched_points, links):
    link_to_slopes = {}
    #tuple (linkPVID, altitude, dist_from_ref)
    for match_point in matched_points:
        linkPVID = match_point[0]
        link = links[linkPVID]
        dist, slope = cpt_slope(match_point, link)
        if slope != None:
            link_to_slopes.setdefault(linkPVID, []).append((dist, slope))
    return link_to_slopes


def save_link_to_slopes(link_to_slopes, links):
    with open('../data/slopes.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for pvid, slopes in link_to_slopes.iteritems():
            link = []
            link.append(pvid)
            slopes = sorted(slopes, key=lambda x:x[0])
            link.append('|'.join(['/'.join(map(str, slope)) for slope in slopes]))
            link.append('|'.join(['/'.join(map(str, slope)) for slope in links[pvid][1]]))
            writer.writerow(link)


def main():
    if not os.path.exists('../data/matched_points.pkl') or not os.path.exists('../data/links.pkl'):
        print "Saving Data"
        save_data()
    print "Loading Data"
    matched_points, links = load_data()
    print "Data Loaded"
    link_to_slopes = process(matched_points, links)
    save_link_to_slopes(link_to_slopes, links)


if __name__ == "__main__":
    main()
