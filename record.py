import os
os.chdir('C:\Programming\Application')
path = 'C:\Programming\Application\Database\data.db'
import database
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage, QPixmap
import cv2

Ui_Manage, baseClass = uic.loadUiType('UI/manage_record.ui')

class ManageRecord(QWidget):
    def __init__(self, icon, username):
        super().__init__()
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
        v = database.add_to_main(path, prn, name)
        if not v:
            QtWidgets.QMessageBox.information(self, "ERROR", "Record already exists in Database!")
            self.reset_add()
        else:
            QtWidgets.QMessageBox.information(self, "SUCCESS", "Record added to Database!")
            self.reset_add()
        self.ui.start.text("Start")
    
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
        v = database.user_exists(path, self.username, password)
        if not v:
            QtWidgets.QMessageBox.information(self, "ERROR", "Password is incorrect!")
        else:
            v = database.remove_from_main(path, prn)
            if not v:
                QtWidgets.QMessageBox.information(self, "ERROR", "Record does not exist in Database!")
                self.reset_remove()
            else:
                QtWidgets.QMessageBox.information(self, "SUCCESS", "Record removed from Database!")
                self.reset_remove()
    
    def reset_remove(self):
        self.ui.remove_prn.setText("")
        self.ui.password.setText("")
        
    def startRecord(self):
        ret, image = self.cap.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (700,600))
        height, width, channel = image.shape
        step = channel * width
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        self.ui.label.setPixmap(QPixmap.fromImage(qImg))

    # start/stop timer
    def controlTimer(self):
        if not self.timer.isActive():
            text = self.ui.start.text()
            if text != "Add":
                self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                self.timer.start(10)
                self.ui.start.setText("Stop")
            else:
                self.add_record()
        else:
            self.timer.stop()
            self.cap.release()
            self.ui.start.setText("Add")
            self.ui.label.setText("Camera Switched Off")
            cv2.destroyAllWindows()