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
        self.ui=Loader.load(UiFile)
        UiFile.close()
        self.ui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 設定最上層
        self.ui.setWindowModality(QtCore.Qt.ApplicationModal)  # 設定須先完成對話框，其他介面設定無效
        if self.ui.IDPWCheck.checkState()==2:
            with open("IDPW.json",mode="r",encoding="utf-8") as file:
                data = json.load(file)
            self.ui.LoginID.setText(data["ID"])
            self.ui.LoginPW.setText(data["PW"])

class MessageDialog(QtCore.QObject):
    def __init__(self,gname):
        UiFile = QtCore.QFile('UI/Message.ui')
        Loader = QUiLoader()
        UiFile.open(QtCore.QFile.ReadOnly)
        self.ui = Loader.load(UiFile)
        UiFile.close()
        self.ui.setWindowTitle(gname)
        # 顯示最大最小化按鍵
        self.ui.setWindowFlags(QtCore.Qt.WindowMinMaxButtonsHint|QtCore.Qt.WindowCloseButtonHint)

# if __name__ == "__main__":
#     FuncUIApp = QApplication(sys.argv)
#     SKLogin = LoginDialog()
#     SKLogin.ui.show()
#     SKMessage = MessageDialog()
#     SKMessage.ui.show()
#     sys.exit(FuncUIApp.exec_())