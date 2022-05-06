import os
import database
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage, QPixmap
import cv2
import numpy as np

class ManageRecord(QWidget):
    def __init__(self, icon, username, path, db_path):
        super().__init__()
        self.path = path
        self.db_path = db_path
        os.chdir(self.path)
        Ui_Manage, baseClass = uic.loadUiType('UI/manage_record.ui')
        self.ui = Ui_Manage()
        self.ui.setupUi(self)
        self.setFixedSize(1200, 800)
        self.icon = icon
        self.setWindowIcon(self.icon)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.startRecord)
        self.username = username
        self.ui.name.setFocus()
        self.ui.remove.clicked.connect(self.remove_record)
        self.ui.reset.clicked.connect(self.reset_add)
        self.ui.reset_2.clicked.connect(self.reset_remove)
        self.ui.start.clicked.connect(self.controlTimer)
        
    def setCentralWidget(self, widget):
        self.centralwidget = widget
    
    def setStatusBar(self, bar):
        self.statusbar = bar
        
    def setMenuBar(self, bar):
        self.menuBar = bar
        
    def setMenuDatabase(self, db):
        self.menuDatabase = db
    
    def add_record(self):
        name = self.ui.name.text()
        prn = self.ui.prn.text()
        if name == "" or prn == "":
            QtWidgets.QMessageBox.about(self, "ERROR", "One or more fields is Empty!")
            self.reset_add()
            return
        prn = int(prn)
        v = database.add_to_main(self.db_path, prn, name)
        if not v:
            QtWidgets.QMessageBox.information(self, "ERROR", "Record already exists in Database!")
            self.reset_add()
        else:
            QtWidgets.QMessageBox.information(self, "SUCCESS", "Record added to Database!")
            self.reset_add()
    
    def reset_add(self):
        self.ui.start.setText("Start")
        self.ui.name.setText("")
        self.ui.prn.setText("")
    
    def remove_record(self):
        prn = self.ui.remove_prn.text()
        password = self.ui.password.text()
        if password == "" or prn == "":
            QtWidgets.QMessageBox.about(self, "ERROR", "One or more fields is Empty!")
            return
        prn = int(prn)
        v = database.user_exists(self.db_path, self.username, password)
        if not v:
            QtWidgets.QMessageBox.information(self, "ERROR", "Password is incorrect!")
        else:
            v = database.remove_from_main(self.db_path, prn)
            if not v:
                QtWidgets.QMessageBox.information(self, "ERROR", "Record does not exist in Database!")
                self.reset_remove()
            else:
                file_path = self.path + "\data\\" + str(prn) + ".npy"
                if os.path.exists(file_path):
                    os.remove(file_path)
                QtWidgets.QMessageBox.information(self, "SUCCESS", "Record removed from Database!")
                self.reset_remove()
    
    def reset_remove(self):
        self.ui.remove_prn.setText("")
        self.ui.password.setText("")
        
    def startRecord(self):
        
        data_path = self.path + "\data\\"
        file_path = self.path + "\data\\" + self.ui.prn.text() + ".npy"
        face_cascade = cv2.CascadeClassifier(self.path + "\haarcascade_frontalface_alt.xml")
        if os.path.exists(file_path):
            QtWidgets.QMessageBox.information(self, "ERROR", "Face Data Already Exists!")
            self.timer.stop()
            self.cap.release()
            self.ui.start.setText("Start")
            self.ui.label.setText("Camera Switched Off")
            self.reset_add()
            cv2.destroyAllWindows()
            return
        skip = 0
        face_data = []

        while True:

            if skip / 10 == 40:
                break
            
            ret, frame = self.cap.read()
            if ret == False:
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            faces = face_cascade.detectMultiScale(frame, 1.3, 4)
            faces = sorted(faces, key = lambda f:f[2]*f[3], reverse = True)
            
            for (x, y, w, h) in faces:
                frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (700,600))
            height, width, channel = frame.shape
            step = channel * width
            qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
            self.ui.label.setPixmap(QPixmap.fromImage(qImg))
            
            try:
                l = faces[0]
                x, y, w, h = l
                offset = 10
                face_section = frame[y-offset:y+h+offset, x-offset:x+w+offset]
                face_section = cv2.resize(face_section, (100, 100))
                
                skip += 1
                if skip%10 ==0:
                    face_data.append(face_section)
                    print(skip/10)
                
            except:
                a=0
            finally:
                
                # cv2.imshow("bw", gray)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('e'):
                    break

        face_data=np.asarray(face_data)
        face_data = face_data.reshape((face_data.shape[0], -1))
        np.save(data_path + self.ui.prn.text() +'.npy', face_data)
        QtWidgets.QMessageBox.about(self, "SUCCESS", "Face Data Captured!")
        self.add_record()
        self.timer.stop()
        self.cap.release()
        self.ui.start.setText("Start")
        self.ui.label.setText("Camera Switched Off")
        self.reset_add()

    # start/stop timer
    def controlTimer(self):
        if not self.timer.isActive():
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.timer.start(10)
            self.ui.start.setText("Stop")
                
        else:
            self.timer.stop()
            self.cap.release()
            self.ui.start.setText("Start")
            self.ui.label.setText("Camera Switched Off")
            cv2.destroyAllWindows()