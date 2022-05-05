import os
os.chdir('C:\Programming\Application')
path = 'C:\Programming\Application\Database\data.db'
import database
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import *
import pandas as pd

Ui_View, baseClass = uic.loadUiType('UI/view_database.ui')

class ViewDatabase(QWidget):
    def __init__(self, icon):
        super().__init__()
        self.ui = Ui_View()
        self.ui.setupUi(self)
        self.setFixedSize(500, 600)
        self.icon = icon
        self.setWindowIcon(self.icon)
        self.show_database()
    
    def show_database(self):
        self.ui.listWidget.addItem("Sr. No.\t\tPRN\t\tName")
        arr = database.view_main(path)
        i = 1
        for x in arr:
            s = "{}\t\t{}\t\t{}".format(i, x[0], x[1])
            self.ui.listWidget.addItem(s)
            i += 1
        
            
        