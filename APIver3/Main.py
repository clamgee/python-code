import sys,os,time
from PySide6.QtCore import QObject, QThreadPool, Signal,Slot,QTime,Qt,QThread,QAbstractTableModel,QFile,Property
from PySide6.QtWidgets import QMainWindow,QApplication,QTableWidgetItem,QMessageBox,QHeaderView
from PySide6.QtGui import QAction
from PySide6 import QtCore
from pandas.core.indexing import need_slice
import pyqtgraph as pg
import pandas as pd
import numpy as np
import multiprocessing as mp
import re
# 使用SKCOM元件
import comtypes.client
import comtypes.gen.SKCOMLib as sk
# SKCOM dll物件導入
skC = comtypes.client.CreateObject(sk.SKCenterLib, interface=sk.ISKCenterLib)
skO = comtypes.client.CreateObject(sk.SKOrderLib, interface=sk.ISKOrderLib)
skQ = comtypes.client.CreateObject(sk.SKQuoteLib, interface=sk.ISKQuoteLib)
skR = comtypes.client.CreateObject(sk.SKReplyLib, interface=sk.ISKReplyLib)
# 外部 自寫模組
from UI.MainWindow import Ui_CapitalAPI
import FuncUI,FuncClass,Config_dict,tickstokline,GlobalVar,KlineItem

