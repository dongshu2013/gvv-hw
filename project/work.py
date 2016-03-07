import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from glob import glob
from skimage.measure import label
from operator import itemgetter
from sklearn.linear_model import LinearRegression as LinRegr
from collections import Counter

def filter_white(img):
    mask = np.logical_and(img[:, :, 1] > 200, img[:, :, 2] > 200)
    tmp = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
    tmp[mask] = 255
    tmp = tmp[1050:1450]
    return tmp

def morph(img):
    kernel = np.ones((10, 10),np.uint8)
    img1 = cv2.morphologyEx(img,cv2.MORPH_CLOSE, kernel)   
    kernel1 = np.ones((10, 10), np.uint8)
    img1 = cv2.morphologyEx(img1,cv2.MORPH_OPEN, kernel1)
    return img1

def connected_component(img):
    label_img = label(img, neighbors=8)
    y = np.bincount(label_img.ravel())
    ii = np.nonzero(y)[0]
    label_count = zip(ii, y[ii])
    label_count.sort(key=itemgetter(1), reverse=True)
    label_count = label_count[1:]
    return label_img, label_count

def find_solid(label_count, label_img1, tmp):
    for lab, count in label_count[:3]:
        x, y = np.where(label_img1 == lab)
        if np.max(y) > 1200 and np.max(y) < 1700:
            x_right, y_right = x, y
    for lab, count in label_count[:2]:
        x, y = np.where(label_img1 == lab)
        if np.min(y) < 200:
            x_left, y_left = x, y
    label_tmp = label(tmp, neighbors=8)
    label_left = Counter([label_tmp[x, y] for x, y in zip(x_left, y_left)]).most_common(1)[0][0]
    label_right = Counter([label_tmp[x, y] for x, y in zip(x_right, y_right)]).most_common(1)[0][0]
    x_left, y_left = np.where(label_tmp == label_left)
    x_right, y_right = np.where(label_tmp == label_right)
    return x_left, y_left, x_right, y_right

def fit_lines(x_left, x_right, y_left, y_right, tmp):
    model_left = LinRegr().fit(x_left.reshape((-1, 1)), y_left)
    model_right = LinRegr().fit(x_right.reshape((-1, 1)), y_right)
    x_line = np.arange(tmp.shape[0]).reshape((-1, 1))
    y_leftline = np.maximum(model_left.predict(x_line).astype(np.int), 0)
    y_rightline = np.minimum(model_right.predict(x_line).astype(np.int), tmp.shape[1] - 1)
    mask_mid = np.zeros((tmp.shape[0], tmp.shape[1]), dtype=np.bool)
    x_white, y_white = np.where(tmp>0)
    for x in xrange(tmp.shape[0]):
        y_left = y_leftline[x]
        y_right = y_rightline[x]
        filt = np.logical_and(x_white == x, np.logical_and(y_white > y_left + 100, y_white < y_right - 100))
        mask_mid[x_white[filt], y_white[filt]] = True
    x_mid, y_mid = np.where(mask_mid)
    model_mid = LinRegr().fit(x_mid.reshape((-1, 1)), y_mid)
    y_midline = np.minimum(model_mid.predict(x_line).astype(np.int), tmp.shape[1] - 1)
    return model_left, model_mid, model_right, y_leftline, y_midline, y_rightline

def draw_white(height, img, y_leftline, y_midline, y_rightline):
    tmp = img.copy()
    for x in xrange(height):
        y_left = y_leftline[x]
        y_right = y_rightline[x]
        y_mid = y_midline[x]
        tmp[x + 1050, y_left : y_mid + 1, [0, 1]] = 255
        tmp[x + 1050, y_mid : y_right + 1, [1, 2]] = 255

    return tmp

def find_white(img, basename):
    tmp = filter_white(img)
    tmp_morph = morph(tmp)
    label_morph, label_morph_count = connected_component(tmp_morph)
    x_left, y_left, x_right, y_right = find_solid(label_morph_count, label_morph, tmp)

    model_left, model_mid, model_right, y_leftline, y_midline, y_rightline = fit_lines(x_left, x_right, y_left, y_right, tmp)
    tmp1 = draw_white(tmp.shape[0], img, y_leftline, y_midline, y_rightline)
    # cv2.imwrite("binary_left/" + basename, tmp1)
    return model_left, model_mid, model_right, y_leftline, y_midline, y_rightline, tmp1

def find_yellow(img_wl, basename, model_left, model_mid, model_right, y_leftline, y_midline, y_rightline):
    for idx, x in enumerate(xrange(1050, 1450)):
        y_left  = y_leftline[idx]
        y_mid   = y_midline[idx]
        y_right = y_rightline[idx]
        offset = int((y_right - y_mid) * 0.88)
        img_wl[x, y_right : y_right + offset, [2, 0]] = 255
    # plt.imshow(img_wl)
    # plt.show()
    cv2.imwrite("labeled_image/" + basename, img_wl)

def work(img_path):
    img = cv2.imread(img_path)
    model_left, model_mid, model_right, y_leftline, y_midline, y_rightline, img_white_labeled = find_white(img, os.path.basename(img_path))
    find_yellow(img_white_labeled, os.path.basename(img_path), model_left, model_mid, model_right, y_leftline, y_midline, y_rightline)

def main():
    for img_name in glob("../cube/*.jpg"):
        work(img_name)
    # work("../cube/7407.jpg")
if __name__ == "__main__":
    main()
