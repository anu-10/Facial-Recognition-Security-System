import os
from PyQt5.QtWidgets import QWidget, QDesktopWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5 import uic, QtWidgets
import threading
os.chdir('C:\Programming\Application')
path = 'C:\Programming\Application\Database\data.db'
import user, login, record, attendance, view, database

import cv2

Ui_Form, baseClass = uic.loadUiType('UI/control_panel_gui.ui')

class ControlPanel(QWidget):
    def __init__(self, icon, username):
        super().__init__()
        self.username = username
        self.icon = icon
        self.setWindowIcon(self.icon)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setFixedSize(1250, 1050)
        self.timer = QTimer()
        self.timer2 = QTimer()
        self.button2_state = True
        self.timer.timeout.connect(self.viewCam)
        self.timer2.timeout.connect(self.viewCam2)
        self.ui.pushButton.clicked.connect(self.controlTimer)
        self.ui.pushButton_2.clicked.connect(self.thread)
        self.ui.pushButton_3.clicked.connect(self.log_out)
        self.ui.listWidget.addItem("ID\t\tPRN")
        self.ui.listWidget.addItem("Item 1\t\t20070122019") 
        self.ui.listWidget.addItem("Item 2\t\t20070122020")
        self.ui.listWidget.addItem("Item 3\t\t20070122021")
        self.ui.listWidget.addItem("Item 4\t\t20070122022")
        self.ui.listWidget.itemClicked.connect(self.Clicked)
        self.ui.actionAdd_User_2.triggered.connect(self.add_user)
        self.ui.actionRemove_User_2.triggered.connect(self.remove_user)
        self.ui.actionManage_Records.triggered.connect(self.manage_record)
        self.ui.actionAttendance.triggered.connect(self.view_attendance)
        self.ui.actionView_Database.triggered.connect(self.view_database)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def addData(self, text):
        self.ui.listWidget.addItem(text)
    
    def removeData(self, prn):
        for i in range(self.ui.listWidget.count()):
            v = self.ui.listWidget.item(i).text()
            if prn in v:
                self.ui.listWidget.takeItem(i)
    
    def Clicked(self,item):
        prn = item.text().split('\t\t')[1]
        if prn != "PRN":
            prn = int(prn)
            v = database.search_main(path, prn)
            if v:
                QtWidgets.QMessageBox.information(self, "Record", "PRN: {}\nName: {}".format(v[0], v[1]))
            else:
                QtWidgets.QMessageBox.information(self, "Caution", "Record does not exist in Database!")
    
    def setCentralWidget(self, widget):
        self.centralwidget = widget
    
    def setStatusBar(self, bar):
        self.statusbar = bar
        
    def setMenuBar(self, bar):
        self.menuBar = bar
        
    def setMenuDatabase(self, db):
        self.menuDatabase = db
    
    def add_user(self):
        self.window_add = user.CreateUser(self.icon, self.username)
        self.window_add.show()
        
    def remove_user(self):
        self.window_remove = user.RemoveUser(self.icon, self.username)
        self.window_remove.show()
    
    def manage_record(self):
        self.window_manage = record.ManageRecord(self.icon, self.username)
        self.window_manage.show()
        
    def view_attendance(self):
        self.window_attendance = attendance.Attendance(self.icon)
        self.window_attendance.show()
    
    def view_database(self):
        self.window_view = view.ViewDatabase(self.icon)
        self.window_view.show()
        
    def log_out(self):
        self.window = login.MainWindow()
        self.window.show()
        self.close()
        
    def viewCam(self):
        ret, image = self.cap.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (750,425))
        height, width, channel = image.shape
        step = channel * width
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        self.ui.label.setPixmap(QPixmap.fromImage(qImg))
        
    def controlTimer(self):
        if not self.timer.isActive():
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.timer.start(10)
            self.ui.pushButton.setText("Stop")
        else:
            self.timer.stop()
            self.cap.release()
            self.ui.pushButton.setText("Start")
            self.ui.label.setText("Camera Switched Off")
            cv2.destroyAllWindows()
        
    def viewCam2(self):
        """while(not self.button2_state):
            try:
                frame = self.footage_socket.recv_string()
                img = base64.b64decode(frame)
                npimg = np.fromstring(img, dtype=np.uint8)
                source = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
                height, width, channel = source.shape
                step = channel * width
                qImg = QImage(source, width, height, step, QImage.Format_RGB888)
                self.ui.label_2.setPixmap(QPixmap.fromImage(qImg))
            except KeyboardInterrupt:
                cv2.destroyAllWindows()
        self.ui.label_2.setText("Camera Switched Off")"""
        url = 'http://192.168.1.34:8080/video'
        self.cap_2 = cv2.VideoCapture(url)
        while(not self.button2_state):
            ret, frame = self.cap_2.read()
            if frame is not None:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = cv2.resize(image, (750,425))
                height, width, channel = image.shape
                step = channel * width
                qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
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
