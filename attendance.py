import os
import database
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import *
import pandas as pd



class Attendance(QWidget):
    def __init__(self, icon, path, db_path):
        super().__init__()
        self.path = path
        self.db_path = db_path
        os.chdir(self.path)
        Ui_Attendance, baseClass = uic.loadUiType('UI/attendance.ui')
        self.ui = Ui_Attendance()
        self.ui.setupUi(self)
        self.setFixedSize(900, 800)
        self.icon = icon
        self.setWindowIcon(self.icon)
        self.ui.calendarWidget.activated.connect(lambda x: self.show_attendance(x))
        self.months = {1:'January', 2:'Feburary', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August',\
                       9:'September', 10:'October', 11:'November', 12: 'December'}
    
    def show_attendance(self, date):
        self.ui.listWidget.clear()
        self.ui.label.setText("No Record Selected")
        path = "Attendance\{}\{}\{}-{}-{}.xlsx".format(date.year(),self.months[date.month()],date.day(), date.month(), date.year())
        if not os.path.exists(path):
            QtWidgets.QMessageBox.information(self, "ERROR", "No Record Created!")
            return
        record = pd.read_excel(path)
        x = QtWidgets.QListWidgetItem("Attendance for {}/{}/{}".format(date.day(), date.month(), date.year()))
        x.setTextAlignment(Qt.AlignCenter)
        self.ui.listWidget.addItem(x)
        self.ui.listWidget.addItem("ID\tPRN\t\tTimestamp\t\tAction")
        for i in range(len(record)):
            item = list(record.iloc[i])
            item[2] = item[2].strftime("%H:%M:%S")
            self.ui.listWidget.addItem("{}\t{}\t\t{}\t\t{}".format(item[0], item[1], item[2], item[3]))
        
        self.ui.label.setText("Attendance summary for {}/{}/{}".format(date.day(), date.month(), date.year()))
        