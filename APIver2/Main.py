# 系統套件
import sys
import os
import datetime
import time
# 運算套件
import numpy as np
import pandas as pd
# 使用PyQt5套件
from PyQt5.uic import loadUi  # 使用.ui介面模組
from PyQt5.QtCore import pyqtSlot, QDate, QTime, QDateTime, QTimer, Qt, QThread, pyqtSignal, \
    QAbstractTableModel  # 插入資訊模組
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMainWindow, QGraphicsScene, QHeaderView, \
    QTableWidgetItem, QMessageBox  # PyQt5介面與繪圖模組
from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
# 匯入外部字寫套件
import FuncUI
import tickstokline
import KlineUi
import Config_dict
# 使用SKCOM元件
import comtypes.client
import comtypes.gen.SKCOMLib as sk

skC = comtypes.client.CreateObject(sk.SKCenterLib, interface=sk.ISKCenterLib)
skO = comtypes.client.CreateObject(sk.SKOrderLib, interface=sk.ISKOrderLib)
skQ = comtypes.client.CreateObject(sk.SKQuoteLib, interface=sk.ISKQuoteLib)
skR = comtypes.client.CreateObject(sk.SKReplyLib, interface=sk.ISKReplyLib)


class SKMainWindow(QMainWindow):  # 主視窗
    def __init__(self):
        super(SKMainWindow, self).__init__()
        loadUi(r'UI/MainWindow.ui', self)
        self.showMaximized()
        # 帳號處理
        self.SKID = '未登入'  # 登入帳號
        self.IBAccount = ''  # 期貨帳號
        self.statusBar.showMessage('帳號:' + self.SKID)
        self.fOrder = sk.FUTUREORDER()
        self.timestart = ''
        self.timeend = ''
        self.timeA=[]
        self.timeB=[]
        self.timeC=[]
        # 圖形化設定
        # 12K圖示宣告
        self.GL12K=pg.GraphicsLayout()
        self.GV1.setCentralItem(self.GL12K)
        self.Axis12k = pg.AxisItem(orientation='bottom')
        self.draw12k = self.GL12K.addPlot(axisItems={'bottom': self.Axis12k})
        self.draw12k.showAxis('right',show=True)
        self.draw12k.showAxis('left',show=False)
        self.draw12k.showGrid(x=False,y=True)
        self.axis12k_xmin = 0
        self.axis12k_xmax = 100
        self.axis12k_ymin = 0
        self.axis12k_ymax = 100
        self.draw12k.setXRange(self.axis12k_xmin,self.axis12k_xmax)
        self.draw12k.setYRange(self.axis12k_ymin,self.axis12k_ymax)
        # 分鐘K當沖圖形宣告，X軸共用，最小值為0
        self.GLminK=pg.GraphicsLayout()
        self.GV_pawn.setCentralItem(self.GLminK)
        self.Axismink = pg.AxisItem(orientation='bottom')
        self.drawmink = self.GLminK.addPlot(axisItems={'bottom': self.Axismink})
        self.drawmink.showAxis('right',show=True)
        self.drawmink.showAxis('left',show=False)
        self.drawmink.showGrid(x=False,y=True)
        self.axismin_ch = 0 #圖形邊界更新
        if time.localtime(time.time()).tm_hour >= 15 or time.localtime(time.time()).tm_hour < 8:
            self.axismink_xmax = 827
        elif time.localtime(time.time()).tm_hour >=8 and time.localtime(time.time()).tm_hour < 15:
            self.axismink_xmax = 300
        else:
            print('當沖邊界錯誤!!')
        self.axismink_ymin = 0
        self.axismink_ymax = 100
        self.drawmink.setXRange(0,self.axismink_xmax)
        self.drawmink.setYRange(self.axismink_ymin,self.axismink_ymax)
        self.YCline = pg.InfiniteLine(angle=0, movable=False)
        self.drawmink.addItem(self.YCline)
        self.GLminK.nextRow()#新增一個副圖Layout 多空力道
        self.Axisdealminus = pg.AxisItem(orientation='bottom')
        self.drawdealminus = self.GLminK.addPlot(axisItems={'bottom': self.Axisdealminus})
        self.drawdealminus.showAxis('right',show=True)
        self.drawdealminus.showAxis('left',show=False)
        self.drawdealminus.showGrid(x=False,y=True)
        self.axisdealminus_ymin = 0
        self.axisdealminus_ymax = 100
        self.drawdealminus.setXRange(0,self.axismink_xmax)
        self.drawdealminus.setYRange(self.axisdealminus_ymin,self.axisdealminus_ymax)
        self.drawdealminus.setXLink(self.drawmink)
        self.GLminK.nextRow()#新增一個副圖Layout 大單
        self.AxisBigDeal = pg.AxisItem(orientation='bottom')
        self.drawBigDeal = self.GLminK.addPlot(axisItems={'bottom': self.AxisBigDeal})
        self.drawBigDeal.showAxis('right',show=True)
        self.drawBigDeal.showAxis('left',show=False)
        self.drawBigDeal.showGrid(x=False,y=True)
        self.axisBigDeal_ymin = 0
        self.axisBigDeal_ymax = 100
        self.drawBigDeal.setXRange(0,self.axismink_xmax)
        self.drawBigDeal.setYRange(self.axisBigDeal_ymin,self.axisBigDeal_ymax)
        self.drawBigDeal.setXLink(self.drawmink)
        self.GLminK.nextRow()#新增一個副圖Layout 小單
        self.AxisRetailInvestors = pg.AxisItem(orientation='bottom')
        self.drawRetailInvestors = self.GLminK.addPlot(axisItems={'bottom': self.AxisRetailInvestors})
        self.drawRetailInvestors.showAxis('right',show=True)
        self.drawRetailInvestors.showAxis('left',show=False)
        self.drawRetailInvestors.showGrid(x=False,y=True)
        self.axisRetailInvestors_ymin = 0
        self.axisRetailInvestors_ymax = 100
        self.drawRetailInvestors.setXRange(0,self.axismink_xmax)
        self.drawRetailInvestors.setYRange(self.axisRetailInvestors_ymin,self.axisRetailInvestors_ymax)
        self.drawRetailInvestors.setXLink(self.drawmink)
        self.GLminK.layout.setRowStretchFactor(0,7) #當沖第 1 分鐘K線圖框大小
        self.GLminK.layout.setRowStretchFactor(1,1) #當沖第 2 多空力道圖框大小
        self.GLminK.layout.setRowStretchFactor(2,1) #當沖第 3 大單主力圖框大小
        self.GLminK.layout.setRowStretchFactor(3,1) #當沖第 4 小單散戶圖框大小

        # 下單參數 Future structure
        self.trade_act = -1
        self.OrderPrice = ''
        self.ReplyComplete = False
        # 介面導入
        self.SKLoginUI()  # 登入介面
        self.SKMessageFunc()  # 系統訊息介面
        self.RightUI()  # 權益數介面
        self.DomTableUI()  # 閃電下單介面
        self.MPTableUI()    #多空力道
        # ManuBar連結
        self.actionLogin.triggered.connect(self.Login.show)  # 登入介面連結
        # ToolBar連結
        self.SysDetail.triggered.connect(self.SKMessage.show)
        self.Connectbtn.triggered.connect(self.ConnectFun)
        self.Disconnectbtn.triggered.connect(self.disconnectFun)
        # Tab內功能組連結
        self.commoditybtn.clicked.connect(self.commodityFnc)
        self.BidAct_btn.clicked.connect(self.BidFunc)
        self.AskAct_btn.clicked.connect(self.AskFunc)
        self.LastPrice_btn.clicked.connect(self.LastPriceFunc)
        self.PriceSpin.valueChanged.connect(self.GetPriceFunc)
        self.MarketPrice_btn.clicked.connect(self.MarketPriceFunc)
        self.LimitMarketPrice_btn.clicked.connect(self.LimitMarketPriceFunc)
        self.Order_btn.clicked.connect(self.Order_btn_Func)
        self.OrderCancel_btn.clicked.connect(self.OrderCancelFunc)
        self.ClosePositionAll_btn.clicked.connect(self.ClosePositionAllFunc)

    def Draw12kUpdate(self):
        xmax = int(len(self.Kitem.pictures))
        if self.axis12k_xmax != xmax:
            self.axis12k_xmax = xmax
            xmin = int(max(0, xmax - self.Kitem.countK))
            self.axis12k_xmin = xmin 
            self.draw12k.setXRange(self.axis12k_xmin,self.axis12k_xmax)
            dict_tmp = self.Kitem.data['ndatetime'][(self.Kitem.data.volume!=12000) & (self.Kitem.data.ndatetime.dt.hour>8) & (self.Kitem.data.ndatetime.dt.hour<15)].dt.strftime('%Y-%m-%d %H:%M:%S').to_dict()
            self.Axis12k.setTicks([dict_tmp.items()])
            self.MAHighLine=self.draw12k.plot(pen='y')
            self.MALowLine=self.draw12k.plot(pen='b')
            self.MAHighLine.setData(self.Kitem.data.high_avg)
            self.MALowLine.setData(self.Kitem.data.low_avg)
        ymin = self.Kitem.data.loc[self.axis12k_xmin:self.axis12k_xmax, ['low']].values.min()
        ymax = self.Kitem.data.loc[self.axis12k_xmin:self.axis12k_xmax, ['high']].values.max()
        if self.axis12k_ymin != ymin or self.axis12k_ymax != ymax:
            self.axis12k_ymin = ymin
            self.axis12k_ymax = ymax        
            self.draw12k.setYRange(self.axis12k_ymin,self.axis12k_ymax)
            # xdate = self.Kitem.data.ndatetime.dt.strftime('%Y-%m-%d %H:%M:%S')
            # axis12k = pg.AxisItem('buttom')
    def DrawminkUpdate(self):
        xmax = int(len(self.minKitem.pictures))
        if self.axismin_ch != xmax:
            self.axismin_ch = xmax
            dict_tmp=self.minKitem.data['ndatetime'][self.minKitem.data.ndatetime.dt.minute==0].dt.strftime('%H:%M:%S').to_dict()
            self.Axismink.setTicks([dict_tmp.items()])
            self.Axisdealminus.setTicks([dict_tmp.items()])
            self.AxisBigDeal.setTicks([dict_tmp.items()])
            self.AxisRetailInvestors.setTicks([dict_tmp.items()])
            self.YCline.setPos(self.Future.yesterdayclose)
            self.curve=self.drawmink.plot(pen='y')
            tmpline=self.minKitem.data.close.cumsum()
            self.avgline = tmpline.apply(lambda x: x/(tmpline[tmpline==x].index[0]+1))
            self.curve.setData(self.avgline)
            del tmpline

        ymin = self.minKitem.data.loc[0:self.minKitem.lastidx, ['low']].values.min()
        ymin = min(ymin,self.Future.yesterdayclose)
        ymax = self.minKitem.data.loc[0:self.minKitem.lastidx, ['high']].values.max()
        ymax = max(ymax,self.Future.yesterdayclose)        
        dealbar_ymin=self.dealminusbar.data.loc[0:self.dealminusbar.lastidx,['dealminus']].values.min()
        dealbar_ymax=self.dealminusbar.data.loc[0:self.dealminusbar.lastidx,['dealminus']].values.max()
        Bigbar_ymin=self.bigbar.data.loc[0:self.bigbar.lastidx,['big']].values.min()
        Bigbar_ymax=self.bigbar.data.loc[0:self.bigbar.lastidx,['big']].values.max()
        RetailInvestorsbar_ymin=self.RetailInvestorsbar.data.loc[0:self.RetailInvestorsbar.lastidx,['small']].values.min()
        RetailInvestorsbar_ymax=self.RetailInvestorsbar.data.loc[0:self.RetailInvestorsbar.lastidx,['small']].values.max()
        if self.axismink_ymin != ymin or self.axismink_ymax != ymax:
            self.axismink_ymin = ymin
            self.axismink_ymax = ymax        
            self.drawmink.setYRange(self.axismink_ymin,self.axismink_ymax)
        if self.axisdealminus_ymin != dealbar_ymin or self.axisdealminus_ymax != dealbar_ymax:
            self.axisdealminus_ymin = dealbar_ymin
            self.axisdealminus_ymax = dealbar_ymax        
            self.drawdealminus.setYRange(self.axisdealminus_ymin,self.axisdealminus_ymax)
        if self.axisBigDeal_ymin != Bigbar_ymin or self.axisBigDeal_ymax != Bigbar_ymax:
            self.axisBigDeal_ymin = Bigbar_ymin
            self.axisBigDeal_ymax = Bigbar_ymax
            self.drawBigDeal.setYRange(self.axisBigDeal_ymin,self.axisBigDeal_ymax)
        if self.axisRetailInvestors_ymin != RetailInvestorsbar_ymin or self.axisRetailInvestors_ymax != RetailInvestorsbar_ymax:
            self.axisRetailInvestors_ymin = RetailInvestorsbar_ymin
            self.axisRetailInvestors_ymax = RetailInvestorsbar_ymax
            self.drawRetailInvestors.setYRange(self.axisRetailInvestors_ymin,self.axisRetailInvestors_ymax)



    # 呼叫系統訊息介面與功能
    def SKMessageFunc(self):
        self.SKMessage = FuncUI.MessageDialog('系統訊息')  # 設定系統訊息介面
        self.SKMessage.setWindowModality(QtCore.Qt.WindowModal)  # 設定須先關閉對話框，GUI設定無效
        # self.SKMessage.setWindowTitle('系統訊息')

    # 系統功能介面結束
    # 呼叫登入介面，與登入功能
    def SKLoginUI(self):
        self.Login = FuncUI.LoginDialog()
        self.Login.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 設定最上層
        self.Login.setWindowModality(QtCore.Qt.ApplicationModal)  # 設定須先完成對話框，GUI設定無效
        self.Login.show()
        self.Login.LoginConfirmbtn.clicked.connect(self.LoginFunc)

    def LoginFunc(self):
        try:
            skC.SKCenterLib_SetLogPath(os.path.split(os.path.realpath(__file__))[0] + "\\CapitalLog_Quote")
            ID = self.Login.LoginID.text().replace(' ', '')
            PW = self.Login.LoginPW.text().replace(' ', '')
            m_nCode = skC.SKCenterLib_Login(ID, PW)
            print("Login: "+str(m_nCode))
            m_nCode = skO.SKOrderLib_Initialize()
            print("SKOrderLib_Initialize(): "+str(m_nCode))
            m_nCode = skO.GetUserAccount()
            print("GetUserAccount: "+str(m_nCode))
            if m_nCode == 0:
                self.SKID = ID
                self.statusBar.showMessage('帳號:' + str(self.SKID))
                self.SKMessage.textBrowser.append('登入成功')
                self.SKMessage.textBrowser.append('帳號: ' + str(self.SKID))
                self.Reply_Open_Fnc()
                self.Login.close()
            else:
                self.SKMessage.textBrowser.append('登入失敗,錯誤碼:')
                ID = '未登入'
                pass
        except Exception as e:
            # messagebox.showerror("error！",e)
            self.SKMessage.textBrowser.append('發生錯誤:' + e)
            # print('系統錯誤:'+e)
            pass
    # 登入功能結束
    
    # 權益數介面
    def RightUI(self):
        self.Right_TB.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.Right_TB.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.Right_TB.setHorizontalHeaderLabels(['帳戶餘額', '浮動損益', '已實現費用'])
        self.Bill = pd.DataFrame(np.arange(41).reshape(41), columns=['Right'])  # 期貨權益數 DataFrame        
        i = 0
        while i < self.Bill.shape[0]:
            self.Bill.at[i, 'Right'] = QTableWidgetItem('')
            self.Bill.at[i, 'Right'].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            i += 1
        i = 1
        j = 0
        while i < self.Right_TB.rowCount():
            self.Right_TB.setItem(i, 0, self.Bill.at[j, 'Right'])
            j += 1
            if j >= self.Bill.shape[0]:
                break
            self.Right_TB.setItem(i, 1, self.Bill.at[j, 'Right'])
            j += 1
            if j >= self.Bill.shape[0]:
                break
            self.Right_TB.setItem(i, 2, self.Bill.at[j, 'Right'])
            j += 1
            if j >= self.Bill.shape[0]:
                break
            i += 2

    # 權益數介面結束
    # 閃電下單
    def DomTableUI(self):
        self.bestfive = pd.DataFrame(np.arange(24).reshape(6,4), columns=['買量','買價','賣價','賣量'])
        self.bestfive[['買量','買價','賣價','賣量']]=self.bestfive[['買量','買價','賣價','賣量']].astype(str)
        self.Dom1model=PandasModel()
        self.Dom1model.UpdateData(self.bestfive)
        self.DomTable.setModel(self.Dom1model)
        self.DomTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.DomTable.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.DomTable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.DomTable_pawn.setModel(self.Dom1model)
        self.DomTable_pawn.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.DomTable_pawn.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.DomTable_pawn.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # # TickKDom
        # self.DomTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.DomTable.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        # self.DomTable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.DomTable.setHorizontalHeaderLabels(['數量', '買進', '賣出', '數量'])
        # self.DomTable.horizontalHeader().setStyleSheet('QHeaderView::section{background:yellow}')
        # # 當沖Dom
        # self.DomTable_pawn.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.DomTable_pawn.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        # self.DomTable_pawn.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.DomTable_pawn.setHorizontalHeaderLabels(['數量', '買進', '賣出', '數量'])
        # self.DomTable_pawn.horizontalHeader().setStyleSheet('QHeaderView::section{background:yellow}')
        # self.bestfive = pd.DataFrame(np.arange(24).reshape(6,4), columns=['買量','買價','賣價','賣量'])

        # i = 0
        # while i < 6:
        #     self.bestfive.at[i, '買量'] = QTableWidgetItem('')
        #     self.DomTable.setItem(i, 0, self.bestfive.at[i, '買量'])
        #     self.DomTable_pawn.setItem(i, 0, self.bestfive.at[i, '買量'])
        #     self.bestfive.at[i, '買價'] = QTableWidgetItem('')
        #     self.DomTable.setItem(i, 1, self.bestfive.at[i, '買價'])
        #     self.DomTable_pawn.setItem(i, 1, self.bestfive.at[i, '買價'])
        #     self.bestfive.at[i, '賣價'] = QTableWidgetItem('')
        #     self.DomTable.setItem(i, 2, self.bestfive.at[i, '賣價'])
        #     self.DomTable_pawn.setItem(i, 2, self.bestfive.at[i, '賣價'])
        #     self.bestfive.at[i, '賣量'] = QTableWidgetItem('')
        #     self.DomTable.setItem(i, 3, self.bestfive.at[i, '賣量'])
        #     self.DomTable_pawn.setItem(i, 3, self.bestfive.at[i, '賣量'])
        #     self.bestfive.at[i, '買量'].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        #     self.bestfive.at[i, '買價'].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        #     self.bestfive.at[i, '賣價'].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        #     self.bestfive.at[i, '賣量'].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        #     i += 1
        # self.bestfive.at[13, 'closeTBitem'].setBackground(Qt.yellow)
        # self.bestfive.at[13, 'bidTBitem'].setBackground(Qt.yellow)
        # self.bestfive.at[13, 'askTBitem'].setBackground(Qt.yellow)
    def MPTableUI(self):
        self.MPTable.horizontalHeader().setVisible(True)
        self.MPTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.MPTable.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.MPTable.verticalHeader().setVisible(True)
        self.MPTable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.MPTable.verticalHeader().setDefaultAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.MPTable.setHorizontalHeaderLabels(['委口', '委筆', '成筆', '成口'])
        self.MPTable.horizontalHeader().setStyleSheet('QHeaderView::section{background:yellow}')
        self.MPTable.setVerticalHeaderLabels(['買進', '賣出', '差', '總口數'])
        self.MPTable.verticalHeader().setStyleSheet('QHeaderView::section{background:yellow}')
        self.MPower = pd.DataFrame(np.arange(16).reshape(4,4), columns=['ComQty','ComCont','DealCont','DealQty'])
        self.MPTable_pawn.horizontalHeader().setVisible(True)
        self.MPTable_pawn.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.MPTable_pawn.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.MPTable_pawn.verticalHeader().setVisible(True)
        self.MPTable_pawn.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.MPTable_pawn.verticalHeader().setDefaultAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.MPTable_pawn.setHorizontalHeaderLabels(['委口', '委筆', '成筆', '成口'])
        self.MPTable_pawn.horizontalHeader().setStyleSheet('QHeaderView::section{background:yellow}')
        self.MPTable_pawn.setVerticalHeaderLabels(['買進', '賣出', '差', '總口數'])
        self.MPTable_pawn.verticalHeader().setStyleSheet('QHeaderView::section{background:yellow}')
        self.MPower_pawndf = pd.DataFrame(np.arange(20).reshape(4,5), columns=['ComQty','ComCont','DealCont','DealQty','ndatetime'])
        self.MPower_pawndf['ndatetime'] = pd.to_datetime(self.MPower_pawndf['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')

        i=0
        while i < 4 :
            j=0
            while j < 4:
                self.MPower.at[i,self.MPower.columns[j]] = QTableWidgetItem('')
                self.MPower.at[i,self.MPower.columns[j]].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.MPTable.setItem(i, j, self.MPower.at[i,self.MPower.columns[j]])
                self.MPower_pawndf.at[i,self.MPower_pawndf.columns[j]] = QTableWidgetItem('')
                self.MPower_pawndf.at[i,self.MPower_pawndf.columns[j]].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.MPTable_pawn.setItem(i, j, self.MPower_pawndf.at[i,self.MPower_pawndf.columns[j]])
                j+=1
            # self.MPower.at[i,'ComQty'] = QTableWidgetItem('')
            # self.MPower.at[i,'ComQty'].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            # # self.MPTable_pawn.setItem(i, 0, self.MPower.at[i,'ComQty'])
            # self.MPower.at[i,'ComCont'] = QTableWidgetItem('')
            # self.MPower.at[i,'ComCont'].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            # self.MPTable.setItem(i, 1, self.MPower.at[i,'ComCont'])
            # # self.MPTable_pawn.setItem(i, 1, self.MPower.at[i,'ComCont'])
            # self.MPower.at[i,'DealCont'] = QTableWidgetItem('')
            # self.MPower.at[i,'DealCont'].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            # self.MPTable.setItem(i, 2, self.MPower.at[i,'DealCont'])
            # # self.MPTable_pawn.setItem(i, 2, self.MPower.at[i,'DealCont'])
            # self.MPower.at[i,'DealQty'] = QTableWidgetItem('')
            # self.MPower.at[i,'DealQty'].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            # self.MPTable.setItem(i, 3, self.MPower.at[i,'DealQty'])
            # # self.MPTable_pawn.setItem(i, 3, self.MPower.at[i,'DealQty'])
            i+=1





    # def DomTableFillFunc(self,total_dict):
    #     self.bestfive.loc[0:4,['bidQty','nbid','nask','askQty']]=pd.DataFrame.from_dict(total_dict)
        # if self.bestfive.at[13, 'close'] != nclose:
        #     self.bestfive['close'] = self.bestfive['close'].map(
        #         lambda x: nclose + 13 - (self.bestfive['close'][self.bestfive['close'] == x].index[0]))
        #     self.bestfive['closeTBitem'].map(lambda x: x.setText(str(self.bestfive.at[self.bestfive['closeTBitem'][self.bestfive['closeTBitem'] == x].index[0], 'close'])))
        #         # self.bestfive.loc[self.bestfive['closeTBitem'][self.bestfive['closeTBitem'] == x].index[0], 'close'])))
        # self.bestfive['bid'] = self.bestfive['close'].map(bid_dict).fillna(value=0)#.astype(int)
        # self.bestfive['ask'] = self.bestfive['close'].map(ask_dict).fillna(value=0)#.astype(int)
        # asklist = self.bestfive['ask'][self.bestfive['ask'] != 0].index.tolist()
        # bidlist = self.bestfive['bid'][self.bestfive['bid'] != 0].index.tolist()
        # # # print('bid: ',self.bestfive['bid'].to_dict())
        # self.lastbidlist = list(set(self.lastbidlist + bidlist))
        # self.lastasklist = list(set(self.lastasklist + asklist))
        # self.bestfive.loc[self.lastbidlist, 'bidTBitem'].map(lambda x: x.setText(
        #     str(self.bestfive.loc[self.bestfive['bidTBitem'][self.bestfive['bidTBitem'] == x].index[0], 'bid'])) if
        # self.bestfive.loc[
        #     self.bestfive['bidTBitem'][self.bestfive['bidTBitem'] == x].index[0], 'bid'] != 0 else x.setText(''))
        # self.bestfive.loc[self.lastasklist, 'askTBitem'].map(lambda x: x.setText(
        #     str(self.bestfive.loc[self.bestfive['askTBitem'][self.bestfive['askTBitem'] == x].index[0], 'ask'])) if
        # self.bestfive.loc[
        #     self.bestfive['askTBitem'][self.bestfive['askTBitem'] == x].index[0], 'ask'] != 0 else x.setText(''))
        # # self.lastclose=self.bestfive['close'].tolist()
        # self.lastbidlist = bidlist
        # self.lastasklist = asklist

    # 閃電下單結束
    # 報價系統連線功能
    def ConnectFun(self):
        m_nCode = skQ.SKQuoteLib_EnterMonitor()
        # self.Connectbtn.setStyleSheet(""" QAction { background-color: rgb(49,49,49); color: rgb(255,255,255); border: 1px solid ;} """)
        self.SKMessage.textBrowser.append("EnterMonitor: "+str(m_nCode))

    def disconnectFun(self):
        m_nCode = skQ.SKQuoteLib_LeaveMonitor()
        self.SKMessage.textBrowser.append("LeaveMonitor: "+str(m_nCode))

    # 報價系統結束
    # 商品訂閱
    def commodityFnc(self):
        nstock = self.commodityline.text().replace(' ', '')
        self.Future = tickstokline.dataprocess(nstock)
        # self.newThread=His_KLlineThread()
        # self.tmpthread=QThread()
        # self.newThread.moveToThread(self.tmpthread)
        # self.tmpthread.start()
        skQ.SKQuoteLib_RequestTicks(0, nstock)
        skQ.SKQuoteLib_RequestFutureTradeInfo(comtypes.automation.c_short(0),nstock)
        self.ndetialmsg = FuncUI.MessageDialog(nstock)
        self.TDetailbtn.clicked.connect(self.ndetialmsg.show)
        # self.ndetialmsg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # self.ndetialmsg.show()
        # self.Kitem = KlineUi.CandlestickItem()
        self.Kitem = KlineUi.CandleItem()
        self.minKitem = KlineUi.CandleItem()
        self.dealminusbar = KlineUi.BarItem('dealminusbar')
        self.bigbar = KlineUi.BarItem('bigbar')
        self.RetailInvestorsbar = KlineUi.BarItem('RetailInvestorsbar')
        # self.Kui = KlineUi.KlineWidget(nstock)
        # self.Kui.addItem(self.Kitem)
        self.draw12k.addItem(self.Kitem)
        self.Kitem.set_data(self.Future.lastidx,self.Future.High,self.Future.Low,self.Future.contractkpd)
        self.drawmink.addItem(self.minKitem)
        self.drawdealminus.addItem(self.dealminusbar)
        self.drawBigDeal.addItem(self.bigbar)
        self.drawRetailInvestors.addItem(self.RetailInvestorsbar)
        # while self.Future.mindf.any()==False:
        #     sleep(1000)
        # self.minKitem.set_data(self.Future.minlastidx,self.Future.minhigh,self.Future.minlow,self.Future.mindf)
        # self.Kitem.set_data(self.Future.contractkpd)
        # self.SKQThread = SKQuoteThread()
        # self.SKQThread.start()
        # self.HisKlineThrd=His_KLlineThread()
        # self.HisKlineThrd.start()
        # self.TableThrd = TableThread()
        # if self.TableThrd.isRunning:
        #     self.TableThrd.quit()
        #     pass
        # else:
        #     self.TableThrd.start()
        self.Draw12kUpdate()
        # self.DrawminkUpdate()        

    # 商品訂閱結束
    # 委託未平倉回報資料
    def Reply_Open_Fnc(self):
        self.replypd = pd.DataFrame(
            columns=['商品名稱', '買賣', '委託價格', '委託口數', '委託狀態', '成交口數', '取消口數', '倉位', '條件', '價位格式', '委託序號', '委託書號', '委託日期',
                     '委託時間', '交易時段'])
        self.ReplyCRpdMode = PandasModel()
        self.openpd = pd.DataFrame(
            columns=['市場別', '期貨帳號', '商品', '買賣別', '未平倉部位', '當沖未平倉部位', '平均成本', '一點價值', '單口手續費', '交易稅','登入帳號'])
        self.OpenCRpdMode = PandasModel()
        self.test = 0

    # 委託未平倉回報結束
    # 下單功能
    def BidFunc(self):
        if self.trade_act != 0:
            self.BidAct_btn.setStyleSheet('background-color: red;''color: white;')
            self.trade_act = 0
            self.AskAct_btn.setStyleSheet('background-color: ')
        else:
            self.BidAct_btn.setStyleSheet('background-color: ;''color:')
            self.trade_act = -1

    def AskFunc(self):
        if self.trade_act != 1:
            self.AskAct_btn.setStyleSheet('background-color: green')
            self.trade_act = 1
            self.BidAct_btn.setStyleSheet('background-color: ;''color:')
        else:
            self.AskAct_btn.setStyleSheet('background-color: ')
            self.trade_act = -1

    def LastPriceFunc(self):
        self.PriceSpin.setEnabled(True)
        self.OrderType_box.setCurrentIndex(0)
        self.PriceSpin.setValue(self.Future.contractkpd.iloc[-1, 4])

    def GetPriceFunc(self):
        self.OrderPrice = str(self.PriceSpin.value())

    def MarketPriceFunc(self):
        self.PriceSpin.setEnabled(False)
        if self.OrderPrice != 'M':
            self.OrderPrice = 'M'
            self.OrderType_box.setCurrentIndex(1)

    def LimitMarketPriceFunc(self):
        self.PriceSpin.setEnabled(False)
        if self.OrderPrice != 'P':
            self.OrderPrice = 'P'
            self.OrderType_box.setCurrentIndex(1)

    def Order_btn_Func(self):
        # 填入完整帳號
        self.fOrder.bstrFullAccount = self.Future_Acc_CBox.currentText()
        # 填入期權代號
        if self.commodityline.text() == 'TX00':
            commodity = 'MTX00'
        else:
            commodity = self.commodityline.text()
        # 買賣別
        if self.trade_act == -1:
            msgbox = QMessageBox()
            msgbox.setWindowTitle('買賣設定錯誤')
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText('尚未選定買或賣')
            msgbox.setStandardButtons(QMessageBox.Abort)
            msgbox.setDefaultButton(QMessageBox.Abort)
            reply = msgbox.exec_()
            if reply == QMessageBox.Abort:
                return None
        self.OrderFunc(self.Future_Acc_CBox.currentText(), commodity, self.trade_act, self.OrderType_box.currentIndex(),
                       self.OrderPrice, self.Contract_Box.value(), self.InterestType_box.currentIndex())

    def OrderFunc(self, Account, Commodity, TradeAct, TradeType, OderPrice, Qty, InterestType):
        # 填入完整帳號
        self.fOrder.bstrFullAccount = Account
        # 填入期權代號
        self.fOrder.bstrStockNo = Commodity
        # 買賣別
        self.fOrder.sBuySell = TradeAct
        # ROD、IOC、FOK
        self.fOrder.sTradeType = TradeType
        # 非當沖、當沖
        self.fOrder.sDayTrade = 0
        # 委託價
        self.fOrder.bstrPrice = OderPrice
        # 委託數量
        self.fOrder.nQty = Qty
        # 新倉、平倉、自動
        self.fOrder.sNewClose = InterestType
        # 盤中、T盤預約
        self.fOrder.sReserved = 0
        # bstrMessage=''
        m_nCode = skO.SendFutureOrder(self.SKID, False, self.fOrder)
        print(m_nCode, type(m_nCode))
        # print(skC.SKCenterLib_GetReturnCodeMessage(m_nCode))
        # self.SKMessage.textBrowser.append(str(skC.SKCenterLib_GetReturnCodeMessage(m_nCode)))

    def OrderCancelFunc(self):
        if self.replypd.shape[0] > 0:
            for SqNo in self.replypd['委託序號']:
                m_tupple = skO.CancelOrderBySeqNo(self.SKID, False, self.IBAccount, SqNo)
                SKMain.SKMessage.textBrowser.append(
                    str(m_tupple[0]) + ',' + str(m_tupple[1]) + ',' + str(self.IBAccount) + ',' + str(SqNo))
        else:
            msg_box = QMessageBox()
            msg_box.setWindowTitle('無委託')
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText('目前無有效委託單')
            msg_box.setStandardButtons(QMessageBox.Abort)
            msg_box.setDefaultButton(QMessageBox.Abort)
            reply = msg_box.exec_()
            if reply == QMessageBox.Abort:
                return None

    def ClosePositionAllFunc(self):
        if self.openpd.shape[0] == 0:
            msgbox = QMessageBox()
            msgbox.setWindowTitle('無倉位')
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText('目前無持有倉位')
            msgbox.setStandardButtons(QMessageBox.Abort)
            msgbox.setDefaultButton(QMessageBox.Abort)
            reply = msgbox.exec_()
            if reply == QMessageBox.Abort:
                return None
        else:
            tmplist = self.openpd.index.tolist()
            for i in tmplist:
                # ['市場別','帳號','商品','買賣別','未平倉部位','當沖未平倉部位','平均成本','一點價值','單口手續費','交易稅']
                Account = SKMain.openpd.loc[i, '帳號']
                Commodity = SKMain.openpd.loc[i, '商品']
                if self.openpd.loc[i, '買賣別'] == 'B':
                    TradeAct = 1  # 賣出平倉
                elif self.openpd.loc[i, '買賣別'] == 'S':
                    TradeAct = 0  # 買進平倉
                else:
                    msgbox = QMessageBox()
                    msgbox.setWindowTitle('倉位錯誤')
                    msgbox.setIcon(QMessageBox.Information)
                    msgbox.setText('目前持有倉位不明')
                    msgbox.setStandardButtons(QMessageBox.Abort)
                    msgbox.setDefaultButton(QMessageBox.Abort)
                    reply = msgbox.exec_()
                    if reply == QMessageBox.Abort:
                        return None
                TradeType = 1
                OderPrice = 'M'
                Qty = self.openpd.loc[i, '未平倉部位']
                InterestType = 1
                self.OrderFunc(Account, Commodity, TradeAct, TradeType, OderPrice, Qty, InterestType)

    # 下單功能結束


# 多執行續閃電下單
class TableThread(QThread):
    Table_signal = pyqtSignal(int, dict)

    def __init__(self, parent=None):
        super(TableThread, self).__init__(parent)
        self.Table_signal.connect(self.TableFunc)

    def TableFunc(self, nclose, total_dict):
        SKMain.DomTableFillFunc(nclose, total_dict['bid_dict'], total_dict['ask_dict'])


class His_KLlineThread(QtCore.QObject):
    KLine_signal = pyqtSignal(str, int, int, int, int, int, int)

    def __init__(self, parent=None):
        super(His_KLlineThread, self).__init__(parent)
        self.KLine_signal.connect(self.run)

    def run(self, lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty):
        SKMain.Future.Ticks(lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty)
        strMsg = str(SKMain.Future.contractkpd.iloc[-1:].values)
        SKMain.ndetialmsg.textBrowser.append(strMsg)


class PandasModel(QAbstractTableModel):
    def __init__(self):
        QAbstractTableModel.__init__(self)

    def UpdateData(self, data):
        self._data = data
        self.layoutAboutToBeChanged.emit()  # 建立變更資料通知訊號發射
        self.dataChanged.emit(self.createIndex(0, 0),self.createIndex(self.rowCount(), self.columnCount()))  # 資料變更區域訊號發射
        self.layoutChanged.emit()  # 資料變更訊號發射

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.at[index.row(), self._data.columns[index.column()]])
            elif role == Qt.TextAlignmentRole:
                return int(Qt.AlignCenter | Qt.AlignVCenter)
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None


