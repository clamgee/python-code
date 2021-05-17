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
        self.Bill = []
        self.fOrder = sk.FUTUREORDER()
        self.timestart = ''
        self.timeend = ''
        self.timeA=[]
        self.timeB=[]
        # 圖形化設定
        # 12K圖示宣告
        self.GL12K=pg.GraphicsLayout()
        self.GV1.setCentralItem(self.GL12K)
        self.drawmain = self.GL12K.addPlot()
        self.drawmain.showAxis('right',show=True)
        self.drawmain.showAxis('left',show=False)
        self.axis_xmin = 0
        self.axis_xmax = 100
        self.axis_ymin = 0
        self.axis_ymax = 100
        self.drawmain.setXRange(self.axis_xmin,self.axis_xmax)
        self.drawmain.setYRange(self.axis_ymin,self.axis_ymax)
        # 下單參數 Future structure
        self.trade_act = -1
        self.OrderPrice = ''
        self.ReplyComplete = False
        # 介面導入
        self.SKLoginUI()  # 登入介面
        self.SKMessageFunc()  # 系統訊息介面
        self.RightUI()  # 權益數介面
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

    def DrawmainUpdate(self):
        xmax = int(len(self.Kitem.pictures))
        if self.axis_xmax != xmax:
            self.axis_xmax = xmax
            xmin = int(max(0, xmax - self.Kitem.countK))
            self.axis_xmin = xmin 
            self.drawmain.setXRange(self.axis_xmin,self.axis_xmax)
        ymin = self.Kitem.data.loc[self.axis_xmin:self.axis_xmax, ['low']].values.min()
        ymax = self.Kitem.data.loc[self.axis_xmin:self.axis_xmax, ['high']].values.max()
        if self.axis_ymin != ymin or self.axis_ymax != ymax:
            self.axis_ymin = ymin
            self.axis_ymax = ymax        
            self.drawmain.setYRange(self.axis_ymin,self.axis_ymax)
            # xdate = self.Kitem.data.ndatetime.dt.strftime('%Y-%m-%d %H:%M:%S')
            # myAxis = pg.AxisItem('buttom')


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
        self.Bill = pd.DataFrame(np.arange(39).reshape(39), columns=['Right'])  # 期貨權益數
        i = 0
        while i < self.Bill.shape[0]:
            self.Bill.loc[i, 'Right'] = QTableWidgetItem('')
            self.Bill.loc[i, 'Right'].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            i += 1
        i = 1
        j = 0
        while i < self.Right_TB.rowCount():
            self.Right_TB.setItem(i, 0, self.Bill.loc[j, 'Right'])
            j += 1
            self.Right_TB.setItem(i, 1, self.Bill.loc[j, 'Right'])
            j += 1
            self.Right_TB.setItem(i, 2, self.Bill.loc[j, 'Right'])
            j += 1
            i += 2

    # 權益數介面結束
    # 閃電下單
    def DomTableUI(self):
        self.DomTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.DomTable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.DomTable.setHorizontalHeaderLabels(['買價', '成交價', '賣價'])
        self.bestfive = pd.DataFrame(np.arange(27).reshape(27), columns=['close'])
        self.bestfive['bid'] = 0
        self.bestfive['ask'] = 0
        self.bestfive = self.bestfive[['close', 'bid', 'ask']].astype(int)
        self.bestfive['closeTBitem'] = ''
        self.bestfive['bidTBitem'] = ''
        self.bestfive['askTBitem'] = ''
        self.lastclose = []
        self.lastbidlist = []
        self.lastasklist = []
        # while i < self.bestfive.shape[0]:
        i = 0
        while i < 27:
            self.bestfive.loc[i, 'closeTBitem'] = QTableWidgetItem('')
            self.DomTable.setItem(i, 1, self.bestfive.loc[i, 'closeTBitem'])
            self.bestfive.loc[i, 'bidTBitem'] = QTableWidgetItem('')
            self.DomTable.setItem(i, 0, self.bestfive.loc[i, 'bidTBitem'])
            self.bestfive.loc[i, 'askTBitem'] = QTableWidgetItem('')
            self.DomTable.setItem(i, 2, self.bestfive.loc[i, 'askTBitem'])
            self.bestfive.loc[i, 'closeTBitem'].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.bestfive.loc[i, 'bidTBitem'].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.bestfive.loc[i, 'askTBitem'].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            i += 1
        self.bestfive.loc[13, 'closeTBitem'].setBackground(Qt.yellow)
        self.bestfive.loc[13, 'bidTBitem'].setBackground(Qt.yellow)
        self.bestfive.loc[13, 'askTBitem'].setBackground(Qt.yellow)

    def DomTableFillFunc(self, nclose, bid_dict, ask_dict):
        if self.bestfive.loc[13, 'close'] != nclose:
            self.bestfive['close'] = self.bestfive['close'].map(
                lambda x: nclose + 13 - (self.bestfive['close'][self.bestfive['close'] == x].index[0]))
            self.bestfive['closeTBitem'].map(lambda x: x.setText(str(
                self.bestfive.loc[self.bestfive['closeTBitem'][self.bestfive['closeTBitem'] == x].index[0], 'close'])))
        self.bestfive['bid'] = self.bestfive['close'].map(bid_dict).fillna(value=0).astype(int)
        self.bestfive['ask'] = self.bestfive['close'].map(ask_dict).fillna(value=0).astype(int)
        asklist = self.bestfive['ask'][self.bestfive['ask'] != 0].index.tolist()
        bidlist = self.bestfive['bid'][self.bestfive['bid'] != 0].index.tolist()
        # # print('bid: ',self.bestfive['bid'].to_dict())
        self.lastbidlist = list(set(self.lastbidlist + bidlist))
        self.lastasklist = list(set(self.lastasklist + asklist))
        self.bestfive.loc[self.lastbidlist, 'bidTBitem'].map(lambda x: x.setText(
            str(self.bestfive.loc[self.bestfive['bidTBitem'][self.bestfive['bidTBitem'] == x].index[0], 'bid'])) if
        self.bestfive.loc[
            self.bestfive['bidTBitem'][self.bestfive['bidTBitem'] == x].index[0], 'bid'] != 0 else x.setText(''))
        self.bestfive.loc[self.lastasklist, 'askTBitem'].map(lambda x: x.setText(
            str(self.bestfive.loc[self.bestfive['askTBitem'][self.bestfive['askTBitem'] == x].index[0], 'ask'])) if
        self.bestfive.loc[
            self.bestfive['askTBitem'][self.bestfive['askTBitem'] == x].index[0], 'ask'] != 0 else x.setText(''))
        # self.lastclose=self.bestfive['close'].tolist()
        self.lastbidlist = bidlist
        self.lastasklist = asklist

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
        self.ndetialmsg = FuncUI.MessageDialog(nstock)
        self.TDetailbtn.clicked.connect(self.ndetialmsg.show)
        # self.ndetialmsg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # self.ndetialmsg.show()
        self.DomTableUI()  # 閃電下單介面
        self.Kitem = KlineUi.CandlestickItem()
        # self.Kui = KlineUi.KlineWidget(nstock)
        # self.Kui.addItem(self.Kitem)
        self.drawmain.addItem(self.Kitem)
        self.Kitem.set_data(self.Future.lastidx,self.Future.High,self.Future.Low,self.Future.contractkpd)
        # self.Kitem.set_data(self.Future.contractkpd)
        # self.SKQThread = SKQuoteThread()
        # self.SKQThread.start()
        # self.HisKlineThrd=His_KLlineThread()
        # self.HisKlineThrd.start()
        self.TableThrd = TableThread()
        if self.TableThrd.isRunning:
            self.TableThrd.quit()
            pass
        else:
            self.TableThrd.start()
        self.DrawmainUpdate()        

    # 商品訂閱結束
    # 委託未平倉回報資料
    def Reply_Open_Fnc(self):
        self.replypd = pd.DataFrame(
            columns=['商品名稱', '買賣', '委託價格', '委託口數', '委託狀態', '成交口數', '取消口數', '倉位', '條件', '價位格式', '委託序號', '委託書號', '委託日期',
                     '委託時間', '交易時段'])
        self.ReplyCRpdMode = PandasModel()
        self.openpd = pd.DataFrame(
            columns=['市場別', '帳號', '商品', '買賣別', '未平倉部位', '當沖未平倉部位', '平均成本', '一點價值', '單口手續費', '交易稅'])
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
                self.OrderFunc(self, Account, Commodity, TradeAct, TradeType, OderPrice, Qty, InterestType)

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

    def setdata(self, data):
        self._data = data
        self.layoutAboutToBeChanged.emit()  # 建立變更資料通知訊號發射
        self.dataChanged.emit(self.createIndex(0, 0),
                              self.createIndex(self.rowCount(), self.columnCount()))  # 資料變更區域訊號發射
        self.layoutChanged.emit()  # 資料變更訊號發射

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
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
            m_nCode = skO.GetOpenInterest(bstrLogInID, SKMain.IBAccount)
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
        # print('持倉回報: ',bstrData,' 次數:',SKMain.test)
        Line = bstrData.split(',')
        if Line[0] == 'M003 NO DATA':
            print('No Data pass')
            pass
        elif Line[0] == '##':
            SKMain.OpenCRpdMode.setdata(SKMain.openpd)
            SKMain.Open_TBW.setModel(SKMain.OpenCRpdMode)
            print('OnOpenInterest end pass')
            pass
        else:
            SKMain.openpd = SKMain.openpd.append(pd.DataFrame(Line,columns=['市場別', '帳號', '商品', '買賣別', '未平倉部位', '當沖未平倉部位','平均成本', '一點價值', '單口手續費', '交易稅']))
        # SKMain.test+=1
        # i=0
        # Line=bstrData.split(',')
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
        SKMain.ReplyCRpdMode.setdata(SKMain.replypd)
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
            SKMain.ReplyCRpdMode.setdata(SKMain.replypd)

    def OnSmartData(self, bstrUserID, bstrData):
        print(bstrUserID, '智動回報:', bstrData)


