#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cPickle
import numpy as np
from utils import read_data
from itertools import izip

def main():
    probes, links = read_data()
    with open("data/nearest_link.pkl", "rb") as fin:
        nearest_link = cPickle.load(fin)
    with open("data/link_ids.pkl", "rb") as fin:
        link_ids = cPickle.load(fin)
    with open("data/dis_ref_nonref.pkl", "rb") as fin: 
        dis_ref_nonref = cPickle.load(fin)
    with open("data/dir_angles.pkl", "rb") as fin:
        dir_angles = cPickle.load(fin)
    with open("data/probe_points.csv", "r") as fin, open("data/Partition6467MatchedPoints.csv", "w") as fout:
        for idx, (line, nearest, dir_angle, dis_pair) in enumerate(izip(fin, nearest_link, dir_angles, dis_ref_nonref)):
            if nearest is not None:
                nearest_idx, nearest_dis = nearest
                line = line.strip()
                dis_ref, dis_nonref = dis_pair
                dir_chr = "F" if dir_angle > 0 else "T" 
                link_id = link_ids[nearest_idx]
                line += "," + ",".join([link_id, dir_chr, str(dis_ref), str(dis_nonref)])
                print line
                # fout.write(line + "\n")
            if idx > 10:
                break

if __name__ == "__main__":
    main()
