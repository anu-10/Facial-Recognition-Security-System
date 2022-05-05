import os
os.chdir('C:\Programming\Application')
path = 'C:\Programming\Application\Database\data.db'
import database
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget

Ui_Create, baseClass = uic.loadUiType('UI/create_user.ui')
Ui_Remove, baseClass = uic.loadUiType('UI/remove_user.ui')

class CreateUser(QWidget):
    def __init__(self, icon, username):
        super().__init__()
        self.ui = Ui_Create()
        self.ui.setupUi(self)
        self.setFixedSize(640, 500)
        self.icon = icon
        self.setWindowIcon(self.icon)
        self.ui.create.clicked.connect(self.create)
        self.ui.reset.clicked.connect(self.reset)
        self.username = username
        self.ui.new_user.setFocus()
    
    def create(self):
        name = self.ui.new_user.text()
        new_pass = self.ui.new_password.text()
        curr_pass = self.ui.current_password.text()
        if name == "" or new_pass == "" or curr_pass == "":
            QtWidgets.QMessageBox.about(self, "ERROR", "One or more fields is Empty!")
            return
        if database.user_exists(path, self.username, curr_pass):
            if(database.add_user(path, name, new_pass)):
                QtWidgets.QMessageBox.about(self, "SUCCESS", "User created successfully!")
                self.reset()
            else:
                QtWidgets.QMessageBox.about(self, "ERROR", "User already exists!")
        else:
            QtWidgets.QMessageBox.about(self, "ERROR", "Invalid password!")
    
    def reset(self):
        self.ui.new_user.setText("")
        self.ui.new_password.setText("")
        self.ui.current_password.setText("")
    
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.create()
    
class RemoveUser(QWidget):
    def __init__(self, icon, username):
        super().__init__()
        self.ui = Ui_Remove()
        self.ui.setupUi(self)
        self.setFixedSize(640, 430)
        self.icon = icon
        self.setWindowIcon(self.icon)
        self.ui.remove.clicked.connect(self.remove)
        self.ui.reset.clicked.connect(self.reset)
        self.username = username
        self.ui.username.setFocus()
    
    def remove(self):
        name = self.ui.username.text()
        pwd = self.ui.password.text()
        if name == "" or pwd == "":
            QtWidgets.QMessageBox.about(self, "ERROR", "One or more fields is Empty!")
            return
        if self.username == name:
            QtWidgets.QMessageBox.about(self, "ERROR", "Cannot remove current user!")
            return
        if database.user_exists(path, self.username, pwd):
            res = database.remove_user(path, name)
            if res == 1:
                QtWidgets.QMessageBox.about(self, "SUCCESS", "User removed successfully!")
                self.reset()
            else:
                QtWidgets.QMessageBox.about(self, "ERROR", "User does not exist!")
        else:
            QtWidgets.QMessageBox.about(self, "ERROR", "Invalid password!")
    
    def reset(self):
        self.ui.username.setText("")
        self.ui.password.setText("")
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.remove()