class SKOrderLibEvent:
    def OnAccount(self, bstrLogInID, bstrAccountData):
        Line = bstrAccountData.split(',')
        print(bstrAccountData)
        if Line[0] == 'TF':
            SKMain.IBAccount = str(Line[1]).strip() + str(Line[3]).strip()
            print('期貨帳戶: ' + SKMain.IBAccount, ',', Line[5])
            SKMain.Future_Acc_CBox.addItem(SKMain.IBAccount)
            m_nCode = skO.GetFutureRights(bstrLogInID, SKMain.IBAccount, 1)
            SKMain.SKMessage.textBrowser.append(skC.SKCenterLib_GetReturnCodeMessage(m_nCode))
            m_nCode = skO.ReadCertByID(bstrLogInID)
            SKMain.SKMessage.textBrowser.append(skC.SKCenterLib_GetReturnCodeMessage(m_nCode))
            m_nCode = skR.SKReplyLib_ConnectByID(bstrLogInID)
            SKMain.SKMessage.textBrowser.append(skC.SKCenterLib_GetReturnCodeMessage(m_nCode))
            m_nCode = skO.GetOpenInterestWithFormat(bstrLogInID, SKMain.IBAccount,3)
            SKMain.SKMessage.textBrowser.append(skC.SKCenterLib_GetReturnCodeMessage(m_nCode))

    def OnAsyncOrder(self, nThreadID, nCode, bstrMessage):
        print('OnAsyncOrder:', nThreadID, ',', nCode, ',', bstrMessage)

    def OnFutureRights(self, bstrData):
        Line = bstrData.split(',')
        i = 0
        for row in Line:
            if row.find('##') >= 0:
                break
            else:
                if row.find('+') >= 0:
                    SKMain.Bill.loc[i, 'Right'].setText(str(int(row.replace('+', '').strip())))
                else:
                    SKMain.Bill.loc[i, 'Right'].setText(row.strip())
            i += 1

    def OnOpenInterest(self, bstrData):
        Line = bstrData.split(',')
        if Line[0] == 'M003 NO DATA':
            print('No Data pass')
            pass
        elif Line[0] == '##':
            SKMain.OpenCRpdMode.UpdateData(SKMain.openpd)
            SKMain.Open_TBW.setModel(SKMain.OpenCRpdMode)
            print('OnOpenInterest end pass')
            pass
        else:
            SKMain.openpd = SKMain.openpd.append(pd.DataFrame([Line],columns=['市場別', '期貨帳號', '商品', '買賣別', '未平倉部位', '當沖未平倉部位','平均成本', '一點價值', '單口手續費', '交易稅','登入帳號']))
        SKMain.test+=1
        # i=0
        # print(Line)
        # for row in Line:
        #     print('次數: ', SKMain.test, '欄位:',i,'數值:',row)
        #     i+=1


