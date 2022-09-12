import cv2
import numpy as np
if __name__ ==  '__main__':
    size = 1000
    # size = 500
    grid = np.zeros((size, size), dtype=np.uint8)
    for i in range(0, size):
        if i % (size/10) == 0:
            grid[i, :] = 255
    for j in range(0, size):
        if j % (size/10) == 0:
            grid[:, j] = 255
    grid[size-1,:] = 255
    grid[:, size-1] = 255
    cv2.imwrite('grid_1000.png', grid)
