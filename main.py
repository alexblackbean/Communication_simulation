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
scale = 50 #fps
class Ui_Form(object):
    def setupUi(self, Form):
        
        Form.setObjectName("Form")
        Form.resize(1520, 1020)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(1020, 10, 480, 1000))
        self.groupBox.setFont(font)

        

        self.label_car = QtWidgets.QLabel(self.groupBox)
        self.label_car.setFont(font)
        self.label_car.setGeometry(QtCore.QRect(10, 210, 480, 30))
        self.label_car.setText('Current car number: ')

        self.start = QtWidgets.QPushButton(self.groupBox)
        self.start.setFont(font)
        self.start.setGeometry(QtCore.QRect(10, 70, 200, 100))
        self.start.setText('Start')
        self.start.clicked.connect(self.TimerHandler)

        self.fps = QtWidgets.QTextEdit(self.groupBox)
        self.fps.setText('input fps')
        self.fps.setGeometry(QtCore.QRect(250, 70, 150, 45))

        self.way = QtWidgets.QTextEdit(self.groupBox)
        self.way.setText('input methods')
        self.way.setGeometry(QtCore.QRect(250, 140, 200, 45))

        self.label_threshold_ex = QtWidgets.QLabel(self.groupBox)
        self.label_threshold_ex.setFont(font)
        self.label_threshold_ex.setGeometry(QtCore.QRect(10, 310, 480, 30))
        self.label_threshold_ex.setText('Number of handoff (threshold): ')
        
        self.label_best_ex = QtWidgets.QLabel(self.groupBox)
        self.label_best_ex.setFont(font)
        self.label_best_ex.setGeometry(QtCore.QRect(10, 410, 480, 30))
        self.label_best_ex.setText('Number of handoff (Best effort): ')
        
        self.label_entropy_ex = QtWidgets.QLabel(self.groupBox)
        self.label_entropy_ex.setFont(font)
        self.label_entropy_ex.setGeometry(QtCore.QRect(10, 510, 480, 30))
        self.label_entropy_ex.setText('Number of handoff (Entropy): ')
        

        self.form = Form
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 1000, 1000))
        self.label.setObjectName("label")

        self.number = 0
        self.time = 0
        self.exchange = 0
        self.threshold_ex = 0
        self.best_ex = 0
        self.entropy_ex = 0
        self.method1 = 0


        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.add) #timer for adding car
        
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.move) #timer for car moving update
        
    

        self.car_number = 0
        self.car_list =[]
        self.map = self.CreateRegion()
        self.base = self.CreateBase()
        self.entry,self.exit = self.Create_Entry_Exit()
        self.corner = self.GetCorner()

        self.method = 0 # default -> Threshold

        self.label_car_number = QtWidgets.QLabel(self.groupBox)
        self.label_car_number.setFont(font)
        self.label_car_number.setGeometry(QtCore.QRect(250, 210, 100, 30))
        self.label_car_number.setNum(0)

        self.label_thres_number = QtWidgets.QLabel(self.groupBox)
        self.label_thres_number.setFont(font)
        self.label_thres_number.setGeometry(QtCore.QRect(400, 310, 100, 30))
        self.label_thres_number.setNum(0)

        self.label_best_number = QtWidgets.QLabel(self.groupBox)
        self.label_best_number.setFont(font)
        self.label_best_number.setGeometry(QtCore.QRect(400, 410, 100, 30))
        self.label_best_number.setNum(0)

        self.label_entropy_number = QtWidgets.QLabel(self.groupBox)
        self.label_entropy_number.setFont(font)
        self.label_entropy_number.setGeometry(QtCore.QRect(400, 510, 100, 30))
        self.label_entropy_number.setNum(0)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "<html><head/><body><p><img src=\"grid_4.png\"/></p></body></html>"))
        self.groupBox.setTitle(_translate("Form", "Details"))
    def TimerHandler(self):
        value = self.fps.toPlainText()
        scale = int(value)
        self.method = int(self.way.toPlainText())
        self.timer1.start(scale)
        self.timer2.start(scale)
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
                base_info = [-1,-1,-1,-1,-1,-1] # x , y , index, db, call time, current time
                self.car_list.append([self.dot, self.car_number, direction,
                                     self.entry[i][0], self.entry[i][1],
                                     step,is_call,base_info])
                # [0] object
                # [1] number label
                # [2] current moving direction
                # [3] x
                # [4] y
                # [5] plot supported step
                # [6] is this on call?
                # [7] selected base information [base_x,base_y,index,db,call time, current time]
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
            
            if item[6] == True: # call time and current call time
                item[7][5] += 1
                if item[7][5] == item[7][4]:
                    item[6] == False
                    item[7][4] = 0
                    item[7][5] = 0
            if self.time % 900 == 0:
                if random.random() <= p and item[6] == False: # may call second times when timeexpire == 15min
                        item[6] = True # this car calls
                        time = np.random.normal(loc= 3, scale= 0.5)
                        db,index = self.find_base(item[3],item[4])
                        item[7][0] = self.base[index][2]
                        item[7][1] = self.base[index][3]
                        item[7][2] = index
                        item[7][3] = db
                        item[7][4] = int(time*60)
            if item[6] == True:
                if self.method == 0:
                    self.threshold_ex += self.threshold_method(item)
                elif self.method == 1:
                    self.best_ex += self.Best_effort(item)
                elif self.method == 2:
                    self.entropy_ex += self.Entropy(item)
                
        # print(self.time)
        self.label_car_number.setNum(len(self.car_list))
        self.label_thres_number.setNum(self.threshold_ex)
        self.label_best_number.setNum(self.best_ex)
        self.label_entropy_number.setNum(self.entropy_ex)
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
    def threshold_method(self,item):
        car_x = item[3]
        car_y = item[4]
        base_x = item[7][0]
        base_y = item[7][1]
        index = item[7][2]
        distance = math.sqrt(abs(car_x - base_x)**2 + abs(car_y - base_y)**2)
        db = 120 - self.PathLoss(frequency = self.base[index][4],distance=distance)
        if db < threshold:
            db, new_index = self.find_base(car_x,car_y)
            if new_index != index:
                item[7][0] = self.base[new_index][2]
                item[7][1] = self.base[new_index][3]
                item[7][2] = new_index
                item[7][3] = db
                return 1
            return 0
    def Best_effort(self,item):
        car_x = item[3]
        car_y = item[4]
        index = item[7][2]
        max = -1
        new_index = -1
        for i,base in enumerate(self.base):
            distance = math.sqrt(abs(car_x - base[2])**2 + abs(car_y - base[3])**2)
            db = 120 - self.PathLoss(base[4],distance)
            if db > max:
                max = db
                new_index = i
        if new_index != index:
            item[7][0] = self.base[new_index][2]
            item[7][1] = self.base[new_index][3]
            item[7][2] = new_index
            item[7][3] = max
            return 1
        return 0
    def Entropy(self,item):
        car_x = item[3]
        car_y = item[4]
        base_x = item[7][0]
        base_y = item[7][1]
        index = item[7][2]
        distance = math.sqrt(abs(car_x - base_x)**2 + abs(car_y - base_y)**2)
        loss = self.PathLoss(frequency = self.base[index][4],distance=distance)
        diff = -1
        new_index = -1
        for i,base in enumerate(self.base):
            if i != index:
                distance = math.sqrt(abs(car_x - base[2])**2 + abs(car_y - base[3])**2)
                loss_2 = self.PathLoss(frequency = base[4],distance=distance)
                diff = loss - loss_2
                if diff > 25:
                    item[7][0] = self.base[i][2]
                    item[7][1] = self.base[i][3]
                    item[7][2] = i
                    item[7][3] = 120 - loss_2
                    return 1
        return 0
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

