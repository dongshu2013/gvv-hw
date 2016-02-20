#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import csv
import os.path
import matplotlib.pyplot as plt
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
    diff = abs(degree - base)
    return (dist, degree, diff, base)


def compare_slopes(slopes, link_slopes):
    link_slopes = sorted(link_slopes, key=lambda x:x[0])
    return [ compare_slope(slope, link_slopes) for slope in slopes ]


def process():
    writer = csv.writer(open('../data/slopes_with_base.csv', 'w+'), delimiter=',')
    diffs = []
    cnt_slope = 0
    cnt_1 = 0
    cnt_2 = 0
    cnt_5 = 0
    link_set = set()
    link_set_1 = set()
    link_set_2 = set()
    link_set_5 = set()
    with open('../data/slopes.csv', 'r') as m:
        datareader = csv.reader(m)
        for row in datareader:
            if row[1] and row[2]:
                link_set.add(row[0])
                cpt_slopes = [tuple(map(float, x.split('/'))) for x in row[1].split('|')]
                link_slopes = [tuple(map(float, x.split('/'))) for x in row[2].split('|')]
                for slope in compare_slopes(cpt_slopes, link_slopes):
                    cnt_slope += 1
                    diff = slope[2]
                    # if diff >= 5:
                    #     diff = 5
                    diffs.append(diff)
                    if diff < 1:
                        cnt_1 += 1
                        link_set_1.add(row[0])
                    if diff < 2:
                        cnt_2 += 1
                        link_set_2.add(row[0])
                    if diff >= 5:
                        cnt_5 += 1
                        link_set_5.add(row[0])
                    link = [row[0]]
                    link.extend(slope)
                    writer.writerow(link)
#                    if abs(slope[2]) < 2:
#                        print "%s,%s" %(row[0], slope)
    print "%d slopes, affect %d links" % (cnt_slope, len(link_set))
    print "%d(%f) slopes <1 error, affect %d links" % (cnt_1, cnt_1 / float(cnt_slope), len(link_set_1))
    print "%d(%f) slopes <2 error, affect %d links" % (cnt_2, cnt_2 / float(cnt_slope), len(link_set_2))
    print "%d(%f) slopes >=5 error, affect %d links" % (cnt_5, cnt_5 / float(cnt_slope), len(link_set_5))
    plt.hist(diffs, range=(0, 20), bins=20)
    plt.ylim(0, 800000)
    plt.show()

def main():
    process()


if __name__ == "__main__":
    main()
