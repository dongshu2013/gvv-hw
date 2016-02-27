import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cv2
from sklearn.neighbors import NearestNeighbors as NN

def latlonelev_to_xyz(points):
    EARTH_R = 6371004 #r of earth in meters
    if len(points.shape) == 1:
        points = points.reshape((-1, 3))
    lat_rad = np.deg2rad(points[:, 0])
    lon_rad = np.deg2rad(points[:, 1])
    elev = points[:, 2]
    x = EARTH_R * np.cos(lat_rad) * np.cos(lon_rad)
    y = EARTH_R * np.cos(lat_rad) * np.sin(lon_rad)
    z = EARTH_R * np.sin(lat_rad) + elev;
    return np.vstack((x, y, z)).T

def find_nearest(nn, points2_prime, M):
    dist, idx = nn.kneighbors(np.dot(points2_prime, M))
    return dist, idx[:, 0]
        
#M is a 4*3 Matrix, transposed since data points are in row vectors
def icp(points1, points2_prime, M_init):
    M = M_init
    nn = NN(n_neighbors=1).fit(points1)
    for i in xrange(1000):
        dist, idx = find_nearest(nn, points2_prime, M)
        print "Iteration %d, average distance %f" % (i, np.mean(dist))
        M = np.dot(np.linalg.pinv(points2_prime), points1[idx, :])
    dist, idx = find_nearest(nn, points2_prime, M)
    print "Final result, average distance %f" % (np.mean(dist))

def main():
    p1 = np.genfromtxt("data/pointcloud1.fuse")
    p2 = np.genfromtxt("data/pointcloud2.fuse")
    points1 = latlonelev_to_xyz(p1)
    points2 = latlonelev_to_xyz(p2)
    points2_prime = np.hstack( (points2, np.ones((points2.shape[0], 1))) )
    translation = np.zeros((1, 3))
    M_init = np.concatenate((np.eye(3), np.zeros((1, 3))), axis=0)
    print M_init
    icp(points1, points2_prime, M_init)

if __name__ == "__main__":
    main()