# 主視窗物件
class SKMainWindow(QMainWindow):
    Candle12KItem_signal = Signal()
    CandleMinuteKItem_signal = Signal()
    CandleMinuteDealMinusItem_signal = Signal()
    CandleMinuteBigItem_signal = Signal()
    CandleMinuteSmallItem_signal = Signal()
    def __init__(self):
        super(SKMainWindow, self).__init__()
        self.MainUi = Ui_CapitalAPI()
        self.MainUi.setupUi(self)
        self.showMaximized() #主視窗最大化
        # 介面導入
        self.SKMessageUI()  # 系統訊息介面
        self.SKRightUI() #權益數介面
        self.SKLoginUI()  # 登入介面
        self.Setup_CandleMinuteKDrawUI() #分鐘線設定
        # self.SKCommodityUI(self) #五檔介面
        # ManuBar連結
        self.MainUi.actionLogin.triggered.connect(self.Login.ui.show)  # 登入介面連結
        self.MainUi.SysDetail.triggered.connect(self.SKMessage.ui.show) #系統資訊介面連結
        self.MainUi.Connectbtn.triggered.connect(self.ConnectFunc) #SKCom 報價連線
        self.MainUi.Disconnectbtn.triggered.connect(self.disconnectFunc) #SKCom 報價斷線        
        #圖形訊號連結
        self.Candle12KDraw_Build_None = True #12K圖形介面尚未初始化
        self.Candle12KItem_signal.connect(self.Candle12KDrawFunc)
        self.CandleMinuteKDraw_Build_None = True #分鐘K圖形介面尚未初始化
        self.CandleMinuteKItem_signal.connect(self.CandleMinuteKDrawFunc)
        self.CandleMinuteDealMinusDraw_Build_None = True #多空力道圖形介面尚未初始化
        self.CandleMinuteDealMinusItem_signal.connect(self.CandleMinuteDealMinusDrawFunc)
        self.CandleMinuteBigDraw_Build_None = True #大單圖形介面尚未初始化
        self.CandleMinuteBigItem_signal.connect(self.CandleMinuteBigDrawFunc)
        self.CandleMinuteSmallDraw_Build_None = True #小單圖形介面尚未初始化
        self.CandleMinuteSmallItem_signal.connect(self.CandleMinuteSmallDrawFunc)
        # 帳號處理
        self.SKID = '未登入'  # 登入帳號
        self.IBAccount = ''  # 期貨帳號
        self.MainUi.statusBar.showMessage('帳號:' + self.SKID)

    def SKLoginUI(self):
        self.Login = FuncUI.LoginDialog() #登入介面
        self.Login.ui.show()
        self.Login.ui.LoginConfirmbtn.accepted.connect(self.LoginFuncAccept)
    
    def SKMessageUI(self):
        self.SKMessage = FuncUI.MessageDialog('系統訊息')  # 設定系統訊息介面
        self.SKMessage.ui.show()
    
    def SKCommodityUI(self,parent):
        self.SKCommodity = FuncUI.CommodityForm(parent)
        self.SKCommodity.ui.show()
        self.SKCommodity.ui.commoditybtn.clicked.connect(self.commodityFunc)
        self.SKCommodity.ui.TDetailbtn.clicked.connect(self.SKTraDetailUI)
        self.SKCommodity.ui.Market_comboBox.currentIndexChanged.connect(self.MarketlistchangeFunc)
        self.DomDataProc = FuncClass.DomDataProcess(GlobalVar.Dom_Event,GlobalVar.DomDataQueue,GlobalVar.NS)
        self.DomDataProc.start()
        print('報價五檔 Pid: ',self.DomDataProc.pid)
        self.DomModel = FuncClass.PandasModel()
        self.DomModel.UpdateData(GlobalVar.NS.Domdf)
        self.SKCommodity.ui.DomTable.setModel(self.DomModel)
        self.DomModelThread = FuncClass.DomTableUpdateThread(self)
        self.DomModelThread.start()
        self.MPTableBigSmallThread = FuncClass.MPTableBigSmallThread(self)
        self.MPTableBigSmallThread.start()
        self.MPTablePowerThread = FuncClass.MPTablePowerThread(self)
        self.MPTablePowerThread.start()
    
    def SKRightUI(self):
        self.MainUi.Right_TB.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.MainUi.Right_TB.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.Bill = pd.DataFrame(np.arange(41).reshape(41), columns=['Right'])  # 期貨權益數 DataFrame        
        i = 0
        while i < self.Bill.shape[0]:
            self.Bill.at[i, 'Right'] = QTableWidgetItem('')
            self.Bill.at[i, 'Right'].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            i += 1
        i = 1
        j = 0
        while i < self.MainUi.Right_TB.rowCount():
            self.MainUi.Right_TB.setItem(i, 0, self.Bill.at[j, 'Right'])
            j += 1
            if j >= self.Bill.shape[0]:
                break
            self.MainUi.Right_TB.setItem(i, 1, self.Bill.at[j, 'Right'])
            j += 1
            if j >= self.Bill.shape[0]:
                break
            self.MainUi.Right_TB.setItem(i, 2, self.Bill.at[j, 'Right'])
            j += 1
            if j >= self.Bill.shape[0]:
                break
            i += 2
    # 權益數介面結束
    # 交易明細介面
    def SKTraDetailUI(self):
        self.SKTraDetail = FuncUI.MessageDialog('交易明細') #交易明細
        self.SKTraDetail.ui.show()
    # 交易明細介面結束
    @Slot()#登入功能鍵
    def LoginFuncAccept(self):
        try:
            skC.SKCenterLib_SetLogPath(os.path.split(os.path.realpath(__file__))[0] + '\\CapitalLog_Quote')
            __ID = self.Login.ui.LoginID.text().replace(' ', '')
            __PW = self.Login.ui.LoginPW.text().replace(' ', '')
            m_nCode1 = skC.SKCenterLib_Login(__ID, __PW)
            if m_nCode1 == 0:
                self.SKID = __ID
                self.MainUi.statusBar.showMessage('帳號:' + str(self.SKID))
                self.SKMessage.ui.textBrowser.append('登入成功，帳號: ' + str(self.SKID))
            else:
                strMsg=skC.SKCenterLib_GetReturnCodeMessage(m_nCode1)
                self.SKMessage.ui.textBrowser.append('登入失敗,錯誤碼:'+strMsg)
            m_nCode2 = skO.SKOrderLib_Initialize()
            self.SKMessage.ui.textBrowser.append('群益API初始化: '+str(m_nCode2))
            m_nCode3 = skO.GetUserAccount()
            self.SKMessage.ui.textBrowser.append('GetUserAccount: '+str(m_nCode3))
            if (m_nCode1+m_nCode2+m_nCode3) == 0:
                self.Reply_Open_Fnc()
                self.Login.ui.close()
            else:
                self.SKMessage.ui.textBrowser.append('登入失敗，程式未觸發')
                ID = '未登入'
                pass
        except Exception as e:
            self.SKMessage.ui.textBrowser.append('發生未知錯誤:' + e)
            pass
    # 登入功能結束
    # 委託未平倉回報資料表設定格式
    def Reply_Open_Fnc(self):
        self.replypd = pd.DataFrame(
        columns=['商品名稱', '買賣', '委託價格', '委託口數', '委託狀態', '成交口數', '取消口數', '倉位', '條件', '價位格式', '委託序號', '委託書號', '委託日期',
                    '委託時間', '交易時段'])
        self.ReplyCRpdMode = FuncClass.PandasModel()
        self.openpd = pd.DataFrame(
            columns=['市場別', '期貨帳號', '商品', '買賣別', '未平倉部位', '當沖未平倉部位', '平均成本', '一點價值', '單口手續費', '交易稅','登入帳號'])
        self.OpenCRpdMode = FuncClass.PandasModel()
        # 回報完成確認參數
        self.ReplyComplete = False
        self.onOpenInterestReplytimes = 0
    # 交易委託和未平倉設定結束
    # 報價系統連線功能
    @Slot()
    def ConnectFunc(self):
        m_nCode = skQ.SKQuoteLib_EnterMonitor()
        if m_nCode==0:
            strMsg = '報價已連線!!!'
            self.SKCommodityUI(self) #商品+5檔+大小單+下單介面
            self.MainUi.CommodityUIbtn.setEnabled(True)
            self.MainUi.CommodityUIbtn.triggered.connect(self.SKCommodity.ui.show) #商品+5檔+大小單+下單介面
        else:
            strMsg = skC.SKCenterLib_GetReturnCodeMessage(m_nCode)
        self.SKMessage.ui.textBrowser.append('EnterMonitor: '+strMsg)
    @Slot()
    def disconnectFunc(self):
        m_nCode = skQ.SKQuoteLib_LeaveMonitor()
        if m_nCode == 0:
            strMsg='報價已斷線!!!'
            self.MainUi.CommodityUIbtn.setEnabled(False)
        else:
            strMsg = skC.SKCenterLib_GetReturnCodeMessage(m_nCode)
        self.SKMessage.ui.textBrowser.append('LeaveMonitor: '+strMsg)
    # 報價系統結束
    # 商品選單
    @Slot()
    def MarketlistchangeFunc(self):
        nCode=skQ.SKQuoteLib_IsConnected()
        if nCode == 0 :
            m_nCode=skQ.SKQuoteLib_RequestStockList(self.SKCommodity.ui.Market_comboBox.currentIndex())
            if m_nCode != 0:
                self.SKMessage.ui.textBrowser.append('商品取得列表錯誤: %s',skC.SKCenterLib_GetReturnCodeMessage(m_nCode))
        elif nCode==2:
            self.SKMessage.ui.textBrowser.append('資料下載中...')
        else:
            self.SKMessage.ui.textBrowser.append('報價未連線!!!')       

    # 商品訂閱
    @Slot()
    def commodityFunc(self):
        bstrStockNo = self.SKCommodity.ui.Commodity_comboBox.currentText().split(',')[0].replace(' ','')
        pSKStock=sk.SKSTOCKLONG()
        skQ.SKQuoteLib_GetStockByNoLONG (bstrStockNo,pSKStock)
        GlobalVar.CandleTarget.set(bstrStockNo)
        setattr(GlobalVar.CandleTarget,'commodityIndex',pSKStock.nStockIdx)
        globals()['DataQueue'+str(pSKStock.nStockIdx)] = mp.Queue()
        setattr(GlobalVar.SaveNotify,'commodityIndex',pSKStock.nStockIdx) 
        setattr(globals()['DataQueue'+str(pSKStock.nStockIdx)],'commodityIndex',pSKStock.nStockIdx)
        globals()['Tick12KQueue'+bstrStockNo] = mp.Queue()
        globals()['MinuteQueue'+bstrStockNo] = mp.Queue()
        PassListTuple = (globals()['DataQueue'+str(pSKStock.nStockIdx)],globals()['Tick12KQueue'+bstrStockNo],globals()['MinuteQueue'+bstrStockNo],GlobalVar.PowerQueue,GlobalVar.NS,GlobalVar.SaveNotify)
        Pass12KTuple =(globals()['Tick12KQueue'+bstrStockNo],GlobalVar.CandleTarget,GlobalVar.CandleItem12K_Event,GlobalVar.NS,GlobalVar.SaveNotify)
        PassMinuteKTuple =(globals()['MinuteQueue'+bstrStockNo],GlobalVar.CandleTarget,GlobalVar.CandleItemMinute_Event,GlobalVar.CandleMinuteDealMinus_Event,GlobalVar.CandleMinuteBig_Event,GlobalVar.CandleMinuteSmall_Event,GlobalVar.NS)
        self.DataProc = FuncClass.MyProcess(tickstokline.DataToTicks,bstrStockNo,pSKStock.nStockIdx,PassListTuple)
        self.DataProc.start()
        self.Tick12KProc = FuncClass.MyProcess(tickstokline.TicksTo12K,bstrStockNo,pSKStock.nStockIdx,Pass12KTuple)
        self.Tick12KProc.start()
        self.MinKProc = FuncClass.MyProcess(tickstokline.TicksToMinuteK,bstrStockNo,pSKStock.nStockIdx,PassMinuteKTuple)
        self.MinKProc.start()
        self.SKMessage.ui.textBrowser.append('Data Pid: {0}'.format(self.DataProc.pid))
        self.SKMessage.ui.textBrowser.append('Tick12K Pid: {0}'.format(self.Tick12KProc.pid))
        self.SKMessage.ui.textBrowser.append('MinK Pid: {0}'.format(self.MinKProc.pid))
        self.CandleItem12K = KlineItem.CandleItem()
        self.Candle12KDrawThread = FuncClass.Candle12KDrawThread(self.CandleItem12K,self.Candle12KItem_signal)
        self.Candle12KDrawThread.start()
        self.CandleMinuteKItem = KlineItem.CandleItem()
        self.CandleMinKDrawThread = FuncClass.CandleMinKDrawThread(self.CandleMinuteKItem,self.CandleMinuteKItem_signal)
        self.CandleMinKDrawThread.start()
        self.CandleDealMinusItem = KlineItem.BarItem()
        self.CandleMinuteDealMinusThread = FuncClass.CandleMinKDealMinusDrawThread(self.CandleDealMinusItem.set_data,self.CandleMinuteDealMinusItem_signal)
        self.CandleMinuteDealMinusThread.start()
        self.CandleMinuteBigItem = KlineItem.BarItem()
        self.CandleMinuteBigThread = FuncClass.CandleMinKBigDrawThread(self.CandleMinuteBigItem.set_data,self.CandleMinuteBigItem_signal)
        self.CandleMinuteBigThread.start()
        self.CandleMinuteSmallItem = KlineItem.BarItem()
        self.CandleMinuteSmallThread = FuncClass.CandleMinKSmallDrawThread(self.CandleMinuteSmallItem.set_data,self.CandleMinuteSmallItem_signal)
        self.CandleMinuteSmallThread.start()
        nCode=skQ.SKQuoteLib_RequestTicks(0, bstrStockNo)
        skQ.SKQuoteLib_RequestFutureTradeInfo(comtypes.automation.c_short(0),bstrStockNo)
        if sum(nCode) !=0 :
            strMsg=skC.SKCenterLib_GetReturnCodeMessage(sum(nCode))
            self.SKMessage.ui.textBrowser.append('商品訂閱錯誤: '+strMsg)
        else:
            self.SKMessage.ui.textBrowser.append('選擇商品: '+bstrStockNo+','+str(pSKStock.nStockIdx))        
    # 商品訂閱結束
    @Slot()
    def Candle12KDrawFunc(self):
        if self.Candle12KDraw_Build_None:
            self.Axis12k = pg.AxisItem(orientation='bottom')
            self.Candle12KDraw = self.MainUi.tab_TicksK.addPlot(row=0,col=0,axisItems={'bottom': self.Axis12k})
            self.Candle12KDraw.autoRange(True)
            self.Candle12KDraw.showAxis('right',show=True)
            self.Candle12KDraw.showAxis('left',show=False)
            self.Candle12KDraw.showGrid(x=False,y=True)
            self.Candle12KDraw.setMouseEnabled(x=False, y=False)
            self.Candle12KDraw.setMenuEnabled(False)
            self.Candle12KDraw.addItem(self.CandleItem12K)
            self.axis12k_xmax = len(self.CandleItem12K.pictures)
            self.axis12k_xmin = self.axis12k_xmax-self.CandleItem12K.countK
            self.axis12k_ymin = self.CandleItem12K.data.loc[self.axis12k_xmin:self.axis12k_xmax, ['low']].values.min()
            self.axis12k_ymax = self.CandleItem12K.data.loc[self.axis12k_xmin:self.axis12k_xmax, ['high']].values.max()
            self.Candle12KDraw.setXRange(self.axis12k_xmin,self.axis12k_xmax)
            self.Candle12KDraw.setYRange(self.axis12k_ymin,self.axis12k_ymax)
            self.MAHighLine=self.Candle12KDraw.plot(pen='y')
            self.MALowLine=self.Candle12KDraw.plot(pen='b')
            dict_tmp = self.CandleItem12K.data['ndatetime'][(self.CandleItem12K.data.volume!=12000) & (self.CandleItem12K.data.ndatetime.dt.hour>8) & (self.CandleItem12K.data.ndatetime.dt.hour<15)].dt.strftime('%Y-%m-%d %H:%M:%S').to_dict()
            self.Axis12k.setTicks([dict_tmp.items()])
            self.MAHighLine.setData(self.CandleItem12K.data.high_avg)
            self.MALowLine.setData(self.CandleItem12K.data.low_avg)
            self.Candle12KDraw_Build_None = False
        else:
            if self.axis12k_xmax != len(self.CandleItem12K.pictures):
                self.axis12k_xmax = len(self.CandleItem12K.pictures)
                self.axis12k_xmin = self.axis12k_xmax-self.CandleItem12K.countK
                self.axis12k_ymin = self.CandleItem12K.data.loc[self.axis12k_xmin:self.axis12k_xmax, ['low']].values.min()
                self.axis12k_ymax = self.CandleItem12K.data.loc[self.axis12k_xmin:self.axis12k_xmax, ['high']].values.max()
                self.Candle12KDraw.setXRange(self.axis12k_xmin,self.axis12k_xmax)
                self.Candle12KDraw.setYRange(self.axis12k_ymin,self.axis12k_ymax)
                dict_tmp = self.CandleItem12K.data['ndatetime'][(self.CandleItem12K.data.volume!=12000) & (self.CandleItem12K.data.ndatetime.dt.hour>8) & (self.CandleItem12K.data.ndatetime.dt.hour<15)].dt.strftime('%Y-%m-%d %H:%M:%S').to_dict()
                self.Axis12k.setTicks([dict_tmp.items()])
                self.MAHighLine.setData(self.CandleItem12K.data.high_avg)
                self.MALowLine.setData(self.CandleItem12K.data.low_avg)

            if self.axis12k_ymin > self.CandleItem12K.close or self.axis12k_ymax < self.CandleItem12K.close:
                self.axis12k_ymin = self.CandleItem12K.data.loc[self.axis12k_xmin:self.axis12k_xmax, ['low']].values.min()
                self.axis12k_ymax = self.CandleItem12K.data.loc[self.axis12k_xmin:self.axis12k_xmax, ['high']].values.max()
                self.Candle12KDraw.setYRange(self.axis12k_ymin,self.axis12k_ymax)
            
    def Setup_CandleMinuteKDrawUI(self):
        self.AxisMinute = pg.AxisItem(orientation='bottom')
        self.CandleMinuteKDraw = self.MainUi.tab_DayTrading.addPlot(row=0,col=0,axisItems={'bottom': self.AxisMinute})
        self.CandleMinuteKDraw.autoRange()
        now = time.localtime(time.time()).tm_hour
        if now>14 or now<8 :
            self.CandleMinuteKDraw.setXRange(0,840)
        elif now>=8 and now<15:
            self.CandleMinuteKDraw.setXRange(0,310)
        self.CandleMinuteKDraw.showAxis('right',show=True)
        self.CandleMinuteKDraw.showAxis('left',show=False)
        self.CandleMinuteKDraw.showGrid(x=False,y=True)
        self.AxisMinuteDealMinus = pg.AxisItem(orientation='bottom')
        self.CandleMinuteDealMinusDraw=self.MainUi.tab_DayTrading.addPlot(row=1,col=0,axisItems={'bottom': self.AxisMinuteDealMinus})
        self.CandleMinuteDealMinusDraw.autoRange(True)
        self.CandleMinuteDealMinusDraw.setXLink(self.CandleMinuteKDraw)
        self.CandleMinuteDealMinusDraw.showAxis('right',show=True)
        self.CandleMinuteDealMinusDraw.showAxis('left',show=False)
        self.CandleMinuteDealMinusDraw.showGrid(x=False,y=True)
        self.AxisMinuteBig = pg.AxisItem(orientation='bottom')
        self.CandleMinuteBigDraw=self.MainUi.tab_DayTrading.addPlot(row=3,col=0,axisItems={'bottom': self.AxisMinuteBig})
        self.CandleMinuteBigDraw.autoRange(True)
        self.CandleMinuteBigDraw.setXLink(self.CandleMinuteKDraw)
        self.CandleMinuteBigDraw.showAxis('right',show=True)
        self.CandleMinuteBigDraw.showAxis('left',show=False)
        self.CandleMinuteBigDraw.showGrid(x=False,y=True)
        self.AxisMinuteSmall = pg.AxisItem(orientation='bottom')
        self.CandleMinuteSmallDraw=self.MainUi.tab_DayTrading.addPlot(row=2,col=0,axisItems={'bottom': self.AxisMinuteSmall})
        self.CandleMinuteSmallDraw.autoRange(True)
        self.CandleMinuteSmallDraw.setXLink(self.CandleMinuteKDraw)
        self.CandleMinuteSmallDraw.showAxis('right',show=True)
        self.CandleMinuteSmallDraw.showAxis('left',show=False)
        self.CandleMinuteSmallDraw.showGrid(x=False,y=True)
        self.CandleMinuteKDraw.setMouseEnabled(x=False, y=False)
        self.CandleMinuteKDraw.setMenuEnabled(False)
        self.CandleMinuteDealMinusDraw.setMouseEnabled(x=False, y=False)
        self.CandleMinuteDealMinusDraw.setMenuEnabled(False)
        self.CandleMinuteBigDraw.setMouseEnabled(x=False, y=False)
        self.CandleMinuteBigDraw.setMenuEnabled(False)
        self.CandleMinuteSmallDraw.setMouseEnabled(x=False, y=False)
        self.CandleMinuteSmallDraw.setMenuEnabled(False)
        self.MainUi.tab_DayTrading.ci.layout.setRowStretchFactor(0,7)
        self.MainUi.tab_DayTrading.ci.layout.setRowStretchFactor(1,1)
        self.MainUi.tab_DayTrading.ci.layout.setRowStretchFactor(2,1)
        self.MainUi.tab_DayTrading.ci.layout.setRowStretchFactor(3,1)

    @Slot()
    def CandleMinuteKDrawFunc(self):
        if self.CandleMinuteKDraw_Build_None:
            self.CandleMinuteKDraw.addItem(self.CandleMinuteKItem)
            direct=os.path.abspath('../data')
            filelist = os.listdir('../data')
            file = filelist[-1]
            tmpdf = pd.read_csv(direct+'\\'+file,header=None,names=['ndatetime','nbid','nask','close','volume','deal'])
            self.yesterdayclose = tmpdf.at[tmpdf.last_valid_index(),'close']
            print(self.yesterdayclose)
            del tmpdf
            self.YCline = pg.InfiniteLine(angle=0, movable=False,pen='y')
            self.CandleMinuteKDraw.addItem(self.YCline)
            self.YCline.setPos(self.yesterdayclose)
            dict_tmp=self.CandleMinuteKItem.data['ndatetime'][self.CandleMinuteKItem.data.ndatetime.dt.minute==0].dt.strftime('%H:%M:%S').to_dict()
            self.AxisMinute.setTicks([dict_tmp.items()])
            self.AxisMinuteDealMinus.setTicks([dict_tmp.items()])
            del dict_tmp
            tmpline=self.CandleMinuteKItem.data.close.cumsum()
            self.avgline = tmpline.apply(lambda x: x/(tmpline[tmpline==x].index[0]+1))
            self.curve=self.CandleMinuteKDraw.plot(pen='w')
            self.curve.setData(self.avgline)
            del tmpline
            self.CandleMinuteKDrawYrectHigh = max(self.CandleMinuteKItem.data.high.max(),self.yesterdayclose)
            self.CandleMinuteKDrawYrectLow = min(self.CandleMinuteKItem.data.low.min(),self.yesterdayclose)
            self.CandleMinuteKDraw.setYRange(self.CandleMinuteKDrawYrectLow,self.CandleMinuteKDrawYrectHigh)
            self.ChangeRectidx = self.CandleMinuteKItem.lastidx
            self.CandleMinuteKDraw_Build_None = False
        else:
            if self.ChangeRectidx != self.CandleMinuteKItem.lastidx:
                self.ChangeRectidx = self.CandleMinuteKItem.lastidx
                dict_tmp=self.CandleMinuteKItem.data['ndatetime'][self.CandleMinuteKItem.data.ndatetime.dt.minute==0].dt.strftime('%H:%M:%S').to_dict()
                self.AxisMinute.setTicks([dict_tmp.items()])
                self.AxisMinuteDealMinus.setTicks([dict_tmp.items()])
                self.AxisMinuteBig.setTicks([dict_tmp.items()])
                self.AxisMinuteSmall.setTicks([dict_tmp.items()])
                del dict_tmp
                tmpline=self.CandleMinuteKItem.data.close.cumsum()
                self.avgline = tmpline.apply(lambda x: x/(tmpline[tmpline==x].index[0]+1))
                self.curve.setData(self.avgline)
                del tmpline
            if self.CandleMinuteKDrawYrectHigh < self.CandleMinuteKItem.high:
                self.CandleMinuteKDrawYrectHigh = self.CandleMinuteKItem.high
                self.CandleMinuteKDraw.setYRange(self.CandleMinuteKDrawYrectLow,self.CandleMinuteKDrawYrectHigh)
            if self.CandleMinuteKDrawYrectLow > self.CandleMinuteKItem.low:
                self.CandleMinuteKDrawYrectLow = self.CandleMinuteKItem.low
                self.CandleMinuteKDraw.setYRange(self.CandleMinuteKDrawYrectLow,self.CandleMinuteKDrawYrectHigh)
                    
    @Slot()
    def CandleMinuteDealMinusDrawFunc(self):
        if self.CandleMinuteDealMinusDraw_Build_None:
            self.CandleMinuteDealMinusDraw.addItem(self.CandleDealMinusItem)
            self.CandleMinuteDealMinusDrawYrectHigh = self.CandleDealMinusItem.data.dealminus.max()
            self.CandleMinuteDealMinusDrawYrectLow = self.CandleDealMinusItem.data.dealminus.min()
            self.CandleMinuteDealMinusDraw.setYRange(self.CandleMinuteDealMinusDrawYrectLow,self.CandleMinuteDealMinusDrawYrectHigh)
            self.DealMinusChangeRectidx = self.CandleDealMinusItem.lastidx
            self.CandleMinuteDealMinusDraw_Build_None = False
        else:
            if self.CandleMinuteDealMinusDrawYrectHigh < self.CandleDealMinusItem.high:
                self.CandleMinuteDealMinusDrawYrectHigh = self.CandleDealMinusItem.high
                self.CandleMinuteDealMinusDraw.setYRange(self.CandleMinuteDealMinusDrawYrectLow,self.CandleMinuteDealMinusDrawYrectHigh)
            if self.CandleMinuteDealMinusDrawYrectLow > self.CandleDealMinusItem.low:
                self.CandleMinuteDealMinusDrawYrectLow = self.CandleDealMinusItem.low
                self.CandleMinuteDealMinusDraw.setYRange(self.CandleMinuteDealMinusDrawYrectLow,self.CandleMinuteDealMinusDrawYrectHigh)
            
    @Slot()
    def CandleMinuteBigDrawFunc(self):
        if self.CandleMinuteBigDraw_Build_None:
            self.CandleMinuteBigDraw.addItem(self.CandleMinuteBigItem)
            self.CandleMinuteBigDrawYrectHigh = self.CandleMinuteBigItem.data.big.max()
            self.CandleMinuteBigDrawYrectLow = self.CandleMinuteBigItem.data.big.min()
            self.CandleMinuteBigDraw.setYRange(self.CandleMinuteBigDrawYrectLow,self.CandleMinuteBigDrawYrectHigh)
            self.BigChangeRectidx = self.CandleMinuteBigItem.lastidx
            self.CandleMinuteBigDraw_Build_None = False
        else:
            if self.CandleMinuteBigDrawYrectHigh < self.CandleMinuteBigItem.high:
                self.CandleMinuteBigDrawYrectHigh = self.CandleMinuteBigItem.high
                self.CandleMinuteBigDraw.setYRange(self.CandleMinuteBigDrawYrectLow,self.CandleMinuteBigDrawYrectHigh)
            if self.CandleMinuteBigDrawYrectLow > self.CandleMinuteBigItem.low:
                self.CandleMinuteBigDrawYrectLow = self.CandleMinuteBigItem.low
                self.CandleMinuteBigDraw.setYRange(self.CandleMinuteBigDrawYrectLow,self.CandleMinuteBigDrawYrectHigh)

    @Slot()
    def CandleMinuteSmallDrawFunc(self):
        if self.CandleMinuteSmallDraw_Build_None:
            self.CandleMinuteSmallDraw.addItem(self.CandleMinuteSmallItem)
            self.CandleMinuteSmallDrawYrectHigh = self.CandleMinuteSmallItem.data.small.max()
            self.CandleMinuteSmallDrawYrectLow = self.CandleMinuteSmallItem.data.small.min()
            self.CandleMinuteSmallDraw.setYRange(self.CandleMinuteSmallDrawYrectLow,self.CandleMinuteSmallDrawYrectHigh)
            self.SmallChangeRectidx = self.CandleMinuteSmallItem.lastidx
            self.CandleMinuteSmallDraw_Build_None = False
        else:
            self.CandleMinuteSmallItem.set_data(GlobalVar.NS.dfMinK[['ndatetime','small']],GlobalVar.NS.listMinSmall)
            if self.CandleMinuteSmallDrawYrectHigh < self.CandleMinuteSmallItem.high:
                self.CandleMinuteSmallDrawYrectHigh = self.CandleMinuteSmallItem.high
                self.CandleMinuteSmallDraw.setYRange(self.CandleMinuteSmallDrawYrectLow,self.CandleMinuteSmallDrawYrectHigh)
            if self.CandleMinuteSmallDrawYrectLow > self.CandleMinuteSmallItem.low:
                self.CandleMinuteSmallDrawYrectLow = self.CandleMinuteSmallItem.low
                self.CandleMinuteSmallDraw.setYRange(self.CandleMinuteSmallDrawYrectLow,self.CandleMinuteSmallDrawYrectHigh)
            
