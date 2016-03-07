#Author: Qinglin Li, Net ID: qlt073
import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob

def bgr2hsv(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

def get_train_samples(transform=None):
    samples = []
    for file_path in glob.glob("train/*"):
        img_train = cv2.imread(file_path)
        if transform:
            img_train = transform(img_train)
        samples.append(img_train)
    return samples

class HistSeg:
    def __init__(self, channel1, channel2):
        self.channel1 = channel1
        self.channel2 = channel2
        self.hist = None

    def train(self, samples):
        hist = np.zeros((256, 256), dtype=np.float)
        cnt = 0
        for img in samples:
            tmp = 1.0 / img.size
            for i in xrange(img.shape[0]):
                for j in xrange(img.shape[1]):
                    chs = img[i, j]
                    ch1, ch2 = chs[self.channel1], chs[self.channel2]
                    hist[ch1, ch2] += tmp
        self.hist = hist / len(samples)

    def test(self, img, threshold=1e-4):
        chs = cv2.split(img)
        ch1, ch2 = chs[self.channel1], chs[self.channel2]
        return self.hist[ch1, ch2] > threshold

class GaussianSeg:
    def __init__(self, channel1, channel2):
        self.channel1 = channel1
        self.channel2 = channel2

    def train(self, samples):
        samples = [x.reshape((-1, 3)) for x in samples]
        data = np.concatenate(samples, axis=0)[:, (self.channel1, self.channel2)]
        self.mean = np.mean(data, axis=0)
        self.cov = np.cov(data, rowvar=0)
        self.icov = np.linalg.inv(self.cov)
        # print self.mean 
        # print np.linalg.inv(self.cov)

    def test(self, img, threshold=0):
        v_img = img.reshape(-1, 3)[:, [self.channel1, self.channel2]]
        v_diff = v_img - self.mean
        t = np.sum(np.dot(v_diff, self.icov) * v_diff, axis=1)
        return (t < threshold).reshape(img.shape[:2]) 

def work(img_name, img_test, channel1, channel2, transform=bgr2hsv, Seg=HistSeg, threshold=0):
    samples = get_train_samples(transform) 
    seg = Seg(channel1, channel2)
    seg.train(samples)
    tmp = img_test.copy()
    img_test = transform(img_test)
    mask = seg.test(img_test, threshold)
    plt.imshow(mask, cmap="gray")
    plt.show()
    tmp[np.logical_not(mask)] = 255
    plt.imshow(cv2.cvtColor(tmp, cv2.COLOR_BGR2RGB))
    if transform:
        color_space_name = transform.__name__.split("2")[1]
    else:
        color_space_name = "rgb"
    print color_space_name
    title = seg.__class__.__name__ + "_" + color_space_name
    plt.title(title)
    plt.show()
    cv2.imwrite("results/%s_%s.jpg" % (img_name, title), tmp)

def main():
    img_test = cv2.imread("7350.jpg")
    work("gun1", img_test, 0, 1, transform=bgr2hsv, Seg=HistSeg, threshold=10)
    work("gun1", img_test, 0, 1, transform=bgr2hsv, Seg=GaussianSeg, threshold=10)

if __name__ == "__main__":
    main()
