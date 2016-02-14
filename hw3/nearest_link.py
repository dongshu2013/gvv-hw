#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import cPickle
import numpy as np
import random
from utils import read_data, compute_dist, haversine_np, calc_link_dis
from itertools import izip
from operator import itemgetter

# def test_1():
#     probes, links = read_data()
#     print "Data loaded"
#     info = nearest_link_and_height(links, [2, 4, 5, 9], probes[0])
#     print "Probe: %s, Link: %s, Height: %f" % (probes[0], links[info[0]][0], info[1])
#
#
# def nearest_link_and_height(links, link_candidates, probe):
#     dists = {}
#     for idx in link_candidates:
#         # compute distance from probe to each link point
#         min_height = probe_to_link_dist(links[idx], probe)
#         dists[idx] = min_height
#
#     # select link from link candidates
#     return min(dists.items(), key=lambda x: x[1])
#
#
# def probe_to_link_dist2(link_points, probe):
#     dists = {}
#     for link_point in link_points:
#         dists[link_point] = compute_dist(link_point, probe)
#
#     heights = []
#     for i in range(len(link_points) - 1):
#         l1_to_l2 = compute_dist(link_points[i], link_points[i+1])
#         p_to_l1 = dists[link_points[i]]
#         p_to_l2 = dists[link_points[i+1]]
#         heights.append(compute_height(p_to_l1, p_to_l2, l1_to_l2))
#     return min(heights)
#
# def compute_height(p_to_l1, p_to_l2, l1_to_l2):
#     p = (p_to_l1 + p_to_l2 + l1_to_l2) / 2
#     s = math.sqrt(p * (p - p_to_l1) * (p - p_to_l2) * (p - l1_to_l2))
#     height = 2 * s / l1_to_l2
#     return height

def probe_to_link_dist(link_points, probe):
    link_points_rad = np.deg2rad(link_points)
    probe_rad = np.deg2rad(probe)

    #底边
    base_side = haversine_np(link_points_rad[:-1,:], link_points_rad[1:,:])
    #腰
    tmp = haversine_np(probe_rad, link_points_rad)
    side1 = tmp[:-1]
    side2 = tmp[1:]

    link_dis = calc_link_dis(base_side, side1, side2)
    return np.min(link_dis)

def main():
    link_candidates = cPickle.load(open("data/link_candidates.pkl", "rb"))
    print len(link_candidates), " link candidates"
    probes, links = read_data()
    print len(probes), " probes"
    print len(links), " links"
    idx = 0
    nearest_links = []
    for probe, candidates in izip(probes, link_candidates):
        link_dis = dict()
        for cand_id in candidates:
            dis = probe_to_link_dist(links[cand_id], probe)
            if dis < 100:
                link_dis[cand_id] = dis
        # print sorted(link_dis.items(), key=itemgetter(1))[:3]
        if len(link_dis) == 0:
            nearest_links.append(None)
        else:
            nearest_link = min(link_dis.items(), key=itemgetter(1))
            nearest_links.append(nearest_link)
        idx += 1
        if idx % 10000 == 0:
            print idx
    with open("data/nearest_link.pkl", "wb") as fout:
        cPickle.dump(nearest_links, fout, 2)

def test():
    link_candidates = cPickle.load(open("data/link_candidates.pkl", "rb"))
    probes, links = read_data()
    d = dict()
    indices = random.sample(range(len(probes)), 10000)
    for idx in indices:
    # for probe, candidates in izip(probes, link_candidates):
        probe = probes[idx]
        candidates = link_candidates[idx]
        link_dis = dict()
        for cand_id in candidates:
            dis = probe_to_link_dist(links[cand_id], probe)
            if dis < 100:
                link_dis[cand_id] = dis
        link_dis = link_dis.items()
        if len(link_dis):
            min_dis = min(link_dis, key=itemgetter(1))[1]
            # print min_dis
            link_dis = [x for x in link_dis if x[1] < min_dis + 10 and min_dis * 3 > x[1]]
            l = len(link_dis)
            if l == 4:
                print link_dis
            d[l] = d.get(l, 0) + 1
    print d

if __name__ == '__main__':
    main()
    # test()
