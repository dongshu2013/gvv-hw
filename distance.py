#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cPickle
import numpy as np
from utils import calc_link_dis, read_data, haversine_np
from itertools import izip

#side1 is near to ref node, side2 is near to nonref node
def calc_proj_len(base, side1, side2):
    #compute the projection length of side1 onto base by law of cosine
    proj_len = (base * base + side1 * side1 - side2 * side2) / (2 * base)
    if proj_len > base:
        proj_len = base
    if proj_len < 0:
        proj_len = 0
    return proj_len

def dis_ref_nonref(probe, link_points, nearest_dis, link_len):
    link_points_rad = np.deg2rad(link_points)
    probe_rad = np.deg2rad(probe)

    base_side = haversine_np(link_points_rad[:-1,:], link_points_rad[1:,:])
    tmp = haversine_np(probe_rad, link_points_rad)
    side1 = tmp[:-1]
    side2 = tmp[1:]

    link_dis = calc_link_dis(base_side, side1, side2)
    min_idx = np.argmin(link_dis)
    proj_len = calc_proj_len(base_side[min_idx], side1[min_idx], side2[min_idx])
    dis_ref = np.sum(base_side[:min_idx]) + proj_len
    dis_ref = dis_ref / np.sum(base_side) * link_len
    dis_nonref = link_len - dis_ref
    return dis_ref, dis_nonref

def main():
    probes, links = read_data()
    with open("data/link_lengths.pkl", "rb") as fin:
        link_lengths = cPickle.load(fin)
    with open("data/nearest_link.pkl", "rb") as fin:
        nearest_link = cPickle.load(fin)
    idx = 0
    dis_ref_nonref_list = []
    for probe, nearest in izip(probes, nearest_link):
        if nearest is not None:
            nearest_idx, nearest_dis = nearest
            dis_ref, dis_nonref = dis_ref_nonref(probe, links[nearest_idx], nearest_dis, link_lengths[nearest_idx])
            dis_ref_nonref_list.append((dis_ref, dis_nonref))
            idx += 1
            if idx % 10000 == 0:
                print idx
        else:
            dis_ref_nonref_list.append(None)
    print len(dis_ref_nonref_list)
    with open("data/dis_ref_nonref.pkl", "wb") as fout:
        cPickle.dump(dis_ref_nonref_list, fout, 2)

if __name__ == "__main__":
    main()
