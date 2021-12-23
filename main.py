import numpy as np
import math
import cv2
import seaborn as sns
import matplotlib.pyplot as plt
import random


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap 
from PyQt5.QtCore import QTimer
import random
threshold = 70
class Ui_Form(object):
    def setupUi(self, Form):
        scale = 50 #fps
        Form.setObjectName("Form")
        Form.resize(1020, 1020)
        self.form = Form
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 1000, 1000))
        self.label.setObjectName("label")

        self.number = 0
        self.time = 0
        self.exchange = 0

        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.add) #timer for adding car
        self.timer1.start(scale)
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.move) #timer for car moving update
        self.timer2.start(scale)
    

        self.car_number = 0
        self.car_list =[]
        self.map = self.CreateRegion()
        self.base = self.CreateBase()
        self.entry,self.exit = self.Create_Entry_Exit()
        self.corner = self.GetCorner()

        self.method = 0 # default -> Threshold

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "<html><head/><body><p><img src=\"grid_4.png\"/></p></body></html>"))
    def add(self):
        p = self.Poisson(1/12,1,1) # Poisson Distribution for arrival model
        offset = 5
        for i in range(0,36): 
            if random.random() <= p:
                self.car_number += 1
                self.dot = QtWidgets.QLabel(self.form)
                x = self.entry[i][0]*40+offset #plot coordinate x, self.entry is real initial position
                y = self.entry[i][1]*40+offset #plot coordinate y
                self.dot.setGeometry(QtCore.QRect(x, y, 10, 10))# plot behavior
                self.dot.setObjectName("dot") # objectName
                self.dot.setPixmap(QPixmap('dot.png')) #image set
                self.dot.show()# show image
                direction = i // 9
                step = 0
                is_call = False
                base_info = [-1,-1,-1,-1] # x , y , index, db
                self.car_list.append([self.dot, self.car_number, direction, self.entry[i][0], self.entry[i][1],step,is_call,base_info])
                # [0] object
                # [1] number label
                # [2] current moving direction
                # [3] x
                # [4] y
                # [5] plot supported step
                # [6] is this on call?
                # [7] selected base information [base_x,base_y,index,db]
    def move(self):
        plot_offset = 40
        self.time += 1
        p = self.Poisson(2,1,0.25) # average 2 call per hour, we focus on every 15minute == 0.25 hour
        for item in self.car_list:
            x = (item[0].x())
            y = (item[0].y())
            dir = item[2]
            if x in self.corner and y in self.corner:
                dir = self.GetDirection(dir)
            x_speed = 0
            y_speed = 0
            if dir == 0:
                x_speed = 0.02
                y_speed = 0
            elif dir == 1:
                x_speed = 0
                y_speed = 0.02
            elif dir == 2:
                x_speed = -0.02
                y_speed = 0
            else:
                x_speed = 0
                y_speed = -0.02
            item[2] = dir
            item[3] = item[3] + x_speed
            item[4] = item[4] + y_speed
            item[5] += 1
            if item[3] < 0 or item[3] > 25 or item[4] < 0 or item[4] > 25:
                item[0].setHidden(True)
                del item[0]
                del self.car_list[self.car_list.index(item)]
            if item[5] == 5:
                item[5] = 0
                item[0].setGeometry(QtCore.QRect(x+x_speed*5*plot_offset, y+y_speed*5*plot_offset, 10, 10))
            if (self.time % 900 == 0):
                if random.random() <= p:
                    if item[6] == False:
                        item[6] = True # this car calls
                        db,index = self.find_base(item[3],item[4])
                        item[7][0] = self.base[index][2]
                        item[7][1] = self.base[index][3]
                        item[7][2] = index
                        item[7][3] = db
                        # print(item[1],'is connected to ',item[7][0],item[7][1])
            if item[6] == True:
                choose = self.method
                if choose == 0:
                    car_x = item[3]
                    car_y = item[4]
                    base_x = item[7][0]
                    base_y = item[7][1]
                    index = item[7][2]
                    temp = index
                    distance = math.sqrt(abs(car_x - base_x)**2 + abs(car_y - base_y)**2)
                    db = 120 - self.PathLoss(frequency = self.base[index][4],distance=distance)
                    if db < threshold:
                        db, index = self.find_base(car_x,car_y)
                        item[7][0] = self.base[index][2]
                        item[7][1] = self.base[index][3]
                        item[7][2] = index
                        item[7][3] = db
                        if temp != index:
                            print(temp,'change to ',index)
                        self.exchange += 1
                elif choose == 1:
                    None
                elif choose == 2:
                    None
                elif choose == 3:
                    None
        # print(self.time)
        # print(self.number)
        # print(self.exchange)
    def find_base(self,car_x,car_y):
        min = 100000
        index = -1
        for i,item in enumerate(self.base):
            distance_2 = abs(car_x - item[2])**2 + abs(car_y - item[3])**2
            distance = math.sqrt(distance_2)
            frequency = item[4]
            loss = self.PathLoss(frequency=frequency,distance=distance)
            if loss <= min:
                min = loss
                index = i
        db = 120 - loss
        return db,index
            
    def CreateRegion(self):
        position = np.zeros(shape = (10,10,2))
        for i in range (0,10):
            for j in range (0,10):
                position[i][j][0] = i*2.5
                position[i][j][1] = j*2.5
        return position
    def CreateBase(self):
        position = []
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
                    x = self.map[i][j][0] + 1.25 + delta_x
                    y = self.map[i][j][1] + 1.25 + delta_y
                    frequency = random.randint(1,10)*100
                    position.append([i,j,x,y,frequency])  # [0] block_x_info 
                                            # [1] block_y_info
                                            # [2] base_x
                                            # [3] base_y 
                                            # [4] base_freq
        
        for item in position:
            base = QtWidgets.QLabel(self.form)
            base.setGeometry(QtCore.QRect(item[2]*40, item[3]*40, 20, 20))
            base.setObjectName("base")
            base.setPixmap(QPixmap('base_2.png'))
            base.show()
        return position
    def Create_Entry_Exit(self):
        entry = np.zeros(shape = (36,2))
        exit = np.zeros(shape = (40,2))
        for i in range(0,9):
            entry[i][1] = self.map[0][i+1][1]
            exit [i][1] = entry[i][1]
        for i in range(9,18):
            entry[i][0] = self.map[i-9+1][0][0]
            exit [i][0] = entry[i][0]
        for i in range(18,27):
            entry[i][1] = self.map[9][i-18+1][1]
            entry[i][0] = self.map[9][i-18+1][0] + 2.5
            exit [i][1] = entry[i][1]
            exit [i][0] = entry[i][0]
        for i in range(27,36):
            entry[i][0] = self.map[i-27+1][9][0]
            entry[i][1] = self.map[i-27+1][9][1] + 2.5
            exit [i][0] = entry[i][0]
            exit [i][1] = entry[i][1]

        exit [36][0] = self.map[0][0][0]
        exit [36][1] = self.map[0][0][1]
        exit [37][0] = self.map[9][0][0] + 2.5
        exit [37][1] = self.map[9][0][1]
        exit [38][0] = self.map[9][9][0] + 2.5
        exit [38][1] = self.map[9][9][1] + 2.5
        exit [39][0] = self.map[0][9][0]
        exit [39][1] = self.map[0][9][1] + 2.5
        return entry,exit
    def Poisson(self,lambda_i,n,t):
        p = ((lambda_i*t)**n)*(math.exp(-lambda_i*t))/(math.factorial(n))
        return p
    def PathLoss(self,frequency,distance):
        Lpf = 32.45 + 20*math.log10(frequency) + 20*math.log10(distance)
        return Lpf
    def GetCorner(self):
        corner = np.zeros(11)
        for i in range(0,11):
            corner[i] = i*100+5
        return corner
    def GetDirection(self,dir):
        rv = np.random.choice(np.arange(0, 4), p=[1/2, 7/32, 1/16, 7/32])
        if dir == 0:
            dir = dir + rv
        elif dir == 1:
            dir = (dir + rv) % 4
        elif dir == 2:
            dir = (dir + rv) % 4
        elif dir == 3:
            dir = (dir + rv) % 4
        return dir
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