class SKReplyLibEvent:
    def OnConnect(self, bstrUserID, nErrorCode):
        nErrorStr = skC.SKCenterLib_GetReturnCodeMessage(nErrorCode)
        print('連線成功: ', bstrUserID, nErrorStr)

    def OnDisconnect(self, bstrUserID, nErrorCode):
        nErrorStr = skC.SKCenterLib_GetReturnCodeMessage(nErrorCode)
        ntime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print('連線失敗: ', bstrUserID, nErrorStr, ntime)
    
    def OnReplyMessage(self,bstrUserID,bstrMessage):
        sComfirmCode=-1
        SKMain.SKMessage.textBrowser.append(bstrUserID+","+bstrMessage)
        print(bstrUserID+","+bstrMessage)
        return sComfirmCode

    def OnComplete(self, bstrUserID):
        SKMain.ReplyCRpdMode.UpdateData(SKMain.replypd)
        SKMain.Reply_TBW.setModel(SKMain.ReplyCRpdMode)
        SKMain.ReplyComplete = True
        # print(SKMain.replypd)

    def OnNewData(self, bstrUserID, bstrData):
        Line = bstrData.split(',')

        if Line[2] == 'D':
            dealcontract = Line[20]
        else:
            dealcontract = 0

        if Line[2] == 'C':
            cancelcontract = Line[20]
        else:
            cancelcontract = 0

        if SKMain.replypd.shape[0] > 0:
            tmp = SKMain.replypd.委託序號.isin({Line[0]})
            if tmp[tmp == True].index.shape[0] > 0:
                i = tmp[tmp == True].index[0]
            else:
                i = None
        else:
            i = None

        if i is not None:
            SKMain.replypd.loc[i, '買賣'] = Config_dict.OnNewData_dict['BuySell'][Line[1]][Line[6][0]]
            SKMain.replypd.loc[i, '委託價格'] = Line[11]
            SKMain.replypd.loc[i, '委託口數'] = Line[20]
            SKMain.replypd.loc[i, '委託狀態'] = Config_dict.OnNewData_dict['Type'][Line[2]]
            SKMain.replypd.loc[i, '成交口數'] = dealcontract
            SKMain.replypd.loc[i, '取消口數'] = cancelcontract
            SKMain.replypd.loc[i, '倉位'] = Config_dict.OnNewData_dict['BuySell'][Line[1]][Line[6][1]]
            SKMain.replypd.loc[i, '條件'] = Config_dict.OnNewData_dict['BuySell'][Line[1]][Line[6][2]]
            SKMain.replypd.loc[i, '價位格式'] = Config_dict.OnNewData_dict['BuySell'][Line[1]][Line[6][3]]
            SKMain.replypd.loc[i, '委託時間'] = Line[24]
            SKMain.replypd.loc[i, '交易時段'] = Line[24]
        else:
            tmplist = [[Line[8], Config_dict.OnNewData_dict['BuySell'][Line[1]][Line[6][0]],
                        Line[11], Line[20],
                        Config_dict.OnNewData_dict['Type'][Line[2]],
                        dealcontract, cancelcontract,
                        Config_dict.OnNewData_dict['BuySell'][Line[1]][Line[6][1]],
                        Config_dict.OnNewData_dict['BuySell'][Line[1]][Line[6][2]],
                        Config_dict.OnNewData_dict['BuySell'][Line[1]][Line[6][3]],
                        Line[0], Line[10], Line[23], Line[24], Line[24]]]
            SKMain.replypd = SKMain.replypd.append(pd.DataFrame(tmplist,
                                                                columns=['商品名稱', '買賣', '委託價格', '委託口數', '委託狀態', '成交口數',
                                                                         '取消口數', '倉位', '條件', '價位格式', '委託序號', '委託書號',
                                                                         '委託日期', '委託時間', '交易時段']), ignore_index=True)
        if SKMain.ReplyComplete == True:
            SKMain.ReplyCRpdMode.UpdateData(SKMain.replypd)

    def OnSmartData(self, bstrUserID, bstrData):
        print(bstrUserID, '智動回報:', bstrData)


