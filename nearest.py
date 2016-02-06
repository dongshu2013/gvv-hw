#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import numpy as np
from utils import read_probes, read_links, compute_distance
from operator import itemgetter
from sklearn.neighbors import NearestNeighbors as NN

def flatten(links):
    link_points = []
    belong = []
    for idx, link in enumerate(links):
        for link_point in link:
            link_points.append(link_point)
            belong.append(idx)
    return link_points, belong

def nearest_bruteforce(probes, link_points):
    nearest = []
    for p_idx, probe in enumerate(probes):
        print "compute nearest for %d" % p_idx
        distance = []
        for idx, link_point in enumerate(link_points):
            dis = compute_distance(link_point, probe)
            distance.append((dis, idx))
        distance.sort(key=itemgetter(0))
        print distance[:5]
        nearest.append(distance[:5])
    return nearest

def nearest_kdtree(probes, link_points):
    nn = NN(n_neighbors=5, algorithm="kd_tree").fit(link_points)
    knns = nn.kneighbors(probes, return_distance=False)
    return knns

def main():
    # probe_file = 'probe_points.sample.csv'
    probe_file = 'probe_points.csv'
    link_file = 'links.csv'

    probes = read_probes(probe_file)
    links = read_links(link_file)

    link_points, belong = flatten(links)

    probes = np.array(random.sample(probes, 5))
    print probes

    print nearest_kdtree(probes, link_points)
    print nearest_bruteforce(probes, link_points)

if __name__ == "__main__":
    main()
