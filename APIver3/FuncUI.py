# 系統套件
import sys
# import os
# # 使用PySide6套件
from PySide6.QtUiTools import QUiLoader #使用 .ui介面模組
from PySide6.QtWidgets import QApplication,QDialog #PySide6介面控制模組
from PySide6 import QtCore, QtGui, QtWidgets
import json

class LoginDialog(QtCore.QObject):
    def __init__(self):
        self.UiFile = QtCore.QFile('UI/Login.ui')
        Loader = QUiLoader()
        self.UiFile.open(QtCore.QFile.ReadOnly)
        DialogUi=Loader.load(self.UiFile)
        self.UiFile.close()
        self.ui = DialogUi
        if self.ui.IDPWCheck.checkState()==2:
            with open("IDPW.json",mode="r",encoding="utf-8") as file:
                data = json.load(file)
            self.ui.LoginID.setText(data["ID"])
            self.ui.LoginPW.setText(data["PW"])

# class MessageDialog(QDialog):
#     def __init__(self,gname):
#         super(MessageDialog,self).__init__()
#         self.setWindowTitle(gname)
#         loadUi(r'UI/Message.ui',self)

if __name__ == "__main__":
    LoginApp=QApplication(sys.argv)
    SKLogin=LoginDialog()
    SKLogin.ui.show()
    sys.exit(LoginApp.exec_())