def repeatQuote(func):
    def wrapper():
        func()

    return wrapper


class SKQuoteLibEvents:

    def OnConnection(self, nKind, nCode):
        if (nKind == 3001):
            strMsg = "Connected!, "+str(nCode)
        elif (nKind == 3002):
            strMsg = "DisConnected!, "+str(nCode)
        elif (nKind == 3003):
            strMsg = "Stocks ready!, "+str(nCode)
            time.sleep(5)
            SKMain.commodityFnc()
        elif (nKind == 3021):
            strMsg = "Connect Error!, "+str(nCode)
        else:
            strMsg = nCode
        print(strMsg)
        SKMain.SKMessage.textBrowser.append(strMsg)

    def OnNotifyServerTime(self, sHour, sMinute, sSecond, nTotal):
        nTime = QTime(sHour, sMinute, sSecond)
        rTime = QTime(8,30,00)
        if rTime == nTime:
            SKMain.ConnectFun()
        jTime = QTime(13, 50, 00)
        # jTime=datetime.datetime.strptime('13:50:00','%H:%M:%S').time()
        if nTime == jTime and SKMain.Future.ticklst is not None:
            ticksdf = pd.DataFrame(columns=['ndatetime','nbid','nask','close','volume','deal'])
            ticksdf =ticksdf.append(pd.DataFrame(SKMain.Future.ticklst,columns=['ndatetime','nbid','nask','close','volume','deal']),ignore_index=True,sort=False)
            ticksdf['ndatetime']=pd.to_datetime(ticksdf['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
            filename = 'Ticks' + ticksdf.iloc[-1, 0].date().strftime('%Y-%m-%d') + '.txt'
            ticksdf.to_csv('../data/'+filename, header=False, index=False)
            df1=pd.read_csv('filename.txt')
            df1=df1.append(pd.DataFrame([[filename]],columns=['filename']),ignore_index=True)
            df1.to_csv('filename.txt',index=False)
            del df1
            del ticksdf
            result=SKMain.Future.contractkpd.drop(columns=['high_avg','low_avg','dealbid','dealask','dealminus'])            
            result.sort_values(by=['ndatetime'],ascending=True)
            result.to_csv('../result.dat',header=True, index=False,mode='w')
        nTime = QTime(sHour, sMinute, sSecond).toString(Qt.ISODate)
        # print('帳號:' + str(SKMain.SKID) + '\t伺服器時間:' + nTime)
        SKMain.statusBar.showMessage('帳號:' + str(SKMain.SKID) + '\t伺服器時間:' + nTime)

    # @repeatQuote
    def OnNotifyHistoryTicks(self, sMarketNo, sStockIdx, nPtr, lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty, nSimulate):
        if nSimulate == 0:
            # SKMain.newThread.KLine_signal.emit(str(lDate),int(lTimehms),int(lTimemillismicros),int(nBid),int(nAsk),int(nClose),int(nQty))
            # print([lDate,lTimehms,lTimemillismicros,nBid,nAsk,nClose,nQty,sStockIdx])
            if SKMain.timestart=='':
                SKMain.timestart = time.time()
            if SKMain.Future.hisbol!=1:
                SKMain.Future.hisbol=1
            SKMain.Future.Ticks(lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty)
            # print(lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty)

            # strMsg = str(SKMain.Future.contractkpd.iloc[-1:].values)
            # SKMain.ndetialmsg.textBrowser.append(strMsg)

    def OnNotifyTicks(self, sMarketNo, sStockIdx, nPtr, lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty, nSimulate):
        # strMsg=str(lDate)+','+str(lTimehms)+','+str(lTimemillismicros)+','+str(nBid)+','+str(nAsk)+','+str(nClose)+','+str(nQty)
        if nSimulate == 0:
            # SKMain.newThread.KLine_signal.emit(str(lDate),int(lTimehms),int(lTimemillismicros),int(nBid),int(nAsk),int(nClose),int(nQty))
            # print('ThreadName: ',QThread.currentThread().objectName(),'ThreadID: ',int(QThread.currentThreadId()))
            if SKMain.timeend == '' and SKMain.Future.hisbol==1:
                SKMain.timeend = time.time()
                SKMain.Future.hisbol=2
                SKMain.Future.Ticks(lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty)
                print(round((SKMain.timeend-SKMain.timestart),3))
                # print(SKMain.Future.contractkpd.tail(10))
            else:
                SKMain.Future.Ticks(lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty)
            # strMsg = str(SKMain.Future.contractkpd.iloc[-1:].values)
            start = time.time()
            SKMain.Kitem.set_data(SKMain.Future.lastidx,SKMain.Future.High,SKMain.Future.Low,SKMain.Future.contractkpd.tail(SKMain.Future.lastidx+1-SKMain.Kitem.lastidx))
            A = time.time()-start
            start = time.time()
            SKMain.minKitem.set_data(SKMain.Future.minlastidx,SKMain.Future.minhigh,SKMain.Future.minlow,SKMain.Future.mindf.tail(SKMain.Future.minlastidx+1-SKMain.minKitem.lastidx))
            B = time.time()-start
            start = time.time()
            SKMain.dealminusbar.set_data(SKMain.Future.minlastidx,SKMain.Future.mindf[['ndatetime','dealminus']].tail(SKMain.Future.minlastidx+1-SKMain.dealminusbar.lastidx))
            if SKMain.Future.mindf is not None:
                SKMain.bigbar.set_data(SKMain.Future.minlastidx,SKMain.Future.mindf[['ndatetime','big']].tail(SKMain.Future.minlastidx+1-SKMain.bigbar.lastidx))
                SKMain.RetailInvestorsbar.set_data(SKMain.Future.minlastidx,SKMain.Future.mindf[['ndatetime','small']].tail(SKMain.Future.minlastidx+1-SKMain.RetailInvestorsbar.lastidx))
            C = time.time()-start
            xmax = SKMain.Future.lastidx + 1
            minkmax = SKMain.Future.minlastidx + 1
            if SKMain.axis12k_xmax != xmax:
                SKMain.Draw12kUpdate()
            if SKMain.axismin_ch != minkmax:
                SKMain.DrawminkUpdate()
            SKMain.MPower.at[0,'DealQty'].setText(str(SKMain.Future.contractkpd.at[SKMain.Future.lastidx,'dealbid']))
            SKMain.MPower.at[1,'DealQty'].setText(str(SKMain.Future.contractkpd.at[SKMain.Future.lastidx,'dealask']))
            SKMain.MPower.at[2,'DealQty'].setText(str(SKMain.Future.contractkpd.at[SKMain.Future.lastidx,'dealminus']))
            SKMain.MPower_pawndf.at[0,'DealQty'].setText(str(SKMain.Future.contractkpd.at[SKMain.Future.lastidx,'dealbid']))
            SKMain.MPower_pawndf.at[1,'DealQty'].setText(str(SKMain.Future.contractkpd.at[SKMain.Future.lastidx,'dealask']))
            SKMain.MPower_pawndf.at[2,'DealQty'].setText(str(SKMain.Future.contractkpd.at[SKMain.Future.lastidx,'dealminus']))

            if SKMain.Future.contractkpd.at[SKMain.Future.lastidx,'dealminus'] > 0:
                SKMain.MPower.at[2,'DealQty'].setBackground(Qt.red)
                SKMain.MPower_pawndf.at[2,'DealQty'].setBackground(Qt.red)
            else:
                SKMain.MPower.at[2,'DealQty'].setBackground(Qt.green)
                SKMain.MPower_pawndf.at[2,'DealQty'].setBackground(Qt.green)
            SKMain.MPower.at[3,'DealQty'].setText(str(SKMain.Future.ticksum))
            SKMain.MPower_pawndf.at[3,'DealQty'].setText(str(SKMain.Future.ticksum))
            if len(SKMain.timeA)==1000 or len(SKMain.timeB)==1000:
                SKMain.timeA.pop(0)
                SKMain.timeA.append(A)
                SKMain.timeB.pop(0)
                SKMain.timeB.append(B)
                SKMain.timeC.pop(0)
                SKMain.timeC.append(C)

            else:
                SKMain.timeA.append(A)
                SKMain.timeB.append(B)
                SKMain.timeC.append(C)
            A = str(int(1/(sum(SKMain.timeA)/len(SKMain.timeA))))
            B = str(int(1/(sum(SKMain.timeB)/len(SKMain.timeB))))
            C = str(int(1/(sum(SKMain.timeC)/len(SKMain.timeC))))
            SKMain.draw12k.setLabel('top','12K線: '+ A +' ,分鐘: '+ B+' ,Bar : '+ C)
            
            # SKMain.ndetialmsg.textBrowser.append(str(SKMain.Future.ticklst[-1]))
            # if SKMain.axis12k_xmax != xmax:
            #     SKMain.axis12k_xmax = xmax
            #     xmin = int(max(0, xmax - SKMain.Kitem.countK))
            #     SKMain.axis12k_xmin = xmin 
            #     SKMain.draw12k.setXRange(SKMain.axis12k_xmin,SKMain.axis12k_xmax)
            # ymin = SKMain.Kitem.data.loc[SKMain.axis12k_xmin:SKMain.axis12k_xmax, ['low']].values.min()
            # if SKMain.axis12k_ymin != ymin:
            #     SKMain.axis12k_ymin = ymin
            #     SKMain.draw12k.setYRange(SKMain.axis12k_ymin,SKMain.axis12k_ymax)
            # ymax = SKMain.Kitem.data.loc[SKMain.axis12k_xmin:SKMain.axis12k_xmax, ['high']].values.max()
            # if SKMain.axis12k_ymax != ymax:
            #     SKMain.axis12k_ymax = ymax        
            #     SKMain.draw12k.setYRange(SKMain.axis12k_ymin,SKMain.axis12k_ymax)


    def OnNotifyBest5(self,sMarketNo,sStockidx,nBestBid1,nBestBidQty1,nBestBid2,nBestBidQty2,nBestBid3,nBestBidQty3,nBestBid4,nBestBidQty4,nBestBid5,nBestBidQty5,nExtendBid,nExtendBidQty,nBestAsk1,nBestAskQty1,nBestAsk2,nBestAskQty2,nBestAsk3,nBestAskQty3,nBestAsk4,nBestAskQty4,nBestAsk5,nBestAskQty5,nExtendAsk,nExtendAskQty,nSimulate):
        # total_dict={'bid_dict':{int(nBestBid1/100):int(nBestBidQty1),int(nBestBid2/100):int(nBestBidQty2),int(nBestBid3/100):int(nBestBidQty3),int(nBestBid4/100):int(nBestBidQty4),int(nBestBid5/100):int(nBestBidQty5)},
        # 'ask_dict':{int(nBestAsk1/100):int(nBestAskQty1),int(nBestAsk2/100):int(nBestAskQty2),int(nBestAsk3/100):int(nBestAskQty3),int(nBestAsk4/100):int(nBestAskQty4),int(nBestAsk5/100):int(nBestAskQty5)}}
        total_dict={'買量':{0:nBestBidQty1,1:nBestBidQty2,2:nBestBidQty3,3:nBestBidQty4,4:nBestBidQty5},
                    '買價':{0:int(nBestBid1/100),1:int(nBestBid2/100),2:int(nBestBid3/100),3:int(nBestBid4/100),4:int(nBestBid5/100)},
                    '賣價':{0:int(nBestAsk1/100),1:int(nBestAsk2/100),2:int(nBestAsk3/100),3:int(nBestAsk4/100),4:int(nBestAsk5/100)},
                    '賣量':{0:nBestAskQty1,1:nBestAskQty2,2:nBestAskQty3,3:nBestAskQty4,4:nBestAskQty5}}
        
        # start = time.time()
        # SKMain.bestfive.loc[0:4,'買量'].map(lambda x: x.setText(str(total_dict['買量'][SKMain.bestfive['買量'][SKMain.bestfive['買量'] == x].index[0]])))
        # SKMain.bestfive.loc[0:4,'買價'].map(lambda x: x.setText(str(total_dict['買價'][SKMain.bestfive['買價'][SKMain.bestfive['買價'] == x].index[0]])))
        # SKMain.bestfive.loc[0:4,'賣價'].map(lambda x: x.setText(str(total_dict['賣價'][SKMain.bestfive['賣價'][SKMain.bestfive['賣價'] == x].index[0]])))
        # SKMain.bestfive.loc[0:4,'賣量'].map(lambda x: x.setText(str(total_dict['賣量'][SKMain.bestfive['賣量'][SKMain.bestfive['賣量'] == x].index[0]])))
        for (t, x) in SKMain.bestfive.loc[0:4,['買量','買價','賣價','賣量']].iterrows():
            SKMain.bestfive.at[t,'買量']=str(total_dict['買量'][t])
            SKMain.bestfive.at[t,'買價']=str(total_dict['買價'][t])
            SKMain.bestfive.at[t,'賣價']=str(total_dict['賣價'][t])
            SKMain.bestfive.at[t,'賣量']=str(total_dict['賣量'][t])
            # print(x.買量,x.買價,x.賣價, x.賣量)
            # x.買量.setText(str(total_dict['買量'][t]))
            # x.買價.setText(str(total_dict['買價'][t]))
            # x.賣價.setText(str(total_dict['賣價'][t]))
            # x.賣量.setText(str(total_dict['賣量'][t]))

        bidQty = total_dict['買量'].values()
        askQty = total_dict['賣量'].values()
        SKMain.bestfive.at[5,'買量']=str(int(sum(bidQty)))
        SKMain.bestfive.at[5,'賣量']=str(int(sum(askQty)))
        SKMain.bestfive.at[5,'買價']=str('')
        SKMain.bestfive.at[5,'賣價']=str('')
        # print(SKMain.bestfive)
        SKMain.Dom1model.UpdateData(SKMain.bestfive)

        # C = time.time()-start
        # if len(SKMain.timeC)==1000:
        #         SKMain.timeC.pop(0)
        #         SKMain.timeC.append(C)
        # else:
        #     SKMain.timeC.append(C)
        # if (sum(SKMain.timeC)/len(SKMain.timeC))>0:
        #     Cavg = str(int(1/(sum(SKMain.timeC)/len(SKMain.timeC))))
            # SKMain.draw12k.setLabel('top','5檔: '+Cavg)
        # else:
        #     pass
        # 更新點
    def OnNotifyFutureTradeInfo(self,bstrStockNo,sMarketNo,sStockidx,nBuyTotalCount,nSellTotalCount,nBuyTotalQty,nSellTotalQty,nBuyDealTotalCount,nSellDealTotalCount): 
        # print(nBuyTotalCount,nSellTotalCount,nBuyTotalQty,nSellTotalQty,nBuyDealTotalCount,nSellDealTotalCount)
        # 'ComQty','ComCont','DealCont','DealQty'
        MP_dict = {'ComCont':{0:nBuyTotalCount,1:nSellTotalCount,2:int(nSellTotalCount-nBuyTotalCount)},
        'ComQty':{0:nBuyTotalQty,1:nSellTotalQty,2:int(nBuyTotalQty-nSellTotalQty)},
        'DealCont':{0:nBuyDealTotalCount,1:nSellDealTotalCount,2:int(nSellDealTotalCount-nBuyDealTotalCount)}}
        # columns=['ComQty','ComCont','DealCont','DealQty']
        for key in MP_dict:
            i = 0
            while i < 3:
                # SKMain.MPower.at[i,key]=MP_dict[key][i]
                SKMain.MPower_pawndf.at[i,key].setText(str(MP_dict[key][i]))
                i+=1
        for (t, x) in SKMain.MPower.loc[0:2,['ComQty','ComCont','DealCont']].iterrows():
            x.ComQty.setText(str(MP_dict['ComQty'][t]))
            x.ComCont.setText(str(MP_dict['ComCont'][t]))
            x.DealCont.setText(str(MP_dict['DealCont'][t]))
            if t == 2 and SKMain.Future.mindf is not None:
                SKMain.Future.mindf.at[SKMain.Future.minlastidx,'big']=MP_dict['ComQty'][t]
                SKMain.Future.mindf.at[SKMain.Future.minlastidx,'small']=MP_dict['ComCont'][t]
                if MP_dict['ComQty'][t]>0:
                    x.ComQty.setBackground(Qt.red)
                    SKMain.MPower_pawndf.at[t,'ComQty'].setBackground(Qt.red)
                else:
                    x.ComQty.setBackground(Qt.green)
                    SKMain.MPower_pawndf.at[t,'ComQty'].setBackground(Qt.green)
                if MP_dict['ComCont'][t]>0:
                    x.ComCont.setBackground(Qt.red)
                    SKMain.MPower_pawndf.at[t,'ComCont'].setBackground(Qt.red)
                else:
                    x.ComCont.setBackground(Qt.green)
                    SKMain.MPower_pawndf.at[t,'ComCont'].setBackground(Qt.green)
                if MP_dict['DealCont'][t]>0:
                    x.DealCont.setBackground(Qt.red)
                    SKMain.MPower_pawndf.at[t,'DealCont'].setBackground(Qt.red)
                else:
                    x.DealCont.setBackground(Qt.green)
                    SKMain.MPower_pawndf.at[t,'DealCont'].setBackground(Qt.green)




# comtypes使用此方式註冊callback
SKQuoteEvent = SKQuoteLibEvents()
SKQuoteLibEventHandler = comtypes.client.GetEvents(skQ, SKQuoteEvent)
SKOrderEvent = SKOrderLibEvent()
SKOrderLibEventHandler = comtypes.client.GetEvents(skO, SKOrderEvent)
SKReplyEvent = SKReplyLibEvent()
SKReplyLibEventHandler = comtypes.client.GetEvents(skR, SKReplyEvent)

if __name__ == "__main__":
    SKApp = QApplication(sys.argv)
    SKMain = SKMainWindow()
    SKMain.show()
    sys.exit(SKApp.exec_())
