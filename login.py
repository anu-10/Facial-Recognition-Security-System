# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 10:06:02 2022

@author: mural
"""
import os
from datetime import date
path = 'C:\Programming\Application'
db_path = 'C:\Programming\Application\Database\data.db'
os.chdir(path)

import sys
from PyQt5 import QtWidgets
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic, QtCore, QtGui
import database, control_panel as cp
Ui_Login, baseClass = uic.loadUiType('UI/login_gui.ui')

class MainWindow(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = QtGui.QIcon('Icon/logo.ico')
        self.setWindowIcon(self.icon)
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        self.username = ""
        self.setFixedSize(600, 500)
        self.ui.login.clicked.connect(self.login)
        self.ui.username.setFocus()
        self.ui.reset.clicked.connect(self.reset)
        self.show()
        
    def login(self):
        self.username = self.ui.username.text()
        password = self.ui.password.text()
        result = database.user_exists(db_path, self.username, password)
        if result:
            self.window = cp.ControlPanel(self.icon,self. username, path, db_path)
            self.window.show()
            self.close()
        else:
            QtWidgets.QMessageBox.about(self, "ERROR", "Invalid username or password!")
        
    def reset(self):
        self.ui.username.setText("")
        self.ui.password.setText("")
    
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.login()


if __name__ == '__main__':
    """database.create_accounts(path)
    database.add_user(path, 'Anupam', '123')"""
    year = date.today().year
    p = "Attendance\{}".format(year)
    months = ['January','Feburary', 'March', 'April', 'May', 'June', 'July', 'August',\
                   'September', 'October', 'November', 'December']
    if not os.path.exists(p):
        os.mkdir(p)
        for x in months:
            s = p + "\{}".format(x)
            os.mkdir(s)
    app = qtw.QApplication(sys.argv+[QtCore.Qt.WindowStaysOnTopHint])
    w = MainWindow()
    sys.exit(app.exec_())