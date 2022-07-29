import cv2
import numpy as np

if __name__ == '__main__':
    base = np.zeros((10, 10, 3), dtype=np.uint8)
    base[:, :, 0] = 0 
    base[:, :, 1] = 0 
    base[:, :, 2] = 255

    for i in range(2, 8):
        for j in range(2, 8):
            base[i, j, 0] = 0
            base[i, j, 1] = 0
            base[i, j, 2] = 0
    cv2.imwrite('base_img.png', base)
    # cv2.imshow('base', base)
    # cv2.waitKey(5000) 