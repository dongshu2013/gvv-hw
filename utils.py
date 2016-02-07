from geopy.distance import vincenty
from geopy.distance import great_circle
import csv
import json
import numpy as np

def haversine_np(probe, link_points):
    delta = probe - link_points
    d_lat = delta[:, 0]
    d_lon = delta[:, 1]
    lat1 = probe[0]
    lat2 = link_points[:, 0]

    tmp = np.sin(d_lat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(d_lon/2.0)**2
    ratio = 2 * np.arcsin(np.sqrt(tmp))

    return 6371004 * ratio

def read_probes(probe_file):
    probes = []
    with open(probe_file, 'r') as p:
        datareader = csv.reader(p)
        for row in datareader:
            lat, lon = row[3], row[4]
            point = (float(lat), float(lon))
            probes.append(point)
    return probes

def read_links(link_file):
    links = [] 
    with open(link_file, 'r') as l:
        datareader = csv.reader(l)
        for row in datareader:
            shape_info = row[14]
            shapes = []
            for point in shape_info.split('|'):
                lat, lon, _ = point.split('/')
                shapes.append((float(lat), float(lon)))
            links.append(shapes)
    return links

def compute_distance(src_loc, dst_loc):
    return vincenty(src_loc, dst_loc).meters

if __name__ == '__main__':
    main()
