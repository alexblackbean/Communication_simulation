import numpy as np
import math
import cv2
import seaborn as sns
import matplotlib.pyplot as plt
import random
def CreateRegion():
    position = np.zeros(shape = (10,10,2))
    for i in range (0,10):
        for j in range (0,10):
            position[i][j][0] = i*2.5
            position[i][j][1] = j*2.5
    return position
def CreateBase(map):
    position = np.zeros(shape = (10,10,2))
    prob_array_10 = np.array([False,False,False,False,False,False,False,False,False,True],dtype = bool)
    prob_array_4 = np.array([0,1,2,3])
    for i in range (0,10):
        for j in range (0,10):
            index = random.randint(0,9)
            if (prob_array_10[index]):
                index = random.randint(0,3)
                delta_x = 0
                delta_y = 0
                if (prob_array_4[index] == 0):# up
                    delta_y = -0.1
                elif (prob_array_4[index] == 1):# right
                    delta_x = 0.1
                elif (prob_array_4[index] == 2):# down
                    delta_y = 0.1
                elif (prob_array_4[index] == 3):# left
                    delta_x = -0.1
                position[i][j][0] = map[i][j][0] + 1.25 + delta_x
                position[i][j][1] = map[i][j][1] + 1.25 + delta_y
            else:
                position[i][j][0] = -1
                position[i][j][1] = -1
    print(position)
map = CreateRegion()
CreateBase(map)