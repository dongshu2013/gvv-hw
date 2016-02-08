#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import numpy as np
from utils import read_probes, read_links, haversine_np, compute_dist
from operator import itemgetter
from sklearn.neighbors import NearestNeighbors as NN
from itertools import izip
from time import time
import math
import cPickle
import geopy

def flatten(links):
    link_points = []
    belong = {}
    for idx, link in enumerate(links):
        for link_point in link:
            link_points.append(link_point)
            belong[link_point] = idx
    return link_points, belong

def nearest_probe_force(probe, link_points, n):
    distance = haversine_np(probe, link_points)
    knns = np.argsort(distance)[:n]
    # print distance[knns]
    return knns

def nearest_force(probes, link_points, n=10):
    nearest = []
    for p_idx, probe in enumerate(probes):
        # print "compute nearest for %d" % p_idx
        knns = nearest_probe_force(probe, link_points, n)
        nearest.append(knns)
    return np.array(nearest)

def nearest_kdtree(probes, link_points, n=10, is_filter=True):
    _n = n * 3 if is_filter else n
    nn = NN(n_neighbors=_n, algorithm="kd_tree").fit(link_points)
    knn_candidates = nn.kneighbors(probes, return_distance=False)
    if not is_filter:
        return knn_candidates
    knns = []
    for probe, cands in izip(probes, knn_candidates):
        ret = nearest_probe_force(probe, link_points[cands], n)
        knns.append(cands[ret])
    return np.array(knns)

def read_data():
    # probe_file = 'probe_points.sample.csv'
    probe_file = 'probe_points.csv'
    link_file = 'links.csv'
    probes = read_probes(probe_file)
    links = read_links(link_file)
    return probes, links

def evaluate(func, label=""):
    t1 = time()
    ret = func()
    t2 = time()
    print label + " time elapsed: %f" % (t2 - t1)
    return ret

def test():
    probes, link_points, belong = read_data()
    print "%d probe points loaded" % len(probes)
    print "%d link points loaded" % len(link_points)

    probes = np.array(random.sample(probes, 100))
    # print probes

    probes = np.deg2rad(probes)
    link_points = np.deg2rad(link_points)

    knns_kd = evaluate(lambda: nearest_kdtree(probes, link_points, n=30, is_filter=True), "kdtree")
    knns_force = evaluate(lambda: nearest_force(probes, link_points, n=30), "brute force")

    for idx, (k1, k2) in enumerate(izip(knns_kd, knns_force)):
        diff = np.setdiff1d(k2, k1)
        if diff.size > 0:
            print diff
            print haversine_np(probes[idx], link_points[diff])
            # print haversine_np(probes[idx], link_points[k1])
            # print haversine_np(probes[idx], link_points[k2])

def test_1():
    probes, links = read_data()
    print "Data loaded"
    info = nearest_link_and_height(links, [2, 4, 5, 9], probes[0])
    print "Probe: %s, Link: %s, Height: %f" % (probes[0], links[info[0]][0], info[1])

def nearest_link_and_height(links, link_candidates, probe):
    dists = {}
    for idx in link_candidates:
        #compute distance from probe to each link point
        min_height = probe_to_link_dist(links[idx], probe)
        dists[idx] = min_height

    #select link from link candidates
    return min(dists.items(), key=lambda x: x[1])

def probe_to_link_dist2(link_points, probe):
    dists = {}
    for link_point in link_points:
        dists[link_point] = compute_dist(link_point, probe)

    heights = []
    for i in range(len(link_points) - 1):
        l1_to_l2 = compute_dist(link_points[i], link_points[i+1])
        p_to_l1 = dists[link_points[i]]
        p_to_l2 = dists[link_points[i+1]]
        heights.append(compute_height(p_to_l1, p_to_l2, l1_to_l2))
    return min(heights)

def probe_to_link_dist(link_points, probe):
    size = len(link_points)
    l1_to_l2 = compute_dist(link_points[0], link_points[size - 1])
    p_to_l1 = compute_dist(probe, link_points[0])
    p_to_l2 = compute_dist(probe, link_points[size - 1])
    return compute_height(p_to_l1, p_to_l2, l1_to_l2)

def compute_height(p_to_l1, p_to_l2, l1_to_l2):
    p = (p_to_l1 + p_to_l2 + l1_to_l2) / 2
    s = math.sqrt(p * (p - p_to_l1) * (p - p_to_l2) * (p - l1_to_l2))
    height = 2 * s / l1_to_l2
    return height

def main():
    probes, links = read_data()
    link_points, belong = flatten(links)

    print "%d probe points loaded" % len(probes)
    print "%d link points loaded" % len(link_points_)

    # probes = np.array(random.sample(probes, 10000))
    # print probes

    probes_rad = np.deg2rad(probes)
    link_points_ = np.array(link_points_)
    link_points = np.deg2rad(link_points_)
    knns_kd = nearest_kdtree(probes_rad, link_points, n=40, is_filter=False)
    link_candidates = [set([bel for lat, lon in link_points_[knns] for bel in belong[lat, lon]]) for knns in knns_kd]
    with open("link_candidates.pkl", "wb") as fout:
        cPickle.dump(link_candidates, fout, 2)

if __name__ == "__main__":
    #main()
    test_1()
