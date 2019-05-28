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
#匯入外部字寫套件
import FuncUI
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
        self.SKID='未登入'
        self.statusbar.showMessage('帳號:'+self.SKID)
        self.actionLogin.triggered.connect(self.SKLoginUI)
        self.SKMessageUI()#設定系統訊息介面
        self.SKLoginUI() #設定登入介面

    # 呼叫系統訊息介面與功能
    def SKMessageUI(self):
        self.SKMessage=FuncUI.MessageDialog()        
        self.SKMessage.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.SKMessage.show()
    def SKMessageFunc(self):
        self.SKMessage.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.SKMessage.show()
    # 系統功能介面結束
    # 呼叫登入介面，與登入功能
    def SKLoginUI(self):
        self.Login=FuncUI.LoginDialog()
        self.Login.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.Login.show()
        self.Login.LoginConfirmbtn.clicked.connect(self.LoginFunc)
    
    def LoginFunc(self):
        try:
            skC.SKCenterLib_SetLogPath(os.path.split(os.path.realpath(__file__))[0] + "\\CapitalLog_Quote")
            ID=self.Login.LoginID.text().replace(' ','')
            PW=self.Login.LoginPW.text().replace(' ','')
            m_nCode = skC.SKCenterLib_Login(ID,PW)
            if m_nCode==0:
                self.SKID=ID
                self.statusbar.showMessage('帳號:'+str(self.SKID))
                self.SKMessage.append('登入成功')
                self.Login.close()
            else:
                self.SKMessage.append('登入失敗,錯誤碼:')
                ID='未登入'
                pass
        except Exception as e:
            # messagebox.showerror("error！",e)
            print('系統錯誤:'+e)
            pass
    # 登入功能結束


if __name__ == "__main__":
    SKApp=QApplication(sys.argv)
    SKMain=SKMainWindow()
    SKMain.show()
    sys.exit(SKApp.exec_())