class SKReplyLibEvent:
    def OnConnect(self, bstrUserID, nErrorCode):
        nErrorStr = skC.SKCenterLib_GetReturnCodeMessage(nErrorCode)
        # print('連線成功: ', bstrUserID, nErrorStr)
        SKMain.SKMessage.ui.textBrowser.append('連線成功: '+bstrUserID+',連線資訊: '+nErrorStr)

    def OnDisconnect(self, bstrUserID, nErrorCode):
        nErrorStr = skC.SKCenterLib_GetReturnCodeMessage(nErrorCode)
        ntime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        # print('連線失敗: ', bstrUserID, nErrorStr, ntime)
        SKMain.SKMessage.ui.textBrowser.append('連線失敗: '+bstrUserID+', '+ nErrorStr+', '+ ntime)
    
    def OnReplyMessage(self,bstrUserID,bstrMessage):
        sComfirmCode=-1
        SKMain.SKMessage.ui.textBrowser.append(bstrUserID+','+bstrMessage)
        return sComfirmCode

    def OnComplete(self, bstrUserID):
        SKMain.ReplyCRpdMode.UpdateData(SKMain.replypd)
        SKMain.MainUi.Reply_TBW.setModel(SKMain.ReplyCRpdMode)
        SKMain.ReplyComplete = True

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
            SKMain.replypd.loc[i, '委託價格'] = round(float(Line[11]),2)
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
                        round(float(Line[11]),2), Line[20],
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

