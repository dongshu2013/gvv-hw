#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import read_probes, read_links
import cPickle

def main():
    probe_file = 'probe_points.csv'
    link_file = 'links.csv'
    probes = read_probes(probe_file)
    links = read_links(link_file)
    with open("probes.pkl", "wb") as fout:
        cPickle.dump(probes, fout, 2)
    with open("links.pkl", "wb") as fout:
        cPickle.dump(links, fout, 2)

if __name__ == "__main__":
    main()
