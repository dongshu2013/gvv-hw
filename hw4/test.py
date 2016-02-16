#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import csv
import os.path
from utils import save_data, load_data

def cpt_base(dist, link_slopes):
    for i in range(0, len(link_slopes)):
        if link_slopes[i][0] >= dist:
            break
    lower = None
    upper = None
    if i - 1 >= 0 and i - 1 < len(link_slopes):
        lower = link_slopes[i - 1][1]
    if i >= 0 and i < len(link_slopes):
        upper = link_slopes[i][1]
    if not lower:
        base = upper
    elif not upper:
        base = lower
    else:
        base = (upper + lower) / 2
    return base


def compare_slope(slope, link_slopes):
    dist = slope[0]
    degree = slope[1]
    base = cpt_base(dist, link_slopes)
    diff = degree - base
    return (dist, degree, diff, base)


def compare_slopes(slopes, link_slopes):
    link_slopes = sorted(link_slopes, key=lambda x:x[0])
    return [ compare_slope(slope, link_slopes) for slope in slopes ]


def process():
    writer = csv.writer(open('../data/slopes_with_base.csv', 'w+'), delimiter=',')
    with open('../data/slopes.csv', 'r') as m:
        datareader = csv.reader(m)
        for row in datareader:
            if row[1] and row[2]:
                cpt_slopes = [tuple(map(float, x.split('/'))) for x in row[1].split('|')]
                link_slopes = [tuple(map(float, x.split('/'))) for x in row[2].split('|')]
                for slope in compare_slopes(cpt_slopes, link_slopes):
                    link = []
                    link.append(row[0])
                    link.append(slope)
                    writer.writerow(link)
#                    if abs(slope[2]) < 2:
#                        print "%s,%s" %(row[0], slope)


def main():
    process()


if __name__ == "__main__":
    main()
