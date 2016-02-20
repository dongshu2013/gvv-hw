from tile_transform import latlon_to_pix, pix_to_latlon
from itertools import product

def get_centers(lat1, lon1, lat2, lon2, size=(512, 512)):
    lat1, lat2 = min(lat1, lat2), max(lat1, lat2)
    lon1, lon2 = min(lon1, lon2), max(lon1, lon2)
    x1, y1 = latlon_to_pix(lat1, lon1)
    x2, y2 = latlon_to_pix(lat2, lon2)
    print lat1, lon1, x1, y1
    print lat2, lon2, x2, y2
    x_rng = range(x1, x2 + 1, size[0])
    y_rng = range(y1, y2 + 1, -size[1])
    xy_pairs = product(x_rng, y_rng)
    return [pix_to_latlon(x, y) for x, y in xy_pairs]

def main():
    print len(get_centers(47.678559869527817, -122.13099449872971, 47.688559869527817, -122.12099449872971))

if __name__ == "__main__":
    main()
