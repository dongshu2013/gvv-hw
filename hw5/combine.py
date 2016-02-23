import cv2
import numpy as np
from glob import glob

def combine_images(size):
    file_paths = glob("tmp/*.jpeg")
    file_paths.sort(key=lambda x:int(x[4:-5]))
    col_imgs = [] 
    for col_paths in zip(*[iter(file_paths)] * size[1]):
        imgs = [cv2.imread(path) for path in col_paths]
        imgs = [img[30:-30, :, :] for img in imgs]
        imgs.reverse()
        col_img = np.concatenate(imgs, axis=0)
        col_imgs.append(col_img)
    img = np.concatenate(col_imgs, axis=1)
    return img

def main():
    img = combine_images((3, 3))
    cv2.imwrite("result.jpg", img)

if __name__ == "__main__":
    main()
