from geopy.distance import vincenty
from geopy.distance import great_circle
import csv
import json

def main():
    probe_file = 'probe_points.sample.csv'
#    link_file = 'links.sample.csv'
#    probe_file = 'probe_points.csv'
    link_file = 'links.csv'
    output_file = 'output.json'
    compute_all_distance(probe_file, link_file, output_file)

def compute_all_distance(probe_file, link_file, output_file):
    links = readlinks(link_file)
    f = open(output_file, 'a+');
    for point in readprobe(probe_file):
        distances = {}
        for k, v in links.items():
            distances[k] = []
            for shape in v:
                distances[k].append(compute_distance(shape, point))
        f.write(json.dumps(distances) + "\n")

def readprobe(probe_file):
    with open(probe_file, 'r') as p:
        datareader = csv.reader(p)
        for row in datareader:
            lat, lon = row[3], row[4]
            point = (lat, lon)
            yield point

def readlinks(link_file):
    links = {}
    with open(link_file, 'r') as l:
        datareader = csv.reader(l)
        for row in datareader:
            lid = row[0]
            shape_info = row[14]
            shapes = []
            for point in shape_info.split('|'):
                lat, lon, _ = point.split('/')
                shapes.append((lat, lon))
            links[lid] = shapes
    return links

def compute_distance(src_loc, dst_loc):
    return vincenty(src_loc, dst_loc).meters

if __name__ == '__main__':
    main()
