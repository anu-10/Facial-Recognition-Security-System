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
        def generate(df):
            self.ui.listWidget_2.addItem("ID\tPRN\tName\t\tAttendance")
            for i in range(len(df)):
                item = list(df.iloc[i])
                if type(item[2]) == str and len(item[2]) < 15:
                    self.ui.listWidget_2.addItem("{}\t{}\t{}\t\t{}".format(item[0], item[1], item[2], item[3]))
                else:
                    self.ui.listWidget_2.addItem("{}\t{}\t{}\t{}".format(item[0], item[1], item[2], item[3]))
        d = {}
        self.ui.listWidget.clear()
        self.ui.listWidget_2.clear()
        log_path = "Logs\{}\{}\{}-{}-{}.xlsx".format(date.year(),self.months[date.month()],date.day(), date.month(), date.year())
        if not os.path.exists(log_path):
            QtWidgets.QMessageBox.information(self, "ERROR", "No Record Created!")
            return
        record = pd.read_excel(log_path)
        x = QtWidgets.QListWidgetItem("Logs for {}/{}/{}".format(date.day(), date.month(), date.year()))
        x.setTextAlignment(Qt.AlignCenter)
        self.ui.listWidget.addItem(x)
        self.ui.listWidget.addItem("ID  PRN\t\tTimestamp\t\tAction")
        for i in range(len(record)):
            item = list(record.iloc[i])
            prn = int(item[1])
            time = item[2].split(":")
            action = item[3]
            if action == 'Exited':
                d[prn] = "Exited"
            elif action == 'Entered' and int(time[0]) < 9:
                d[prn] = "Entered"
            self.ui.listWidget.addItem("{}  {}\t\t{}\t\t{}".format(item[0], item[1], item[2], item[3]))
        x = QtWidgets.QListWidgetItem("Attendance for {}/{}/{}".format(date.day(), date.month(), date.year()))
        x.setTextAlignment(Qt.AlignCenter)
        self.ui.listWidget_2.addItem(x)
        attendance_path = "Attendance\{}\{}\{}-{}-{}.xlsx".format(date.year(),self.months[date.month()],date.day(), date.month(), date.year())
        if os.path.exists(attendance_path):
            record = pd.read_excel(attendance_path, index_col = None)
            generate(record)
        else:
            df = pd.DataFrame(columns = ["ID", "PRN", "NAME", "ATTENDANCE"])
            i = 1
            arr = database.view_main(self.db_path)
            d2 = {}
            for x,y in arr:
                d2 = {"ID":i, "PRN": x, "NAME": y, "ATTENDANCE": "ABSENT"}
                if x in d:
                    if d[x] == "Exited":
                        d2 = {"ID":i, "PRN": x, "NAME" : y, "ATTENDANCE": "PRESENT"}
                df = df.append(d2, ignore_index = True)
                i += 1
            df.to_excel(attendance_path, index = False)
            generate(df)
                
            
        