# 先把API com元件初始化
import os

# 第一種讓群益API元件可導入讓Python code使用的方法
#import win32com.client 
#from ctypes import WinDLL,byref
#from ctypes.wintypes import MSG
#SKCenterLib = win32com.client.Dispatch("{AC30BAB5-194A-4515-A8D3-6260749F8577}")
#SKQuoteLib = win32com.client.Dispatch("{E7BCB8BB-E1F0-4F6F-A944-2679195E5807}")

# 第二種讓群益API元件可導入Python code內用的物件宣告
import comtypes.client
# comtypes.client.GetModule(os.path.split(os.path.realpath(__file__))[0] + r'\SKCOM.dll') #加此行需將API放與py同目錄
import comtypes.gen.SKCOMLib as sk
skC = comtypes.client.CreateObject(sk.SKCenterLib,interface=sk.ISKCenterLib)
skOOQ = comtypes.client.CreateObject(sk.SKOOQuoteLib,interface=sk.ISKOOQuoteLib)
skO = comtypes.client.CreateObject(sk.SKOrderLib,interface=sk.ISKOrderLib)
skOSQ = comtypes.client.CreateObject(sk.SKOSQuoteLib,interface=sk.ISKOSQuoteLib)
skQ = comtypes.client.CreateObject(sk.SKQuoteLib,interface=sk.ISKQuoteLib)
skR = comtypes.client.CreateObject(sk.SKReplyLib,interface=sk.ISKReplyLib)

# 畫視窗用物件
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox,colorchooser,font,Button,Frame,Label

# 數學計算用物件
import math
#使用模組
import datetime
import time
import numpy as np
import pandas as pd
import pyqtgraph as pg
from pyqtgraph import QtCore,QtGui
# 其它自建物件
import tickstokline
import KlineUi
#K線繪圖pyqtgraph 宣告
global app
app=pg.Qt.QtWidgets.QApplication([])

# 顯示各功能狀態用的function
def WriteMessage(strMsg,listInformation):
    listInformation.insert('end', strMsg)
    listInformation.see('end')
def SendReturnMessage(strType, nCode, strMessage,listInformation):
    GetMessage(strType, nCode, strMessage,listInformation)
def GetMessage(strType,nCode,strMessage,listInformation):
    strInfo = ""
    if (nCode != 0):
        strInfo ="【"+ skC.SKCenterLib_GetLastLogInfo()+ "】"
    WriteMessage("【" + strType + "】【" + strMessage + "】【" + skC.SKCenterLib_GetReturnCodeMessage(nCode) + "】" + strInfo,listInformation)
