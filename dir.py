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
    road_vec = np.array(link_points[min_idx + 1]) - np.array([min_idx])
    return road_vec

def main():
    probes, links = read_data()
    with open("data/nearest_link.pkl", "rb") as fin:
        nearest_link = cPickle.load(fin)
    with open("data/probe_ids.pkl", "rb") as fin:
        probe_ids = cPickle.load(fin)
    with open("data/probe_times.pkl", "rb") as fin:
        probe_times = cPickle.load(fin)
    with open("data/link_ids.pkl", "rb") as fin:
        link_ids = cPickle.load(fin)
    with open("/Users/lostleaf/dev/gvv-hw/data/dis_ref_nonref.pkl", "rb") as fin:
        dis_ref_nonref = cPickle.load(fin)
    dirs = []
    with open("data/probe_points.csv", "r") as fin:
        with open("data/Partition6467MatchedPoints.csv", "w") as fout:
            for idx, (line, probe, nearest, probe_id, probe_time) in enumerate(izip(fin, probes, nearest_link, probe_ids, probe_times)):
                if nearest is not None:
                    nearest_idx, nearest_dis = nearest
                    road_vec = calc_road_vec(probe, links[nearest_idx])
                    road_vec /= np.linalg.norm(road_vec)
                    sine = None
                    if idx > 0 and probe_ids[idx - 1] == probe_id:
                       drive_vec  =  np.array(probe) - np.array(probes[idx - 1])
                       drive_vec /= np.linalg.norm(drive_vec)
                       sine = road_vec[0] * drive_vec[1] - road_vec[1] * drive_vec[0]
                    if idx < len(probe) - 1 and probe_ids[idx + 1] == probe_id:
                       drive_vec  =  np.array(probes[idx + 1]) - np.array(probe)
                       drive_vec /= np.linalg.norm(drive_vec)
                       sine1 = road_vec[0] * drive_vec[1] - road_vec[1] * drive_vec[0]
                       if sine is None or np.abs(sine1) > np.abs(sine):
                           sine = sine1
                    if sine:
                        dir = sine > 0
                    else:
                        dir = True
                    dis_ref, dis_nonref = dis_ref_nonref[idx]
                    dir_chr = "F" if dir else "T"
                    # print line + "," + ",".join((link_ids[nearest_idx], dir_chr, str(dis_ref), str(dis_nonref)))
                    fout.write(line.strip() + "," + ",".join((link_ids[nearest_idx], dir_chr, str(dis_ref), str(dis_nonref))) + "\n")
                if idx % 10000 == 0:
                    print idx

if __name__ == "__main__":
    main()
