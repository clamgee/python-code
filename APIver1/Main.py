# 系統套件
import sys
import os
#運算套件
import numpy as np
import pandas as pd
# 使用PyQt5套件
from PyQt5.uic import loadUi #使用.ui介面模組
from PyQt5.QtCore import pyqtSlot,QDate,QTime,QDateTime,QTimer,Qt #插入資訊模組
from PyQt5.QtWidgets import QApplication,QDialog,QFileDialog,QMainWindow #PyQt5介面控制模組
from PyQt5 import QtCore, QtGui, QtWidgets
#匯入外部字寫套件
import FuncUI
# 使用SKCOM元件
import comtypes.client
import comtypes.gen.SKCOMLib as sk
skC = comtypes.client.CreateObject(sk.SKCenterLib,interface=sk.ISKCenterLib)
skO = comtypes.client.CreateObject(sk.SKOrderLib,interface=sk.ISKOrderLib)
skQ = comtypes.client.CreateObject(sk.SKQuoteLib,interface=sk.ISKQuoteLib)
skR = comtypes.client.CreateObject(sk.SKReplyLib,interface=sk.ISKReplyLib)

class SKMainWindow(QMainWindow): #主視窗
    def __init__(self):
        super(SKMainWindow,self).__init__()
        loadUi(r'UI/MainWindow.ui',self)
        self.showMaximized()
        self.SKID='未登入'
        self.statusBar.showMessage('帳號:'+self.SKID)
        # 介面導入
        self.SKLoginUI() #登入介面
        self.SKMessageFunc()#系統訊息介面
        #ManuBar連結
        self.actionLogin.triggered.connect(self.Login.show)#登入介面連結
        #ToolBar連結
        self.SysDetail.triggered.connect(self.SKMessage.show)
        self.Connectbtn.triggered.connect(self.ConnectFun)
        self.Disconnectbtn.triggered.connect(self.disconnectFun)

        # Tab內功能組連結
        self.commoditybtn.clicked.connect(self.commodityFnc)

    # 呼叫系統訊息介面與功能
    def SKMessageFunc(self):
        self.SKMessage=FuncUI.MessageDialog('系統訊息') #設定系統訊息介面        
        self.SKMessage.setWindowModality(QtCore.Qt.WindowModal)#設定須先關閉對話框，GUI設定無效
        # self.SKMessage.setWindowTitle('系統訊息')
    # 系統功能介面結束
    # 呼叫登入介面，與登入功能
    def SKLoginUI(self):
        self.Login=FuncUI.LoginDialog()
        self.Login.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)#設定最上層
        self.Login.setWindowModality(QtCore.Qt.ApplicationModal)#設定須先完成對話框，GUI設定無效
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
                self.statusBar.showMessage('帳號:'+str(self.SKID))
                self.SKMessage.textBrowser.append('登入成功')
                self.SKMessage.textBrowser.append('帳號: '+str(self.SKID))
                self.Login.close()
            else:
                self.SKMessage.textBrowser.append('登入失敗,錯誤碼:')
                ID='未登入'
                pass
        except Exception as e:
            # messagebox.showerror("error！",e)
            self.SKMessage.textBrowser.append('發生錯誤:'+e)
            # print('系統錯誤:'+e)
            pass
    # 登入功能結束
    #報價系統連線功能
    def ConnectFun(self):
        m_nCode=skQ.SKQuoteLib_EnterMonitor()
        self.SKMessage.textBrowser.append(str(m_nCode))
    def disconnectFun(self):
        m_nCode=skQ.SKQuoteLib_LeaveMonitor()
        self.SKMessage.textBrowser.append(str(m_nCode))
    #商品訂閱
    def commodityFnc(self):
        nstock=self.commodityline.text().replace(' ','')
        skQ.SKQuoteLib_RequestTicks(0,nstock)
        self.ndetialmsg=FuncUI.MessageDialog(nstock)
        self.TDetailbtn.clicked.connect(self.ndetialmsg.show)

class SKQuoteLibEvents:
     
    def OnConnection(self, nKind, nCode):
        if (nKind == 3001):
            strMsg = "Connected!"
        elif (nKind == 3002):
            strMsg = "DisConnected!"
        elif (nKind == 3003):
            strMsg = "Stocks ready!"
        elif (nKind == 3021):
            strMsg = "Connect Error!"
        print(strMsg)
        SKMain.SKMessage.textBrowser.append(strMsg)

    def OnNotifyServerTime(self,sHour,sMinute,sSecond,nTotal):
        nTime=QTime(sHour,sMinute,sSecond).toString(Qt.ISODate)
        # jTime=datetime.datetime.strptime('13:50:00','%H:%M:%S').time()
        # if nTime==jTime and Future.ticksdf is not None :
        #     filename='data/Ticks'+str(Future.ticksdf.iloc[-1,0])+'.txt'
        #     Future.ticksdf.to_csv(filename,header=False,index=False)
        SKMain.statusBar.showMessage('帳號:'+str(SKMain.SKID)+'\t伺服器時間:'+nTime)
    
    def OnNotifyHistoryTicks(self, sMarketNo, sStockIdx, nPtr, lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty, nSimulate):
        strMsg=str(lDate)+','+str(lTimehms)+','+str(lTimemillismicros)+','+str(nBid)+','+str(nAsk)+','+str(nClose)+','+str(nQty)
        SKMain.ndetialmsg.textBrowser.append(strMsg)
    
    def OnNotifyTicks(self,sMarketNo, sStockIdx, nPtr, lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty, nSimulate):
        strMsg=str(lDate)+','+str(lTimehms)+','+str(lTimemillismicros)+','+str(nBid)+','+str(nAsk)+','+str(nClose)+','+str(nQty)
        SKMain.ndetialmsg.textBrowser.append(strMsg)


SKQuoteEvent=SKQuoteLibEvents()
SKQuoteLibEventHandler = comtypes.client.GetEvents(skQ, SKQuoteEvent)

if __name__ == "__main__":
    SKApp=QApplication(sys.argv)
    SKMain=SKMainWindow()
    SKMain.show()
    sys.exit(SKApp.exec_())