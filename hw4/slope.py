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
        degree = math.degrees(math.atan(diff_alt/dist))
        #set threshold to filter abnormal points
        if degree < 8 and degree > -9:
            return dist, degree
        else:
            return dist, None


def process(matched_points, links, dist_from_link_threshold = 50):
    link_to_slopes = {}
    #tuple (linkPVID, altitude, dist_from_ref, dist_from_link)
    for match_point in matched_points:
        linkPVID = match_point[0]
        dist_from_link = match_point[3]
#        if dist_from_link > dist_from_link_threshold:
#            continue
        link = links[linkPVID]
        dist, degree = cpt_slope(match_point, link)
        if dist != 0 and degree:
            link_to_slopes.setdefault(linkPVID, []).append((dist, degree))
    return link_to_slopes


def save_link_to_slopes(link_to_slopes, links):
    count = 0
    with open('../data/slopes.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for pvid, slopes in link_to_slopes.iteritems():
            link = []
            link.append(pvid)
            slopes = sorted(slopes, key=lambda x:x[0])
            count = count + len(slopes)
            link.append('|'.join(['/'.join(map(str, slope)) for slope in slopes]))
            link.append('|'.join(['/'.join(map(str, slope)) for slope in links[pvid][1]]))
            writer.writerow(link)
    print count


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
