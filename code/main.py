'''Using PyQt5 to create a GUI for the user to interact with the program'''
# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtGui import QPixmap 
# from PyQt5.QtCore import QTimer, QRect
# from PyQt5.QtWidgets import QLabel
'''Using PyQt6 to create a GUI for the user to interact with the program'''
from re import I
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer, QRect
from PyQt6.QtWidgets import QLabel
'''Importing the other files'''
import numpy as np
import math
import cv2
import matplotlib.pyplot as plt
import random

scale_map = 20
threshold = 20
scale = 50 #fps
class Ui_Form(object):
    font = QtGui.QFont()
    font.setFamily("Times New Roman")
    font.setPointSize(16)

    text_base_x = 10
    text_base_y = 70

    button_base_x = 10
    button_base_y = 170
    def object_initialize(self, Form):
       
        self.control_panel = QtWidgets.QGroupBox(Form)
        self.control_panel.setGeometry(QtCore.QRect(520, 10, 480, 500))
        self.control_panel.setFont(self.font)
        self.control_panel.setStyleSheet("background-color: ")

        '''Button setup region'''
        self.start = QtWidgets.QPushButton(self.control_panel)
        self.start.setFont(self.font)
        self.start.setGeometry(QtCore.QRect(self.button_base_x, self.button_base_y, 150, 50))
        self.start.setText('Start')
        self.start.clicked.connect(self.TimerHandler)

        self.stop = QtWidgets.QPushButton(self.control_panel)
        self.stop.setFont(self.font)
        self.stop.setGeometry(QtCore.QRect(self.button_base_x, self.button_base_y + 60, 150, 50))
        self.stop.setText('Stop')
        self.stop.clicked.connect(self.stopTimer)

        self.reset = QtWidgets.QPushButton(self.control_panel)
        self.reset.setFont(self.font)
        self.reset.setGeometry(QtCore.QRect(self.button_base_x, self.button_base_y + 120, 150, 50))
        self.reset.setText('reset')
        self.reset.clicked.connect(self.Reset)
        '''End of button setup region'''

        '''Text setup region'''
        self.control_title = QLabel(self.control_panel)
        self.control_title.setText("Control Panel")
        self.control_title.setStyleSheet("background-color: rgba(0, 0, 0, 80)")
        self.control_title.setGeometry(QRect(15, 10, 450, 30))
        self.control_title.setFont(QtGui.QFont("Times New Roman", 28)) 
        self.control_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.debug_terminal = QtWidgets.QTextBrowser(self.control_panel)
        self.debug_terminal.setGeometry(QRect(10, 350, 460, 190))
        # self.debug_terminal.setStyleSheet("{background-color: rgba(255, 255 , 255, 100%);ck;}")

        self.fps_label = QtWidgets.QLabel(self.control_panel)
        self.fps_label.setText("input fps")
        self.fps_label.setGeometry(QtCore.QRect(self.text_base_x, self.text_base_y - 25, 150, 25))

        self.fps = QtWidgets.QTextEdit(self.control_panel)
        self.fps.setText('100')
        self.fps.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.fps.setGeometry(QtCore.QRect(self.text_base_x, self.text_base_y, 150, 25))

        self.way_label = QtWidgets.QLabel(self.control_panel)
        self.way_label.setText("input method 0 ~ 3")
        self.way_label.setGeometry(QtCore.QRect(self.text_base_x, self.text_base_y + 25, 150, 25))

        self.way = QtWidgets.QTextEdit(self.control_panel)
        self.way.setText('method 0')
        self.way.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.way.setGeometry(QtCore.QRect(self.text_base_x, self.text_base_y + 50, 150, 25))



        self.label_car = QtWidgets.QLabel(self.control_panel)
        self.label_car.setFont(self.font)
        self.label_car.setGeometry(QtCore.QRect(self.text_base_x + 180, self.text_base_y, 200, 30))
        self.label_car.setText('Current car number: ')

        self.label_threshold_ex = QtWidgets.QLabel(self.control_panel)
        self.label_threshold_ex.setFont(self.font)
        self.label_threshold_ex.setGeometry(QtCore.QRect(self.text_base_x + 180, self.text_base_y + 40, 480, 30))
        self.label_threshold_ex.setText('Number of handoff (threshold): ')

        self.label_best_ex = QtWidgets.QLabel(self.control_panel)
        self.label_best_ex.setFont(self.font)
        self.label_best_ex.setGeometry(QtCore.QRect(self.text_base_x + 180, self.text_base_y + 80, 480, 30))
        self.label_best_ex.setText('Number of handoff (Best effort): ')
 
        self.label_entropy_ex = QtWidgets.QLabel(self.control_panel)
        self.label_entropy_ex.setFont(self.font)
        self.label_entropy_ex.setGeometry(QtCore.QRect(self.text_base_x + 180, self.text_base_y + 120, 480, 30))
        self.label_entropy_ex.setText('Number of handoff (Entropy): ')
 
        self.label_entropy_ex = QtWidgets.QLabel(self.control_panel)
        self.label_entropy_ex.setFont(self.font)
        self.label_entropy_ex.setGeometry(QtCore.QRect(self.text_base_x + 180, self.text_base_y + 160, 480, 30))
        self.label_entropy_ex.setText('Number of handoff (own method): ')

        self.label_time = QtWidgets.QLabel(self.control_panel)
        self.label_time.setFont(self.font)
        self.label_time.setGeometry(QtCore.QRect(self.text_base_x + 180, self.text_base_y + 200, 480, 30))
        self.label_time.setText('Currently Passing Time: ')

        self.label_call = QtWidgets.QLabel(self.control_panel)
        self.label_call.setFont(self.font)
        self.label_call.setGeometry(QtCore.QRect(self.text_base_x + 180, self.text_base_y + 240, 480, 30))
        self.label_call.setText('Current Call: ')
        '''End of text setup region'''

        '''Image label setup region'''
        self.map_img = QLabel(Form)
        self.map_img.setPixmap(QPixmap("../image/grid_500.png")) 
        self.map_img.setGeometry(QRect(10, 10, 500, 500))
        '''End of image label setup region'''
        
        '''Item setup region'''
        self.number = 0
        self.time = 0
        self.exchange = 0
        self.threshold_ex = 0
        self.best_ex = 0
        self.entropy_ex = 0
        self.method1 = 0

        self.call = 0
        self.car_number = 0
        self.car_list =[]
        self.form = Form
        

        self.method = 0 # default -> Threshold

        
        self.map = self.CreateRegion()
        self.base = self.CreateBase()
        self.entry,self.exit = self.Create_Entry_Exit()
        self.corner = self.GetCorner()

        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.add) #timer for adding car

        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.move) #timer for car moving update


        self.label_car_number = QtWidgets.QLabel(self.control_panel)
        self.label_car_number.setFont(self.font)
        self.label_car_number.setGeometry(QtCore.QRect(450, 70, 100, 30))
        self.label_car_number.setNum(0)

        self.label_thres_number = QtWidgets.QLabel(self.control_panel)
        self.label_thres_number.setFont(self.font)
        self.label_thres_number.setGeometry(QtCore.QRect(450, 110, 100, 30))
        self.label_thres_number.setNum(0)

        self.label_best_number = QtWidgets.QLabel(self.control_panel)
        self.label_best_number.setFont(self.font)
        self.label_best_number.setGeometry(QtCore.QRect(450, 150, 100, 30))
        self.label_best_number.setNum(0)

        self.label_entropy_number = QtWidgets.QLabel(self.control_panel)
        self.label_entropy_number.setFont(self.font)
        self.label_entropy_number.setGeometry(QtCore.QRect(450, 190, 100, 30))
        self.label_entropy_number.setNum(0)

        self.label_own_number = QtWidgets.QLabel(self.control_panel)
        self.label_own_number.setFont(self.font)
        self.label_own_number.setGeometry(QtCore.QRect(450, 230, 100, 30))
        self.label_own_number.setNum(0)

        self.label_time_number = QtWidgets.QLabel(self.control_panel)
        self.label_time_number.setFont(self.font)
        self.label_time_number.setGeometry(QtCore.QRect(450, 270, 100, 30))
        self.label_time_number.setNum(self.time)

        self.label_call_number = QtWidgets.QLabel(self.control_panel)
        self.label_call_number.setFont(self.font)
        self.label_call_number.setGeometry(QtCore.QRect(450, 310, 100, 30))
        self.label_call_number.setNum(self.call)
        '''End of item setup region'''

        pass
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
                    delta_x = 0; delta_y = 0
                    if (prob_array_4[index] == 0):# up offset
                        delta_y = -0.1
                    elif (prob_array_4[index] == 1):# right offset
                        delta_x = 0.1
                    elif (prob_array_4[index] == 2):# down offset
                        delta_y = 0.1 
                    elif (prob_array_4[index] == 3):# left offset
                        delta_x = -0.1
                    x = self.map[i][j][0] + 1.25 + delta_x # 1.25 is to the center of the square
                    y = self.map[i][j][1] + 1.25 + delta_y
                    frequency = random.randint(1,10)*100
                    poll  = 0
                    position.append([i, j, x, y, frequency, poll])  # [0] block_x_info 
                                            # [1] block_y_info
                                            # [2] base_x
                                            # [3] base_y 
                                            # [4] base_freq
                                            # [5] poll
        for item in position:
            base = QtWidgets.QLabel(self.form)
            base.setGeometry(QtCore.QRect(int(item[2]*20), int(item[3]*20), 10, 10)) # 20 is scale of the map, 20 = 50 (a block of map) // 2.5(real world block distance)
            base.setObjectName("base")
            self.debug_terminal.append("base is added at x={}, y={}".format(item[2], item[3]))
            # self.debug_terminal.append("base is added at")
            base.setPixmap(QPixmap('../image/base_img.png'))
            base.show()
        return position

    def add(self):
        p = self.Poisson(1/12,1,1) # Poisson Distribution for arrival model
        offset = 5
        for i in range(0,36): 
            if random.random() <= p:
                self.car_number += 1
                
                self.dot = QtWidgets.QLabel(self.form)
                x = self.entry[i][0]*scale_map+offset+3 #plot coordinate x, self.entry is real initial position
                y = self.entry[i][1]*scale_map+offset #plot coordinate y
                self.dot.setGeometry(QtCore.QRect(int(x), int(y), 5, 5))# plot behavior
                self.dot.setObjectName("dot") # objectName
                self.dot.setPixmap(QPixmap('../image/dot.png')) #image set
                
                self.dot.show()# show image
                direction = i // 9
                step = 0
                is_call = False
                base_info = [-1,-1,-1,-1,-1,-1] # x , y , index, db, call time, current time
                corner_step = 0
                self.car_list.append([self.dot, self.car_number, direction,
                                     self.entry[i][0], self.entry[i][1],
                                     step,is_call,base_info,corner_step])
                # [0] object
                # [1] number label
                # [2] current moving direction
                # [3] x
                # [4] y
                # [5] plot supported step
                # [6] is this on call?
                # [7] selected base information [base_x,base_y,index,db,call time, current time]
                # [8] corner step
    def move(self):
        self.time += 1
        if self.time == 10000:
            self.stopTimer()
        self.label_time_number.setNum(self.time)
        p = self.Poisson(2,1,0.5) # average 2 call per hour, we focus on every 15minute == 0.25 hour
        for item in self.car_list:
            x = (item[0].x())
            y = (item[0].y())
            # modify
            x = x - 3 # offset
            dir = item[2]
            if x in self.corner and y in self.corner:
                dir = self.GetDirection(dir)
            x = x + 3
            # 72 km/hr = 0.02 km/s
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
            item[5] += 1 # support plot step
            item[8] += 1 # corner step 
            if item[3] < 0 or item[3] > 25 or item[4] < 0 or item[4] > 25:
                item[0].setHidden(True)
                del item[0]
                del self.car_list[self.car_list.index(item)]
            if item[5] == 5:
                item[5] = 0
                item[0].setGeometry(QtCore.QRect(int(x+x_speed*5*10), int(y+y_speed*5*10), 10, 10))
            
            if item[6] == True: # call time and current call time
                item[7][5] += 1
                if item[7][5] == item[7][4]:
                    self.call -= 1
                    item[6] == False
                    item[7][4] = 0
                    item[7][5] = 0
            # call release
            if self.time % 1800 == 0:
                if random.random() <= p and item[6] == False: # may call second times when timeexpire == 15min
                        item[6] = True # this car calls
                        self.call += 1
                        time = np.random.normal(loc= 3, scale= 0.5)
                        db,index = self.find_base(item[3],item[4])
                        item[7][0] = self.base[index][2]
                        item[7][1] = self.base[index][3]
                        item[7][2] = index
                        item[7][3] = db
                        item[7][4] = int(time*60)
            if item[6] == True:
                if self.method == "method 0":
                    self.threshold_ex += self.threshold_method(item)
                elif self.method == "method 1":
                    self.best_ex += self.Best_effort(item)
                elif self.method == "method 2":
                    self.entropy_ex += self.Entropy(item)
                elif self.method == "method 3":
                    self.method1 += self.ownMethod(item)
        self.label_car_number.setNum(len(self.car_list))
        self.label_thres_number.setNum(self.threshold_ex)
        self.label_best_number.setNum(self.best_ex)
        self.label_entropy_number.setNum(self.entropy_ex)
        self.label_own_number.setNum(self.method1)
   

    def TimerHandler(self):
        value = self.fps.toPlainText()
        scale = int(value)
        self.method = self.way.toPlainText()
        self.timer1.start(scale)
        self.timer2.start(scale)
    def stopTimer(self):
        self.timer1.stop()
        self.timer2.stop()
    def Reset(self):
        counter_temp = 0
        self.timer1.stop()
        self.timer2.stop()

        for i in range(0, len(self.car_list)):
            (self.car_list[i])[0].setHidden(True)
            del (self.car_list[i])[0]
        del self.car_list
        self.car_list = []

        self.label_car_number.setNum(len(self.car_list))
        self.label_thres_number.setNum(0)
        self.label_best_number.setNum(0)
        self.label_entropy_number.setNum(0)
        self.label_own_number.setNum(0)
        self.label_time_number.setNum(0)

        self.threshold_ex = 0
        self.best_ex = 0
        self.entropy_ex = 0
        self.method1 = 0
        self.call = 0
        self.time = 0
    
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
        print("hi")
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
    def ownMethod(self,item):
        car_x = item[3]
        car_y = item[4]
        index = item[7][2]
        db = item[7][3]
        new_db = 0
        if item[8] % 125 == 0:
            for i,base in enumerate(self.base):
                if i != index:
                    distance = math.sqrt(abs(car_x - base[2])**2 + abs(car_y - base[3])**2)
                    loss = self.PathLoss(base[4],distance)
                    new_db = 120 - loss
                    if new_db - db > 0:
                        base[5] += 1
                    elif new_db - db == 0:
                        base[5] += 1
                    else:
                        base[5] -= 1
                if item[8] == 250:
                    item[8] = 0
                    if base[5] >= 1:
                        item[7][0] = self.base[i][2]
                        item[7][1] = self.base[i][3]
                        item[7][2] = i
                        item[7][3] = 120 - loss
                        for base in self.base:
                            base[5] = 0
                        return 1
            for base in self.base:
                base[5] = 0
        return 0

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    Form.setWindowTitle("Communication Simulator")
    Form.resize(1020, 520)
    ui = Ui_Form()
    ui.object_initialize(Form)
    # ui.setupUi(Form)
    Form.show()
    # sys.exit(app.exec_()) PyQt5
    sys.exit(app.exec())