class SKOrderLibEvent:
    def OnAccount(self, bstrLogInID, bstrAccountData):
        Line = bstrAccountData.split(',')
        print(bstrAccountData)
        if Line[0] == 'TF':
            SKMain.IBAccount = str(Line[1]).strip() + str(Line[3]).strip()
            print('期貨帳戶: ' + SKMain.IBAccount, ',', Line[5])
            SKMain.MainUi.Future_Acc_CBox.addItem(SKMain.IBAccount)
            m_nCode = skO.GetFutureRights(bstrLogInID, SKMain.IBAccount, 1)
            SKMain.SKMessage.ui.textBrowser.append(skC.SKCenterLib_GetReturnCodeMessage(m_nCode))
            m_nCode = skO.ReadCertByID(bstrLogInID)
            SKMain.SKMessage.ui.textBrowser.append(skC.SKCenterLib_GetReturnCodeMessage(m_nCode))
            m_nCode = skR.SKReplyLib_ConnectByID(bstrLogInID)
            SKMain.SKMessage.ui.textBrowser.append(skC.SKCenterLib_GetReturnCodeMessage(m_nCode))
            m_nCode = skO.GetOpenInterestWithFormat(bstrLogInID, SKMain.IBAccount,3)
            SKMain.SKMessage.ui.textBrowser.append(skC.SKCenterLib_GetReturnCodeMessage(m_nCode))

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
                    SKMain.Bill.loc[i, 'Right'].setText(str(int(int(row.replace('+', '').strip())/100)))
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
            SKMain.MainUi.Open_TBW.setModel(SKMain.OpenCRpdMode)
            print('OnOpenInterest end pass')
            pass
        else:
            SKMain.openpd = SKMain.openpd.append(pd.DataFrame([Line],columns=['市場別', '期貨帳號', '商品', '買賣別', '未平倉部位', '當沖未平倉部位','平均成本', '一點價值', '單口手續費', '交易稅','登入帳號']))
        SKMain.onOpenInterestReplytimes+=1
        # i=0
        # print(Line)
        # for row in Line:
        #     print('次數: ', SKMain.test, '欄位:',i,'數值:',row)
        #     i+=1

