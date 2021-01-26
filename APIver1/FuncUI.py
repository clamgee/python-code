# 系統套件
import sys
# import os
# # 使用PyQt5套件
from PyQt5.uic import loadUi #使用.ui介面模組
from PyQt5.QtWidgets import QApplication,QDialog #PyQt5介面控制模組
from PyQt5 import QtCore, QtGui, QtWidgets
import json

class LoginDialog(QDialog):
    def __init__(self):
        super(LoginDialog,self).__init__()
        loadUi(r'UI/Login.ui',self)
        if self.IDPWCheck.checkState()==2:
            with open("IDPW.json",mode="r",encoding="utf-8") as file:
                data = json.load(file)
            self.LoginID.setText(data["ID"])
            self.LoginPW.setText(data["PW"])

class MessageDialog(QDialog):
    def __init__(self,gname):
        super(MessageDialog,self).__init__()
        self.setWindowTitle(gname)
        loadUi(r'UI/Message.ui',self)

if __name__ == "__main__":
    LoginApp=QApplication(sys.argv)
    SKLogin=LoginDialog()
    SKLogin.show()
    sys.exit(LoginApp.exec_())