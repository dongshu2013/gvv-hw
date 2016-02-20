#!/bin/env/python

import math

MIN_LAT = -85.05112878;
MAX_LAT = 85.05112878;
MIN_LON = -180;
MAX_LON = 180;


def clip(n, min_value, max_value):
    return min(max(n, min_value), max_value);


def pix_to_latlon(px, py, level=20):
    msize = 256 << level
    x = (clip(px, 0, msize - 1) / msize) - 0.5;
    y = 0.5 - (clip(py, 0, msize - 1) / msize);

    lat = 90 - 360 * math.atan(math.exp(-y * 2 * math.pi)) / math.pi;
    lon = 360 * x;
    return (lat, lon)


def latlon_to_pix(lat, lon, level = 20):
    lat = clip(lat, MIN_LAT, MAX_LAT);
    lon = clip(lon, MIN_LON, MAX_LON);

    x = (lon + 180) / 360;
    sin_lat = math.sin(lat * math.pi / 180);
    y = 0.5 - math.log((1 + sin_lat) / (1 - sin_lat)) / (4 * math.pi);

    msize = 256 << level
    px = clip(x * msize + 0.5, 0, msize - 1);
    py = clip(y * msize + 0.5, 0, msize - 1);
    return (int(px), int(py))


def test():
    print (47.610, -122.107)
    print latlon_to_pix(47.610, -122.107)

    print '******************************'

    print (43168150, 93745005)
    print pix_to_latlon(43168150.095022224, 93745004.8788148)


if __name__ == '__main__':
    test()