class SKQuoteLibEvents:
    def __init__(self):
        self.count = 0
    def OnConnection(self, nKind, nCode):
        if (nKind == 3001):
            strMsg = 'Connected!, '+str(nCode)+str(nKind)
        elif (nKind == 3002):
            strMsg = 'DisConnected!, '+str(nCode)+str(nKind)
        elif (nKind == 3003):
            strMsg = 'Stocks ready!, '+str(nCode)+str(nKind)
            # time.sleep(5)
            m_nCode=skQ.SKQuoteLib_RequestStockList(SKMain.SKCommodity.ui.Market_comboBox.currentIndex())
            if m_nCode != 0:
                print('商品取得列表錯誤: %s',skC.SKCenterLib_GetReturnCodeMessage(m_nCode))
        elif (nKind == 3021):
            strMsg = 'Connect Error!, '+str(nCode)+str(nKind)
        else:
            strMsg = skC.SKCenterLib_GetReturnCodeMessage(nCode)
        SKMain.SKMessage.ui.textBrowser.append(strMsg)
    
    def OnNotifyStockList(self,sMarketNo,bstrStockData):
        SKMain.SKCommodity.Commodity_comboBox_signal.emit(sMarketNo,bstrStockData)

    def OnNotifyServerTime(self, sHour, sMinute, sSecond, nTotal):
        nTime = QTime(sHour, sMinute, sSecond)
        rTime = QTime(8,30,00)
        # if rTime == nTime:
        #     SKMain.ConnectFun()
        jTime = QTime(13, 46, 00)
        # # jTime=datetime.datetime.strptime('13:50:00','%H:%M:%S').time()
        if nTime == jTime:
            GlobalVar.SaveNotify.set(True)
            time.sleep(0.5)
            globals()['DataQueue'+str(GlobalVar.SaveNotify.commodityIndex)].put(None)
            globals()['Tick12KQueueTX00'].put(None)
            strMsg =nTime.toString(Qt.ISODate) +' 已變更存檔資訊: '+ str(GlobalVar.SaveNotify.value)
            SKMain.SKMessage.ui.textBrowser.append(strMsg)

        nTime = QTime(sHour, sMinute, sSecond).toString(Qt.ISODate)
        SKMain.MainUi.statusBar.showMessage('帳號:' + str(SKMain.SKID) + '\t伺服器時間:' + nTime)
    
    def OnNotifyHistoryTicks(self, sMarketNo, sStockIdx, nPtr, lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty, nSimulate):
        if nSimulate == 0 and globals()['DataQueue'+str(sStockIdx)].commodityIndex == sStockIdx:
            nhis = True
            nlist = [int(nPtr),str(lDate),str(lTimehms),str(lTimemillismicros),int(nBid),int(nAsk),int(nClose),int(nQty),nhis]
            globals()['DataQueue'+str(sStockIdx)].put(nlist)
    
    def OnNotifyTicks(self, sMarketNo, sStockIdx, nPtr, lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty, nSimulate):
        if nSimulate == 0 and globals()['DataQueue'+str(sStockIdx)].commodityIndex == sStockIdx:
            nhis = False
            nlist = [int(nPtr),str(lDate),str(lTimehms),str(lTimemillismicros),int(nBid),int(nAsk),int(nClose),int(nQty),nhis]
            globals()['DataQueue'+str(sStockIdx)].put(nlist)
    def OnNotifyBest5(self,sMarketNo,sStockidx,nBestBid1,nBestBidQty1,nBestBid2,nBestBidQty2,nBestBid3,nBestBidQty3,nBestBid4,nBestBidQty4,nBestBid5,nBestBidQty5,nExtendBid,nExtendBidQty,nBestAsk1,nBestAskQty1,nBestAsk2,nBestAskQty2,nBestAsk3,nBestAskQty3,nBestAsk4,nBestAskQty4,nBestAsk5,nBestAskQty5,nExtendAsk,nExtendAskQty,nSimulate):
        if GlobalVar.CandleTarget.commodityIndex == sStockidx:
            total_dict={'買量':{0:nBestBidQty1,1:nBestBidQty2,2:nBestBidQty3,3:nBestBidQty4,4:nBestBidQty5},
                        '買價':{0:int(nBestBid1/100),1:int(nBestBid2/100),2:int(nBestBid3/100),3:int(nBestBid4/100),4:int(nBestBid5/100)},
                        '賣價':{0:int(nBestAsk1/100),1:int(nBestAsk2/100),2:int(nBestAsk3/100),3:int(nBestAsk4/100),4:int(nBestAsk5/100)},
                        '賣量':{0:nBestAskQty1,1:nBestAskQty2,2:nBestAskQty3,3:nBestAskQty4,4:nBestAskQty5}}
            GlobalVar.DomDataQueue.put(total_dict)
    def OnNotifyFutureTradeInfo(self,bstrStockNo,sMarketNo,sStockidx,nBuyTotalCount,nSellTotalCount,nBuyTotalQty,nSellTotalQty,nBuyDealTotalCount,nSellDealTotalCount):
        if GlobalVar.CandleTarget.commodityIndex == sStockidx:
            GlobalVar.NS.listFT = [bstrStockNo,nBuyTotalCount,nSellTotalCount,nBuyTotalQty,nSellTotalQty,nBuyDealTotalCount,nSellDealTotalCount]
            if GlobalVar.MP_Event.is_set() is False:
                GlobalVar.MP_Event.set()

# comtypes使用此方式註冊callback
SKQuoteEvent = SKQuoteLibEvents()
SKQuoteLibEventHandler = comtypes.client.GetEvents(skQ, SKQuoteEvent)
SKOrderEvent = SKOrderLibEvent()
SKOrderLibEventHandler = comtypes.client.GetEvents(skO, SKOrderEvent)
SKReplyEvent = SKReplyLibEvent()
SKReplyLibEventHandler = comtypes.client.GetEvents(skR, SKReplyEvent)

if __name__=='__main__':
    GlobalVar.Initialize()
    SKApp = QApplication(sys.argv)
    SKMain = SKMainWindow()
    SKMain.show()
    # sys.exit(SKApp.exec_())
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        SKApp.instance().exec_()
