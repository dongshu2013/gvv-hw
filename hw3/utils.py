#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import cPickle
import numpy as np
from geopy.distance import vincenty
from datetime import datetime

def calc_link_dis(base_side, side1, side2):
    # print base_side.shape, side1.shape, side2.shape
    ans = np.zeros_like(base_side, dtype=np.float)
    mask = np.ones_like(base_side, dtype=np.bool)

    #point on the link
    mask_on_line = np.logical_and(base_side == side1+side2, mask)
    mask = np.logical_xor(mask, mask_on_line)
    ans[mask_on_line] = 0

    #the adjaceny points on the link is overlapped
    mask_point = np.logical_and(base_side < 1e-10, mask)
    mask = np.logical_xor(mask, mask_point)
    ans[mask_point] = side1[mask_point]

    side1_sqr = side1 * side1
    side2_sqr = side2 * side2
    base_side_sqr = base_side * base_side

    #obtuse case 1
    mask_obtuse1 = np.logical_and(side1_sqr > base_side_sqr + side2_sqr, mask)
    mask = np.logical_xor(mask, mask_obtuse1)
    ans[mask_obtuse1] = side2[mask_obtuse1]

    #obtuse case 2
    mask_obtuse2 = np.logical_and(side2_sqr > base_side_sqr + side1_sqr, mask)
    mask = np.logical_xor(mask, mask_obtuse2)
    ans[mask_obtuse2] = side1[mask_obtuse2]

    #compute height by Heron's formula
    half_p = (base_side[mask] + side1[mask] + side2[mask]) * 0.5 # half perimeter
    area = np.sqrt(half_p * (half_p - side1[mask]) * (half_p - side2[mask]) * (half_p - base_side[mask]))
    ans[mask] = 2 * area / base_side[mask]
    return ans

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

def read_csv(file_path, col):
    ret = []
    with open(file_path, "r") as fin:
        reader = csv.reader(fin)
        for row in reader:
            val = row[col]
            ret.append(val)
    return ret

def read_link_ids(link_file):
    return read_csv(link_file, 0)

def read_link_lengths(link_file):
    return [float(x) for x in read_csv(link_file, 3)]

def read_probe_ids(probe_file):
    return read_csv(probe_file, 0)

def read_probe_times(probe_file):
    FMT_STR = "%m/%d/%Y %I:%M:%S %p"
    return [datetime.strptime(x, FMT_STR) for x in read_csv(probe_file, 1)]

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
