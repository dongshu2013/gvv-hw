#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle
import numpy as np
from utils import calc_link_dis, read_data, haversine_np
from itertools import izip

def calc_road_vec(probe, link_points):
    link_points_rad = np.deg2rad(link_points)
    probe_rad = np.deg2rad(probe)

    base_side = haversine_np(link_points_rad[:-1,:], link_points_rad[1:,:])
    tmp = haversine_np(probe_rad, link_points_rad)
    side1 = tmp[:-1]
    side2 = tmp[1:]

    link_dis = calc_link_dis(base_side, side1, side2)
    min_idx = np.argmin(link_dis)
    road_vec = np.array(link_points[min_idx + 1]) - np.array(link_points[min_idx])
    return road_vec

#drive from probe1 to probe2
def get_cosine(probe1, probe2, road_vec):
    drive_vec  =  np.array(probe2) - np.array(probe1)
    road_vec /= np.linalg.norm(road_vec)
    drive_vec /= np.linalg.norm(drive_vec)
    # print probe1, probe2, drive_vec
    cosine = np.dot(road_vec, drive_vec)
    return cosine

def main():
    probes, links = read_data()
    with open("data/nearest_link.pkl", "rb") as fin:
        nearest_link = cPickle.load(fin)
    with open("data/probe_ids.pkl", "rb") as fin:
        probe_ids = cPickle.load(fin)
    dir_angles = []
    for idx, (probe, nearest, probe_id) in enumerate(izip(probes, nearest_link, probe_ids)):
        # print "probe", idx
        if nearest is not None:
            nearest_idx, nearest_dis = nearest
            road_vec = calc_road_vec(probe, links[nearest_idx])
            # print road_vec
            cosine = None
            if idx > 0 and probe_ids[idx - 1] == probe_id:
                cosine = get_cosine(probes[idx - 1], probe, road_vec)

            if idx < len(probe) - 1 and probe_ids[idx + 1] == probe_id:
                cosine1 = get_cosine(probe, probes[idx + 1], road_vec)
                if cosine is None or np.abs(cosine1) > np.abs(cosine):
                    cosine = cosine1
            if cosine is None:
                cosine = 1
            dir_angles.append(cosine)
        else:
            dir_angles.append(None)
        if idx % 10000 == 0:
            print idx
    print len(dir_angles)
    with open("data/dir_angles.pkl", "wb") as fout:
        cPickle.dump(dir_angles, fout, 2)
if __name__ == "__main__":
    main()