def repeatQuote(func):
    def wrapper():
        func()

    return wrapper


class SKQuoteLibEvents:

    def OnConnection(self, nKind, nCode):
        if (nKind == 3001):
            strMsg = "Connected!"
        elif (nKind == 3002):
            strMsg = "DisConnected!"
        elif (nKind == 3003):
            strMsg = "Stocks ready!"
            time.sleep(5)
            SKMain.commodityFnc()
        elif (nKind == 3021):
            strMsg = "Connect Error!"
        print(strMsg)
        SKMain.SKMessage.textBrowser.append(strMsg)

    def OnNotifyServerTime(self, sHour, sMinute, sSecond, nTotal):
        nTime = QTime(sHour, sMinute, sSecond)
        rTime = QTime(8,30,00)
        if rTime == nTime:
            SKMain.ConnectFun()
        jTime = QTime(13, 50, 00)
        # jTime=datetime.datetime.strptime('13:50:00','%H:%M:%S').time()
        if nTime == jTime and SKMain.Future.ticksdf is not None:
            filename = '../data/Ticks' + SKMain.Future.ticksdf.iloc[-1, 0].date().strftime('%Y-%m-%d') + '.txt'
            SKMain.Future.ticksdf.to_csv(filename, header=False, index=False)
            result=SKMain.Future.contractkpd.drop(columns=['high_avg','low_avg'])            
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
            SKMain.Future.Ticks(lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty)
            # print(lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty)
            if SKMain.timeend == '' and lTimehms == 45958:
                SKMain.timeend = time.time()
                print(round((SKMain.timeend-SKMain.timestart),3))

            # strMsg = str(SKMain.Future.contractkpd.iloc[-1:].values)
            # SKMain.ndetialmsg.textBrowser.append(strMsg)

    def OnNotifyTicks(self, sMarketNo, sStockIdx, nPtr, lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty, nSimulate):
        # strMsg=str(lDate)+','+str(lTimehms)+','+str(lTimemillismicros)+','+str(nBid)+','+str(nAsk)+','+str(nClose)+','+str(nQty)
        if nSimulate == 0:
            # SKMain.newThread.KLine_signal.emit(str(lDate),int(lTimehms),int(lTimemillismicros),int(nBid),int(nAsk),int(nClose),int(nQty))
            # print('ThreadName: ',QThread.currentThread().objectName(),'ThreadID: ',int(QThread.currentThreadId()))
            start = pg.time()
            SKMain.Future.Ticks(lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty)
            A = pg.time()-start
            strMsg = str(SKMain.Future.contractkpd.iloc[-1:].values)
            # SKMain.ndetialmsg.textBrowser.append(strMsg)
            start = pg.time()
            SKMain.Kitem.set_data(SKMain.Future.lastidx,SKMain.Future.High,SKMain.Future.Low,SKMain.Future.contractkpd.tail(SKMain.Future.lastidx+1-SKMain.Kitem.lastidx))
            xmax = SKMain.Future.lastidx + 1
            if SKMain.axis_xmax != xmax:
                SKMain.DrawmainUpdate()
            B = pg.time()-start
            if len(SKMain.timeA)==100 or len(SKMain.timeB)==100:
                SKMain.timeA.pop(0)
                SKMain.timeA.append(A)
                SKMain.timeB.pop(0)
                SKMain.timeB.append(B)
            else:
                SKMain.timeA.append(A)
                SKMain.timeB.append(B)
            SKMain.drawmain.setLabel('top',str(np.mean(SKMain.timeA).round(5))+" , "+str(np.mean(SKMain.timeB).round(5)))
            # if SKMain.axis_xmax != xmax:
            #     SKMain.axis_xmax = xmax
            #     xmin = int(max(0, xmax - SKMain.Kitem.countK))
            #     SKMain.axis_xmin = xmin 
            #     SKMain.drawmain.setXRange(SKMain.axis_xmin,SKMain.axis_xmax)
            # ymin = SKMain.Kitem.data.loc[SKMain.axis_xmin:SKMain.axis_xmax, ['low']].values.min()
            # if SKMain.axis_ymin != ymin:
            #     SKMain.axis_ymin = ymin
            #     SKMain.drawmain.setYRange(SKMain.axis_ymin,SKMain.axis_ymax)
            # ymax = SKMain.Kitem.data.loc[SKMain.axis_xmin:SKMain.axis_xmax, ['high']].values.max()
            # if SKMain.axis_ymax != ymax:
            #     SKMain.axis_ymax = ymax        
            #     SKMain.drawmain.setYRange(SKMain.axis_ymin,SKMain.axis_ymax)


    def OnNotifyBest5(self,sMarketNo,sStockidx,nBestBid1,nBestBidQty1,nBestBid2,nBestBidQty2,nBestBid3,nBestBidQty3,nBestBid4,nBestBidQty4,nBestBid5,nBestBidQty5,nExtendBid,nExtendBidQty,nBestAsk1,nBestAskQty1,nBestAsk2,nBestAskQty2,nBestAsk3,nBestAskQty3,nBestAsk4,nBestAskQty4,nBestAsk5,nBestAskQty5,nExtendAsk,nExtendAskQty,nSimulate):
        total_dict={'bid_dict':{int(nBestBid1/100):int(nBestBidQty1),int(nBestBid2/100):int(nBestBidQty2),int(nBestBid3/100):int(nBestBidQty3),int(nBestBid4/100):int(nBestBidQty4),int(nBestBid5/100):int(nBestBidQty5)},
        'ask_dict':{int(nBestAsk1/100):int(nBestAskQty1),int(nBestAsk2/100):int(nBestAskQty2),int(nBestAsk3/100):int(nBestAskQty3),int(nBestAsk4/100):int(nBestAskQty4),int(nBestAsk5/100):int(nBestAskQty5)}}
        SKMain.TableThrd.Table_signal.emit(SKMain.Future.contractkpd.iloc[-1,4],total_dict)
        # 更新點


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
