#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import cPickle
import csv

def read_matched_points(matched_points_file):
    matched_points = []
    with open(matched_points_file, 'r') as m:
        datareader = csv.reader(m)
        for row in datareader:
            altitude = row[5]
            dist_from_ref = row[10]
            linkPVID = row[8]
            matched_point = (linkPVID, float(altitude), float(dist_from_ref))
            matched_points.append(matched_point)
    return matched_points

def read_links(link_file):
    links = {}
    with open(link_file, 'r') as l:
        datareader = csv.reader(l)
        for row in datareader:
            linkPVID = row[0]
            links[linkPVID] = []

            shape_info = row[14]
            ref_alt = shape_info.split('|')[0].split('/')[2]
            if ref_alt:
                links[linkPVID].append(float(ref_alt))
            else:
                links[linkPVID].append(None)

            slope_info = row[16]
            slopes = []
            for slope in slope_info.split('|'):
                if slope:
                    dist, degree = slope.split('/')
                    slopes.append((float(dist), float(degree)))
            links[linkPVID].append(slopes)
    return links

def read_raw_data():
    matched_points = read_matched_points('../data/matched_points.csv')
    links = read_links('../data/links.csv')
    return matched_points, links

def save_data():
    matched_points, links = read_raw_data();
    with open('matched_points.pkl', 'wb+') as fout:
        cPickle.dump(matched_points, fout, 2)
    with open('links.pkl', 'wb+') as fout:
        cPickle.dump(links, fout, 2)

def load_data():
    matched_points = cPickle.load(open('matched_points.pkl', 'rb'))
    links = cPickle.load(open('links.pkl', 'rb'))
    return matched_points, links