#----------------------------------------------------------------------------------------------------------------------------------------------------
#上半部登入框
class FrameLogin(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.grid()
        #self.pack()
        self.place()
        self.FrameLogin = Frame(self)
        self.master["background"] = "#ffecec"
        self.FrameLogin.master["background"] = "#ffecec" 
        self.createWidgets()
    def createWidgets(self):
        #帳號
        self.labelID = Label(self)
        self.labelID["text"] = "帳號："
        self.labelID["background"] = "#ffecec"
        self.labelID["font"] = 20
        self.labelID.grid(column=0,row=0)
            #輸入框
        self.textID = Entry(self)
        self.textID["width"] = 50
        self.textID.grid(column = 1, row = 0)

        #密碼
        self.labelPassword = Label(self)
        self.labelPassword["text"] = "密碼："
        self.labelPassword["background"] = "#ffecec"
        self.labelPassword["font"] = 20
        self.labelPassword.grid(column = 2, row = 0)
            #輸入框
        self.textPassword = Entry(self)
        self.textPassword["width"] = 50
        self.textPassword['show'] = '*'
        self.textPassword.grid(column = 3, row = 0)
        
        #按鈕
        self.buttonLogin = Button(self)
        self.buttonLogin["text"] = "登入"
        self.buttonLogin["background"] = "#ff9797"
        self.buttonLogin["foreground"] = "#000000"
        self.buttonLogin["highlightbackground"] = "#ff0000"
        self.buttonLogin["font"] = 20
        self.buttonLogin["command"] = self.buttonLogin_Click
        self.buttonLogin.grid(column = 4, row = 0)

        #ID
        self.labelID = Label(self)
        self.labelID["text"] = "<<ID>>"
        self.labelID["background"] = "#ffecec"
        self.labelID["font"] = 20
        self.labelID.grid(column = 5, row = 0)

        #訊息欄
        self.listInformation = Listbox(root, height=5)
        self.listInformation.grid(column = 0, row = 1, sticky = E + W)

        global GlobalListInformation,Global_ID
        GlobalListInformation = self.listInformation
        Global_ID = self.labelID
    # 這裡是登入按鈕,使用群益API不管要幹嘛你都要先登入才行
    def buttonLogin_Click(self):
        try:
            skC.SKCenterLib_SetLogPath(os.path.split(os.path.realpath(__file__))[0] + "\\CapitalLog_Quote")
            m_nCode = skC.SKCenterLib_Login(self.textID.get().replace(' ',''),self.textPassword.get().replace(' ',''))
            print(m_nCode)
            if(m_nCode==0):
                Global_ID["text"] =  self.textID.get().replace(' ','')
                WriteMessage("登入成功",self.listInformation)
            else:
                WriteMessage(m_nCode,self.listInformation)
        except Exception as e:
            messagebox.showerror("error！",e)

# 報價連線的按鈕
class FrameQuote(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.grid()
        self.FrameQuote = Frame(self)
        self.FrameQuote.master["background"] = "#ffecec"
        self.createWidgets()
        
    def createWidgets(self):
        #ID
        # self.labelID = Label(self)
        # self.labelID["text"] = "ID："
        # self.labelID.grid(column = 0, row = 0)

        #Connect
        self.btnConnect = Button(self)
        self.btnConnect["text"] = "報價連線"
        self.btnConnect["background"] = "#ff9797"
        self.btnConnect["font"] = 20
        self.btnConnect["command"] = self.btnConnect_Click
        self.btnConnect.grid(column = 0, row = 1)

        #Disconnect
        self.btnDisconnect = Button(self)
        self.btnDisconnect["text"] = "報價斷線"
        self.btnDisconnect["background"] = "#ff9797"
        self.btnDisconnect["font"] = 20
        self.btnDisconnect["command"] = self.btnDisconnect_Click
        self.btnDisconnect.grid(column = 1, row = 1)

        # #ConnectSignal
        # self.ConnectSignal = Label(self)
        # self.ConnectSignal["text"] = "【FALSE】"
        # self.ConnectSignal.grid(column = 2, row = 1)

        #TabControl
        self.TabControl = Notebook(self)
        self.TabControl.add(Quote(master = self),text="報價細節")
        self.TabControl.add(Tick(master = self),text="Tick")
        self.TabControl.add(KLine(master = self),text="KLine")
        self.TabControl.grid(column = 0, row = 2, sticky = E + W, columnspan = 4)

    def btnConnect_Click(self):
        try:
           m_nCode = skQ.SKQuoteLib_EnterMonitor()
           SendReturnMessage("Quote", m_nCode, "SKQuoteLib_EnterMonitor",GlobalListInformation)
        except Exception as e:
            messagebox.showerror("error！",e)
    
    def btnDisconnect_Click(self):
        try:
            m_nCode = skQ.SKQuoteLib_LeaveMonitor()
            if (m_nCode != 0):
                strMsg = "SKQuoteLib_LeaveMonitor failed!", skC.SKCenterLib_GetReturnCodeMessage(m_nCode)
                WriteMessage(strMsg,GlobalListInformation)
            else:
                SendReturnMessage("Quote", m_nCode, "SKQuoteLib_LeaveMonitor",GlobalListInformation)
        except Exception as e:
            messagebox.showerror("error！",e)

#下半部-報價-Quote項目
class Quote(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.grid()
        self.Quote = Frame(self)
        self.Quote.master["background"] = "#ffecec"
        self.createWidgets()
        
    def createWidgets(self):
        #PageNo
        self.LabelPageNo = Label(self)
        self.LabelPageNo["text"] = "PageNo"
        self.LabelPageNo["background"] = "#ffecec"
        self.LabelPageNo["font"] = 20
        self.LabelPageNo.grid(column=0,row=0)
        #輸入框
        self.strPageNo = StringVar()
        self.txtPageNo = Entry(self, textvariable = self.strPageNo)
        self.strPageNo.set("0")
        self.txtPageNo.grid(column=1,row=0)

        #商品代碼
        self.LabelStocks = Label(self)
        self.LabelStocks["text"] = "商品代碼"
        self.LabelStocks["background"] = "#ffecec"
        self.LabelStocks["font"] = 20
        self.LabelStocks.grid(column=2,row=0)
        #輸入框
        self.strStocks = StringVar()
        self.txtStocks = Entry(self, textvariable = self.strStocks)
        self.strStocks.set("TX00")
        self.txtStocks.grid(column=3,row=0)
        
        #提示
        self.LabelP = Label(self)
        self.LabelP["text"] = "( 多筆以逗號{,}區隔 )"
        self.LabelP["background"] = "#ffecec"
        self.LabelP["font"] = 20
        self.LabelP.grid(column=2,row=1, columnspan=2)

        #按鈕
        self.btnQueryStocks = Button(self)
        self.btnQueryStocks["text"] = "查詢"
        self.btnQueryStocks["background"] = "#ff9797"
        self.btnQueryStocks["foreground"] = "#000000"
        self.btnQueryStocks["font"] = 20
        self.btnQueryStocks["command"] = self.btnQueryStocks_Click
        self.btnQueryStocks.grid(column = 4, row = 0)

        #訊息欄
        self.listInformation = Listbox(self, height = 25, width = 100)
        self.listInformation.grid(column = 0, row = 2, sticky = E + W, columnspan = 6)

        global Gobal_Quote_ListInformation
        Gobal_Quote_ListInformation = self.listInformation

    def btnQueryStocks_Click(self):
        try:
            if(self.txtPageNo.get().replace(' ','') == ''):
                pn = 0
            else:
                pn = int(self.txtPageNo.get())
            skQ.SKQuoteLib_RequestStocks(pn,self.txtStocks.get().replace(' ',''))
        except Exception as e:
            messagebox.showerror("error！",e)

#下半部-報價-Tick項目
class Tick(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.grid()
        self.Quote = Frame(self)
        self.Quote.master["background"] = "#ffecec"
        self.createWidgets()
        
    def createWidgets(self):
        #PageNo
        self.LabelPageNo = Label(self)
        self.LabelPageNo["text"] = "PageNo"
        self.LabelPageNo["background"] = "#ffecec"
        self.LabelPageNo["font"] = 20
        self.LabelPageNo.grid(column=0,row=0)
        #輸入框
        self.strPageNo = StringVar()
        self.txtPageNo = Entry(self, textvariable = self.strPageNo)
        self.strPageNo.set("0")
        self.txtPageNo.grid(column=1,row=0)

        #商品代碼
        self.LabelStocks = Label(self)
        self.LabelStocks["text"] = "商品代碼"
        self.LabelStocks["background"] = "#ffecec"
        self.LabelStocks["font"] = 20
        self.LabelStocks.grid(column=2,row=0)
        #輸入框
        self.strStocks = StringVar()
        self.txtStocks = Entry(self, textvariable = self.strStocks)
        self.strStocks.set("TX00")
        self.txtStocks.grid(column=3,row=0)
        
        #按鈕
        self.btnQueryStocks = Button(self)
        self.btnQueryStocks["text"] = "查詢完整"
        self.btnQueryStocks["background"] = "#ff9797"
        self.btnQueryStocks["foreground"] = "#000000"
        self.btnQueryStocks["font"] = 20
        self.btnQueryStocks["command"] = self.btnTick_Click
        self.btnQueryStocks.grid(column = 4, row = 0)
        #按鈕
        self.btnQueryStocks = Button(self)
        self.btnQueryStocks["text"] = "查詢即時"
        self.btnQueryStocks["background"] = "#ff9797"
        self.btnQueryStocks["foreground"] = "#000000"
        self.btnQueryStocks["font"] = 20
        self.btnQueryStocks["command"] = self.btnLiveTick_Click
        self.btnQueryStocks.grid(column = 5, row = 0)

        #訊息欄
        self.listInformation = Listbox(self, height = 25, width = 100)
        self.listInformation.grid(column = 0, row = 2, sticky = E + W, columnspan = 6)

        global Gobal_Tick_ListInformation
        Gobal_Tick_ListInformation = self.listInformation
        
    def btnTick_Click(self):
        try:
            pn = 0
            if(self.txtPageNo.get().replace(' ','') != ''):
                pn = int(self.txtPageNo.get())
            global Future
            global item
            global Kui
            Future = tickstokline.dataprocess(self.txtStocks.get().strip())
            skQ.SKQuoteLib_RequestTicks(pn,self.txtStocks.get().replace(' ',''))
            # app=pg.Qt.QtWidgets.QApplication([])
            item=KlineUi.CandlestickItem()            
            Kui=KlineUi.KlineWidget(self.txtStocks.get().strip())
            Kui.plt.show()
            Kui.plt.addItem(item)
            item.set_data(Future.contractkpd)
            # app.processEvents()
            xmax=int(len(item.pictures))
            xmin=int(max(0,xmax-item.countK))
            ymin=item.data.loc[xmin:xmax,['low']].values.min()
            ymax=item.data.loc[xmin:xmax,['high']].values.max()
            # app.processEvents()   
            Kui.update(xmin,xmax,ymin,ymax)
            
            if __name__ == '__main__':
                import sys
                if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
                    app.exit(app.instance().exec_())
        except Exception as e:
            messagebox.showerror("error！",e)

    def btnLiveTick_Click(self):
        try:
            if(self.txtPageNo.get().replace(' ','') != ''):
                pn = int(self.txtPageNo.get())
            skQ.SKQuoteLib_RequestLiveTick(pn,self.txtStocks.get().replace(' ',''))
        except Exception as e:
            messagebox.showerror("error！",e)

#下半部-報價-KLine項目
class KLine(Frame):
    
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.grid()
        self.KLine = Frame(self)
        self.KLine.master["background"] = "#ffecec"
        self.createWidgets()
        
    def createWidgets(self):
        #商品代碼
        self.LabelKLine = Label(self)
        self.LabelKLine["text"] = "商品代碼"
        self.LabelKLine["background"] = "#ffecec"
        self.LabelKLine["font"] = 20
        self.LabelKLine.grid(column=0,row=0)
        #輸入框
        self.txtKLine = Entry(self)
        self.txtKLine.grid(column=1,row=0)

        #提示
        # self.LabelP = Label(self)
        # self.LabelP["text"] = "( 多筆以逗號{,}區隔 )"
        # self.LabelP.grid(column=0,row=1, columnspan=2)

        #K線種類
        self.boxKLine = Combobox(self,state='readonly')
        self.boxKLine['values'] = tickstokline.KLINETYPESET
        self.boxKLine.grid(column=2,row=0)

        #K線輸出格式
        self.boxOutType = Combobox(self,state='readonly')
        self.boxOutType['values'] = tickstokline.KLINEOUTTYPESET
        self.boxOutType.grid(column=3,row=0)

        #K線盤別
        self.boxTradeSessin = Combobox(self,state='readonly')
        self.boxTradeSessin['values'] = tickstokline.TRADESESSIONSET
        self.boxTradeSessin.grid(column=4,row=0)

        #按鈕
        self.btnKLine = Button(self)
        self.btnKLine["text"] = "查詢"
        self.btnKLine["background"] = "#ff9797"
        self.btnKLine["foreground"] = "#000000"
        self.btnKLine["font"] = 20
        self.btnKLine["command"] = self.btnKLine_Click
        self.btnKLine.grid(column = 5, row = 0)


        #訊息欄
        self.listInformation = Listbox(self, height = 25, width = 100)
        self.listInformation.grid(column = 0, row = 2, sticky = E + W, columnspan = 6)

        #雖然上面有設定global了,但是這邊還是要再宣告一次,不然不會過
        global Gobal_KLine_ListInformation
        Gobal_KLine_ListInformation = self.listInformation
    
    def btnKLine_Click(self):
        try:
            if(self.boxKLine.get() == "0 = 1分鐘線"):
                sKLineType=0
            elif(self.boxKLine.get() == "4 = 完整日線"):
                sKLineType=4
            elif(self.boxKLine.get() == "5 = 週線"):
                sKLineType=5
            else:
                sKLineType=6

            if(self.boxOutType.get() == "0 = 舊版輸出格式"):
                sOutType=0
            else:
                sOutType=1

            if(self.boxTradeSessin.get() == "0 = 全盤K線(國內期選用)"):
                sTradeSession=0
            else:
                sTradeSession=1
            m_nCode = skQ.SKQuoteLib_RequestKLineAM(self.txtKLine.get().replace(' ','') , sKLineType , sOutType, sTradeSession)
            SendReturnMessage("Quote", m_nCode, "SKQuoteLib_RequestKLineAM",GlobalListInformation)
        except Exception as e:
            messagebox.showerror("error！",e)

#事件        
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
        WriteMessage(strMsg,GlobalListInformation)

    def OnNotifyServerTime(self,sHour,sMinute,sSecond,nTotal):
        HH=str(sHour) 
        while len(HH)<2 : 
            HH='0'+HH
        MM=str(sMinute)
        while len(MM)<2 :
            MM='0'+MM
        SS=str(sSecond)
        while len(SS)<2 :
            SS='0'+SS
        nTime=HH+MM+SS
        nTime=datetime.datetime.strptime(nTime,'%H%M%S').time()
        jTime=datetime.datetime.strptime('13:50:00','%H:%M:%S').time()
        if nTime==jTime and Future.ticksdf is not None :
            filename='data/Ticks'+str(Future.ticksdf.iloc[-1,0])+'.txt'
            Future.ticksdf.to_csv(filename,header=False,index=False)
        WriteMessage(nTime,GlobalListInformation)       
    

    def OnNotifyQuote(self, sMarketNo, sStockidx):
        pStock = sk.SKSTOCK()
        skQ.SKQuoteLib_GetStockByIndex(sMarketNo, sStockidx, pStock)
        strMsg = '代碼:',pStock.bstrStockNo,'--名稱:',pStock.bstrStockName,'--開盤價:',pStock.nOpen/math.pow(10,pStock.sDecimal),'--最高:',pStock.nHigh/math.pow(10,pStock.sDecimal),'--最低:',pStock.nLow/math.pow(10,pStock.sDecimal),'--成交價:',pStock.nClose/math.pow(10,pStock.sDecimal),'--總量:',pStock.nTQty
        WriteMessage(strMsg,Gobal_Quote_ListInformation)
        
    def OnNotifyHistoryTicks(self, sMarketNo, sStockIdx, nPtr, lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty, nSimulate):
        if nSimulate==0:
            Future.Ticks(lDate,lTimehms,lTimemillismicros,nBid,nAsk,nClose,nQty)
            strMsg=Future.contractkpd.iloc[-1:].values
            WriteMessage(strMsg,Gobal_Tick_ListInformation)
        # strMsg = "[OnNotifyHistoryTicks]", sStockIdx, nPtr, lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty, nSimulate
        # WriteMessage(strMsg,Gobal_Tick_ListInformation)

    def OnNotifyTicks(self,sMarketNo, sStockIdx, nPtr, lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty, nSimulate):
            if nSimulate==0:
                Future.Ticks(lDate,lTimehms,lTimemillismicros,nBid,nAsk,nClose,nQty)
                strMsg=Future.contractkpd.iloc[-1:].values
                # strMsg=lDate+','+lTimehms+','+lTimemillismicros+','+nBid+','+nAsk+','+nClose+','+nQty
                WriteMessage(strMsg,Gobal_Tick_ListInformation)            
                item.set_data(Future.contractkpd)
                # app.processEvents()
                xmax=int(len(item.pictures))
                xmin=int(max(0,xmax-item.countK))
                ymin=item.data.loc[xmin:xmax,['low']].values.min()
                ymax=item.data.loc[xmin:xmax,['high']].values.max()
                # app.processEvents()   
                Kui.update(xmin,xmax,ymin,ymax)
                # app.processEvents()

        # strMsg = "[OnNotifyTicks]", sStockIdx, nPtr, lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty, nSimulate
        # WriteMessage(strMsg,Gobal_Tick_ListInformation)

    def OnNotifyBest5(self,sMarketNo,sStockidx,nBestBid1,nBestBidQty1,nBestBid2,nBestBidQty2,nBestBid3,nBestBidQty3,nBestBid4,nBestBidQty4,nBestBid5,nBestBidQty5,nExtendBid,nExtendBidQty,nBestAsk1,nBestAskQty1,nBestAsk2,nBestAskQty2,nBestAsk3,nBestAskQty3,nBestAsk4,nBestAskQty4,nBestAsk5,nBestAskQty5,nExtendAsk,nExtendAskQty,nSimulate):
        bid_dict={int(nBestBid1/100):nBestBidQty1,int(nBestBid2/100):nBestBidQty2,int(nBestBid3/100):nBestBidQty3,int(nBestBid4/100):nBestBidQty4,int(nBestBid5/100):nBestBidQty5}
        ask_dict={int(nBestAsk1/100):nBestAskQty1,int(nBestAsk2/100):nBestAskQty2,int(nBestAsk3/100):nBestAskQty3,int(nBestAsk4/100):nBestAskQty4,int(nBestAsk5/100):nBestAskQty5}
        print(ask_dict)
    
    
    def OnNotifyKLineData(self,bstrStockNo,bstrData):
        cutData = bstrData.split(',')
        strMsg = bstrStockNo,bstrData
        WriteMessage(strMsg,Gobal_KLine_ListInformation)

#SKQuoteLibEventHandler = win32com.client.WithEvents(SKQuoteLib, SKQuoteLibEvents)
SKQuoteEvent=SKQuoteLibEvents()
SKQuoteLibEventHandler = comtypes.client.GetEvents(skQ, SKQuoteEvent)

if __name__ == '__main__':
    # import sys
    # if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    #     app.exit(app.instance().exec_())

    root = Tk()
    root.title("PythonExampleQuote")
    root["background"] = "#ffdbdb"
    # Center
    FrameLogin(master = root)
    #TabControl
    root.TabControl = Notebook(root)
    root.TabControl.add(FrameQuote(master = root),text="報價功能")
    root.TabControl.grid(column = 0, row = 2, sticky = 'ew', padx = 10, pady = 10)

    root.mainloop()
