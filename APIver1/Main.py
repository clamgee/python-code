# 系統套件
import sys
import os
#運算套件
import numpy as np
import pandas as pd
# 使用PyQt5套件
from PyQt5.uic import loadUi #使用.ui介面模組
from PyQt5.QtCore import pyqtSlot #插入資訊模組
from PyQt5.QtWidgets import QApplication,QDialog,QFileDialog,QMainWindow #PyQt5介面控制模組
import PyQt5.QtCore as QtCore
# 使用SKCOM元件
import comtypes.client
import comtypes.gen.SKCOMLib as sk
skC = comtypes.client.CreateObject(sk.SKCenterLib,interface=sk.ISKCenterLib)
skO = comtypes.client.CreateObject(sk.SKOrderLib,interface=sk.ISKOrderLib)
skQ = comtypes.client.CreateObject(sk.SKQuoteLib,interface=sk.ISKQuoteLib)
skR = comtypes.client.CreateObject(sk.SKReplyLib,interface=sk.ISKReplyLib)

class SKMainWindow(QMainWindow):
    def __init__(self):
        super(SKMainWindow,self).__init__()
        loadUi(r'UI/MainWindow.ui',self)
        self.actionLogin.triggered.connect(self.SKLogin)
        self.SKLogin()

    def SKLogin(self):
        self.Login=LoginDialog()
        self.Login.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.Login.show()

class LoginDialog(QDialog):
    def __init__(self):
        super(LoginDialog,self).__init__()
        loadUi(r'UI/Login.ui',self)
    def LoginFunc(self):
            skC.SKCenterLib_SetLogPath(os.path.split(os.path.realpath(__file__))[0] + "\\CapitalLog_Quote")
            m_nCode = skC.SKCenterLib_Login(self.textID.get().replace(' ',''),self.textPassword.get().replace(' ',''))
            if(m_nCode==0):
                Global_ID["text"] =  self.textID.get().replace(' ','')
                WriteMessage("登入成功",self.listInformation)
            else:
                WriteMessage(m_nCode,self.listInformation)
        except Exception as e:
            messagebox.showerror("error！",e)


if __name__ == "__main__":
    SKApp=QApplication(sys.argv)
    SKMain=SKMainWindow()
    SKMain.show()
    sys.exit(SKApp.exec_())