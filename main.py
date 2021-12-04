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
    # print(position)
def Create_Entry_Exit(map):
    entry = np.zeros(shape = (36,2))
    exit = np.zeros(shape = (40,2))
    for i in range(0,9):
        entry[i][1] = map[0][i+1][1]
        exit [i][1] = entry[i][1]
    for i in range(9,18):
        entry[i][0] = map[i-9+1][0][0]
        exit [i][0] = entry[i][0]
    for i in range(18,27):
        entry[i][1] = map[9][i-18+1][1]
        entry[i][0] = map[9][i-18+1][0] + 2.5
        exit [i][1] = entry[i][1]
        exit [i][0] = entry[i][0]
    for i in range(27,36):
        entry[i][0] = map[i-27+1][9][0]
        entry[i][1] = map[i-27+1][9][1] + 2.5
        exit [i][0] = entry[i][0]
        exit [i][1] = entry[i][1]

    exit [36][0] = map[0][0][0]
    exit [36][1] = map[0][0][1]
    exit [37][0] = map[9][0][0] + 2.5
    exit [37][1] = map[9][0][1]
    exit [38][0] = map[9][9][0] + 2.5
    exit [38][1] = map[9][9][1] + 2.5
    exit [39][0] = map[0][9][0]
    exit [39][1] = map[0][9][1] + 2.5
    return entry,exit

map = CreateRegion()
CreateBase(map)
entry,exit = Create_Entry_Exit(map)