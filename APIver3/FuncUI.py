# 系統套件
import sys
# import os
# # 使用PySide6套件
from PySide6.QtUiTools import QUiLoader #使用 .LoginUI介面模組
from PySide6.QtWidgets import QApplication,QDialog #PySide6介面控制模組
from PySide6 import QtCore, QtGui, QtWidgets
import json

class LoginDialog(QtCore.QObject):
    def __init__(self):
        UiFile = QtCore.QFile('UI/Login.ui')
        Loader = QUiLoader()
        UiFile.open(QtCore.QFile.ReadOnly)
        self.LoginUI=Loader.load(UiFile)
        UiFile.close()
        self.LoginUI.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 設定最上層
        self.LoginUI.setWindowModality(QtCore.Qt.ApplicationModal)  # 設定須先完成對話框，其他介面設定無效
        self.LoginUI.show()
        self.LoginUI.LoginConfirmbtn.accepted.connect(self.LoginFuncAccept)

        self.LoginUI.LoginConfirmbtn.rejected.connect(self.resetIDPW)        
        if self.LoginUI.IDPWCheck.checkState()==2:
            with open("IDPW.json",mode="r",encoding="utf-8") as file:
                data = json.load(file)
            self.LoginUI.LoginID.setText(data["ID"])
            self.LoginUI.LoginPW.setText(data["PW"])

    def resetIDPW(self):
        self.LoginUI.LoginID.setText('')
        self.LoginUI.LoginPW.setText('')
        self.LoginUI.IDPWCheck.setChecked(False)

class MessageDialog(QDialog):
    def __init__(self,gname):
        UiFile = QtCore.QFile('UI/Message.ui')
        Loader = QUiLoader()
        UiFile.open(QtCore.QFile.ReadOnly)
        self.MessageUI = Loader.load(UiFile)
        UiFile.close()
        self.MessageUI.setWindowTitle(gname)

if __name__ == "__main__":
    FuncUIApp = QApplication(sys.argv)
    SKLogin = LoginDialog()
    SKLogin.LoginUI.show()
    SKMessage = MessageDialog()
    SKMessage.MessageUI.show()
    sys.exit(FuncUIApp.exec_())