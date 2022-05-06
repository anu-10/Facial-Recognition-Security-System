import os
from PyQt5.QtWidgets import QWidget, QDesktopWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5 import uic, QtWidgets
import threading
import numpy as np 
import user, login, record, attendance, view, database
import warnings
import pandas as pd
from datetime import date, datetime
warnings.filterwarnings("ignore")

import cv2



class ControlPanel(QWidget):
    def __init__(self, icon, username, path, db_path):
        super().__init__()
        self.username = username
        self.path = path
        self.db_path = db_path
        os.chdir(self.path)
        self.icon = icon
        self.setWindowIcon(self.icon)
        Ui_Form, baseClass = uic.loadUiType('UI/control_panel_gui.ui')
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setFixedSize(1600, 950)
        self.timer = QTimer()
        self.timer2 = QTimer()
        self.button_state = True
        self.button2_state = True
        self.timer.timeout.connect(self.viewCam)
        self.timer2.timeout.connect(self.viewCam2)
        self.ui.pushButton.clicked.connect(self.controlTimer)
        self.ui.pushButton_2.clicked.connect(self.thread)
        self.ui.pushButton_3.clicked.connect(self.log_out)
        self.ui.actionAdd_User_2.triggered.connect(self.add_user)
        self.ui.actionRemove_User_2.triggered.connect(self.remove_user)
        self.ui.actionManage_Records.triggered.connect(self.manage_record)
        self.ui.actionAttendance.triggered.connect(self.view_attendance)
        self.ui.actionView_Database.triggered.connect(self.view_database)
        self.load_prereq()
        self.id = 1
        self.entry_dict = {}
        self.exit_dict = {}
        self.months = {1:'January', 2:'Feburary', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August',\
                       9:'September', 10:'October', 11:'November', 12: 'December'}
        self.df = pd.DataFrame(columns=["ID","PRN", "TIMESTAMP","ACTION"])
        self.df2 = pd.DataFrame(columns = ["PRN", "ATTENDANCE"])
        self.log_path = "Logs\{}\{}\{}-{}-{}.xlsx".format(date.today().year,self.months[date.today().month],date.today().day, date.today().month, date.today().year)
        self.attendance_path = "Attendance\{}\{}\{}-{}-{}.xlsx".format(date.today().year,self.months[date.today().month],date.today().day, date.today().month, date.today().year)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    
    def setCentralWidget(self, widget):
        self.centralwidget = widget
    
    def setStatusBar(self, bar):
        self.statusbar = bar
        
    def setMenuBar(self, bar):
        self.menuBar = bar
        
    def setMenuDatabase(self, db):
        self.menuDatabase = db
    
    def add_user(self):
        self.window_add = user.CreateUser(self.icon, self.username, self.path, self.db_path)
        self.window_add.show()
        
    def remove_user(self):
        self.window_remove = user.RemoveUser(self.icon, self.username, self.path, self.db_path)
        self.window_remove.show()
    
    def manage_record(self):
        self.window_manage = record.ManageRecord(self.icon, self.username, self.path, self.db_path)
        self.window_manage.show()
        
    def view_attendance(self):
        self.window_attendance = attendance.Attendance(self.icon, self.path, self.db_path)
        self.window_attendance.show()
    
    def view_database(self):
        self.window_view = view.ViewDatabase(self.icon, self.path, self.db_path)
        self.window_view.show()
        
    def log_out(self):
        self.window = login.MainWindow()
        self.window.show()
        self.close()
    
    def reset_elements(self):
        self.id = 1
        self.entry_dict = {}
        self.exit_dict = {}
    
    
    def knn(self, train, test, k=5):
        def distance(v1, v2):
            # Eucledian 
            return np.sqrt(((v1-v2)**2).sum())
        dist = []
    
        for i in range(train.shape[0]):
            # Get the vector and label
            ix = train[i, :-1]
            iy = train[i, -1]
            # Compute the distance from test point
            d = distance(test, ix)
            dist.append([d, iy])
        # Sort based on distance and get top k
        dk = sorted(dist, key=lambda x: x[0])[:k]
        # Retrieve only the labels
        labels = np.array(dk)[:, -1]
        
        # Get frequencies of each label
        output = np.unique(labels, return_counts=True)
        # Find max frequency and corresponding label
        index = np.argmax(output[1])
        return output[0][index]
    
    def load_prereq(self):
        self.face_cascade = cv2.CascadeClassifier(r"C:\Programming\Application\haarcascade_frontalface_alt.xml")
        skip = 0
        dataset_path = './data/'

        face_data = [] 
        labels = []

        class_id = 0 # Labels for the given file
        self.prn = {} #Mapping btw id - name
        # Data Preparation
        for filename in os.listdir(dataset_path):
            if filename.endswith('.npy'):
                #Create a mapping btw class_id and name
                self.prn[class_id] = filename[:-4]
                print("Loaded "+filename)
                data_item = np.load(dataset_path+filename)
                face_data.append(data_item)

                #Create Labels for the class
                target = class_id*np.ones((data_item.shape[0],))
                class_id += 1
                labels.append(target)

        face_dataset = np.concatenate(face_data,axis=0)
        face_labels = np.concatenate(labels,axis=0).reshape((-1,1))

        print(face_dataset.shape)
        print(face_labels.shape)

        self.trainset = np.concatenate((face_dataset,face_labels),axis=1)
        print(self.trainset.shape)
        
    
    
        
    def viewCam(self):

        ret, frame = self.cap.read()
        faces = self.face_cascade.detectMultiScale(frame,1.3,5)
        if(len(faces)!=0):
            for face in faces:
                x,y,w,h = face
        
                #Get the face ROI
                offset = 10
                face_section = frame[y-offset:y+h+offset,x-offset:x+w+offset]
                face_section = cv2.resize(face_section,(100,100))
        
                #Predicted Label (out)
                out = self.knn(self.trainset,face_section.flatten())
                
                #Display on the screen the name and rectangle around it
                pred_prn = self.prn[int(out)]
                time = datetime.now()
                current_time = time.strftime("%H:%M:%S")
                new_row = {"ID":self.id, "PRN":pred_prn, "TIMESTAMP":current_time,"ACTION":'Entered'}
                if pred_prn not in self.entry_dict:
                    self.entry_dict[pred_prn] = 1
                    self.df = self.df.append(new_row, ignore_index = True)
                    self.id += 1
                elif pred_prn in self.exit_dict:
                    if self.entry_dict[pred_prn] <= self.exit_dict[pred_prn]:
                        self.entry_dict[pred_prn] += 1
                        self.df = self.df.append(new_row, ignore_index = True)
                        self.id += 1
                        
                        
                frame = cv2.putText(frame,pred_prn,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
                frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (750,750))
        height, width, channel = frame.shape
        step = channel * width
        qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        self.ui.label.setPixmap(QPixmap.fromImage(qImg))
        
    def controlTimer(self):
        if not self.timer.isActive():
            self.button_state = True
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.timer.start(10)
            self.ui.pushButton.setText("Stop")
        else:
            self.timer.stop()
            self.cap.release()
            self.button_state = False
            self.ui.pushButton.setText("Start")
            self.ui.label.setText("Camera Switched Off")
            print(self.entry_dict)
            print(self.df)
            self.df.to_excel(self.log_path, index = False)
            cv2.destroyAllWindows()
        
    def viewCam2(self):
        url = 'http://192.168.1.36:8080/video'
        self.cap_2 = cv2.VideoCapture(url)
        # Testing 
        count = 0
        final_prn = []
        
        while(not self.button2_state):
            ret, frame = self.cap_2.read()
            if ret == False:
                continue

            faces = self.face_cascade.detectMultiScale(frame,1.3,5)
            if(len(faces)!=0):
                for face in faces:
                    x,y,w,h = face
    
                    #Get the face ROI
                    offset = 10
                    face_section = frame[y-offset:y+h+offset,x-offset:x+w+offset]
                    face_section = cv2.resize(face_section,(100,100))
    
                    #Predicted Label (out)
                    out = self.knn(self.trainset,face_section.flatten())
    
                    #Display on the screen the name and rectangle around it
                    pred_prn = self.prn[int(out)]
                    time = datetime.now()
                    current_time = time.strftime("%H:%M:%S")
                    new_row = {"ID":self.id, "PRN":pred_prn, "TIMESTAMP":current_time,"ACTION":'Exited'}
                    if pred_prn not in self.exit_dict:
                        self.exit_dict[pred_prn] = 1
                        self.df = self.df.append(new_row, ignore_index = True)
                        self.id += 1
                    elif pred_prn in self.entry_dict:
                        if self.exit_dict[pred_prn] <= self.entry_dict[pred_prn]:
                            self.exit_dict[pred_prn] += 1
                            self.df = self.df.append(new_row, ignore_index = True)
                            self.id += 1
                    frame = cv2.putText(frame,pred_prn,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
                    frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (750,750))
            height, width, channel = frame.shape
            step = channel * width
            qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
            self.ui.label_2.setPixmap(QPixmap.fromImage(qImg))
        self.ui.label_2.setText("Camera Switched Off")
        
        
    def thread(self):
        if self.button2_state:
            self.button2_state = False
            self.ui.pushButton_2.setText("Stop")
            self.t=threading.Thread(target=self.viewCam2)
            self.t.start()
        else:
            self.button2_state = True
            self.ui.pushButton_2.setText("Start")
            self.ui.label_2.setText("Camera Switched Off")
            cv2.destroyAllWindows()
