#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle
from utils import read_probes, read_links, read_link_ids, read_link_lengths


def main():
    probe_file = 'data/probe_points.csv'
    link_file = 'data/links.csv'

    probes = read_probes(probe_file)
    links = read_links(link_file)
    link_ids = read_link_ids(link_file)
    link_lengths = read_link_lengths(link_file)

    with open("data/probes.pkl", "wb") as fout:
        cPickle.dump(probes, fout, 2)
    with open("data/links.pkl", "wb") as fout:
        cPickle.dump(links, fout, 2)
    with open("data/link_ids.pkl", "wb") as fout:
    	cPickle.dump(link_ids, fout, 2)
    with open("data/link_lengths.pkl", "wb") as fout:
    	cPickle.dump(link_lengths, fout, 2)

if __name__ == "__main__":
    main()
