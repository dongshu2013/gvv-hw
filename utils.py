#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import cPickle
import numpy as np
from geopy.distance import vincenty


def haversine_np(probe, link_points):
    delta = probe - link_points
    d_lat = delta[:, 0]
    d_lon = delta[:, 1]
    if type(probe) != np.ndarray:
        probe = np.array(probe)

    if len(probe.shape) == 1:
        lat1 = probe[0]
    elif len(probe.shape) == 2:
        lat1 = probe[:, 0]

    lat2 = link_points[:, 0]

    tmp = np.sin(d_lat/2.0)**2 + np.cos(lat1) * \
        np.cos(lat2) * np.sin(d_lon/2.0)**2
    ratio = 2 * np.arcsin(np.sqrt(tmp))

    return 6371004 * ratio


def read_probes(probe_file):
    probes = []
    with open(probe_file, 'r') as p:
        datareader = csv.reader(p)
        for row in datareader:
            lat, lon = row[3], row[4]
            point = (float(lat), float(lon))
            probes.append(point)
    return probes


def read_links(link_file):
    links = []
    with open(link_file, 'r') as l:
        datareader = csv.reader(l)
        for row in datareader:
            shape_info = row[14]
            shapes = []
            for point in shape_info.split('|'):
                lat, lon, _ = point.split('/')
                shapes.append((float(lat), float(lon)))
            links.append(shapes)
    return links


def flatten_uniq(links):
    belong = dict()
    for idx, link in enumerate(links):
        for link_point in link:
            belong[link_point] = belong.get(link_point, [])
            belong[link_point].append(idx)

    return belong.keys(), belong


def read_data():
    probes = cPickle.load(open("data/probes.pkl", "rb"))
    links = cPickle.load(open("data/links.pkl", "rb"))
    return probes, links


def compute_dist(src_loc, dst_loc):
    return vincenty(src_loc, dst_loc).meters


def compute_dist_via_haversine(src_loc, dst_loc):
    lat1 = src_loc[0]
    lon1 = src_loc[1]
    lat2 = dst_loc[0]
    lon2 = dst_loc[1]

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km

if __name__ == '__main__':
    main()
