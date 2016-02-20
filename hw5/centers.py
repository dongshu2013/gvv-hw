from itertools import product
import math

MIN_LAT = -85.05112878;
MAX_LAT = 85.05112878;
MIN_LON = -180;
MAX_LON = 180;


def clip(n, min_value, max_value):
    return min(max(n, min_value), max_value);


def pix_to_latlon(px, py, level=20):
    px = float(px)
    py = float(py)
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

    print (43168150, 93745004)
    print pix_to_latlon(43168150, 93745004)


def get_centers(lat1, lon1, lat2, lon2, size=(512, 512)):
    lat1, lat2 = min(lat1, lat2), max(lat1, lat2)
    lon1, lon2 = min(lon1, lon2), max(lon1, lon2)
    x1, y1 = latlon_to_pix(lat1, lon1)
    x2, y2 = latlon_to_pix(lat2, lon2)
    x_rng = range(x1, x2 + 1, size[0])
    y_rng = range(y1, y2 + 1, -size[1])
    xy_pairs = product(x_rng, y_rng)
    return [pix_to_latlon(x, y) for x, y in xy_pairs], (len(x_rng), len(y_rng))

def main():
    test()
    print len(get_centers(42.057000, -87.674883, 42.058500, -87.676883))

if __name__ == "__main__":
    main()
