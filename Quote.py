# 先把API com元件初始化
import os
#目前已知RequestLiveTick 函數需要指定C語言的變數型態
import ctypes
import datetime
import time
import threading
#繪圖元件
import pyqtgraph as pg
from pyqtgraph import QtCore, QtGui
# 第二種讓群益API元件可導入Python，code內用的物件宣告，SKCOM需要註冊Registry
import comtypes.client
import comtypes.gen.SKCOMLib as sk
skC = comtypes.client.CreateObject(sk.SKCenterLib,interface=sk.ISKCenterLib)
skO = comtypes.client.CreateObject(sk.SKOrderLib,interface=sk.ISKOrderLib)
skQ = comtypes.client.CreateObject(sk.SKQuoteLib,interface=sk.ISKQuoteLib)
skR = comtypes.client.CreateObject(sk.SKReplyLib,interface=sk.ISKReplyLib)

# 畫視窗用物件
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox,colorchooser,font,Button,Frame,Label

# 數學計算用物件
import math
import tickstokline #自訂資料處理函數
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
            skC.SKCenterLib_SetLogPath("C:\CapitalLog_Quote")
            m_nCode = skC.SKCenterLib_Login(self.textID.get().replace(' ',''),self.textPassword.get().replace(' ',''))
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
        self.txtPageNo = Entry(self)
        self.txtPageNo.grid(column=1,row=0)

        #商品代碼
        self.LabelStocks = Label(self)
        self.LabelStocks["text"] = "商品代碼"
        self.LabelStocks["background"] = "#ffecec"
        self.LabelStocks["font"] = 20
        self.LabelStocks.grid(column=2,row=0)
        #輸入框
        self.txtStocks = Entry(self)
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

        self.btnOutputTicks = Button(self)
        self.btnOutputTicks["text"] = "匯出Ticks"
        self.btnOutputTicks["background"] = "#ff9797"
        self.btnOutputTicks["foreground"] = "#000000"
        self.btnOutputTicks["font"] = 20
        self.btnOutputTicks["command"] = self.btnOutputTicks_Click
        self.btnOutputTicks.grid(column = 5, row = 0)


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
                pn=int(self.txtPageNo.get())

            global Future
            global item
            Future = tickstokline.dataprocess(0,self.txtStocks.get().replace(' ',''))
            # x_nCode = skQ.SKQuoteLib_RequestLiveTick(pn,self.txtStocks.get().replace(' ',''))
            x_nCode = skQ.SKQuoteLib_RequestTicks(pn,self.txtStocks.get().replace(' ',''))
            item = tickstokline.CandlestickItem()
            # item.set_data(Future.contractkpd)
            plt = pg.plot()
            plt.hideAxis('left')
            plt.showAxis('right')
            plt.showGrid(False,True)
            plt.addItem(item)
            plt.setWindowTitle('pyqtgraph example: customGraphicsItem')
            print(x_nCode,type(pn),pn,type(self.txtStocks.get().replace(' ','')),self.txtStocks.get().replace(' ',''))
            SendReturnMessage("Quote", x_nCode, "SKQuoteLib_RequestLiveTick",GlobalListInformation)
            print(sys.excepthook)
            #skQ.SKQuoteLib_RequestStocks(pn,self.txtStocks.get().replace(' ',''))
            if __name__ == '__main__':
                import sys
                if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
                    QtGui.QApplication.instance().exec_()

        except Exception as e:
            messagebox.showerror("Ticks SKQuote error！",e)
    
    def btnOutputTicks_Click(self):
        try:
            if Future.ticksdf is not None:
                filename='data/Ticks'+str(Future.ticksdf.iloc[-1,0])+'.txt'
                Future.ticksdf.to_csv(filename,header=False,index=False)
        except Exception as e:
             messagebox.showerror("Ticks Output error！",e)

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
        self.boxKLine['values'] = ("0 = 1分鐘線", "4 =完整日線", "5 =週線", "6 =月線")
        self.boxKLine.grid(column=2,row=0)

        #K線輸出格式
        self.boxOutType = Combobox(self,state='readonly')
        self.boxOutType['values'] = ("0=舊版輸出格式", "1=新版輸出格式")
        self.boxOutType.grid(column=3,row=0)

        #按鈕
        self.btnKLine = Button(self)
        self.btnKLine["text"] = "查詢"
        self.btnKLine["background"] = "#ff9797"
        self.btnKLine["foreground"] = "#000000"
        self.btnKLine["font"] = 20
        self.btnKLine["command"] = self.btnKLine_Click
        self.btnKLine.grid(column = 4, row = 0)

        # #按鈕
        # self.btnCalcute = Button(self)
        # self.btnCalcute["text"] = "計算"
        # self.btnCalcute["background"] = "#66b3ff"
        # self.btnCalcute["foreground"] = "white"
        # self.btnCalcute["font"] = 20
        # self.btnCalcute["command"] = self.btnCalcute_Click
        # self.btnCalcute.grid(column = 5, row = 0)

        #訊息欄
        self.listInformation = Listbox(self, height = 25, width = 100)
        self.listInformation.grid(column = 0, row = 2, sticky = E + W, columnspan = 6)

        #雖然上面有設定global了,但是這邊還是要再宣告一次,不然不會過
        global Gobal_KLine_ListInformation
        Gobal_KLine_ListInformation = self.listInformation
    
    def btnKLine_Click(self):
        try:
            # skQ.SKQuoteLib_RequestKLine(self.txtKLine.get(),self.boxKLine.get(),self.boxOutType.get())
            if(self.boxKLine.get() == "0 = 1分鐘線"):
                ktp=0
            elif(self.boxKLine.get() == "4 =完整日線"):
                ktp=4
            elif(self.boxKLine.get() == "5 =週線"):
                ktp=5
            else:
                ktp=6

            if(self.boxOutType.get() == "0=舊版輸出格式"):
                otp=0
            else:
                otp=1
            m_nCode = skQ.SKQuoteLib_RequestKLine(self.txtKLine.get().replace(' ','') , ktp , otp)
            SendReturnMessage("Quote", m_nCode, "SKQuoteLib_RequestKLine",GlobalListInformation)
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
    
    def OnNotifyTicks(self,sMarketNo,sIndex,nPtr,nDate,nTimehms,nTimemillismicros,nBid,nAsk,nClose,nQty,nSimulate):
        if nSimulate==0:
            Future.Ticks(nDate,nTimehms,nTimemillismicros,nBid,nAsk,nClose,nQty)
            strMsg=Future.contractkpd.iloc[-1:].values
            WriteMessage(strMsg,Gobal_Quote_ListInformation)            
            # add_thread=threading.Thread(target=Future.drawbar(
            # # Future.drawbar(
            #     Future.contractkpd['ndatetime'],
            #     Future.contractkpd['open'],
            #     Future.contractkpd['high'],
            #     Future.contractkpd['low'],
            #     Future.contractkpd['close']
            # ))
            # add_thread.start()
            item.set_data(Future.contractkpd)

    def OnNotifyHistoryTicks(self,sMarketNo,sIndex,nPtr,nDate,nTimehms,nTimemillismicros,nBid,nAsk,nClose,nQty,nSimulate):
        if nSimulate==0:
            # start=time.time()
            Future.Ticks(nDate,nTimehms,nTimemillismicros,nBid,nAsk,nClose,nQty)
            strMsg=Future.contractkpd.iloc[-1:].values
            WriteMessage(strMsg,Gobal_Quote_ListInformation)
            # end=time.time()
            # ep=round((end-start),6)
            # print('歷史Tick時間: ',ep)
            # add_thread=threading.Thread(target=Future.drawbar(
            #     Future.contractkpd['ndatetime'],
            #     Future.contractkpd['open'],
            #     Future.contractkpd['high'],
            #     Future.contractkpd['low'],
            #     Future.contractkpd['close']
            # ))
            # add_thread.start()
        
    
    def OnNotifyKLineData(self,bstrStockNo,bstrData):
        cutData = bstrData.split(',')
        strMsg = bstrStockNo,bstrData
        WriteMessage(strMsg,Gobal_KLine_ListInformation)

#SKQuoteLibEventHandler = win32com.client.WithEvents(SKQuoteLib, SKQuoteLibEvents)
SKQuoteEvent=SKQuoteLibEvents()
SKQuoteLibEventHandler = comtypes.client.GetEvents(skQ, SKQuoteEvent)


if __name__ == '__main__':
    root = Tk()
    FrameLogin(master = root)
    #TabControl
    root.TabControl = Notebook(root)
    root.TabControl.add(FrameQuote(master = root),text="報價功能")
    root.TabControl.grid(column = 0, row = 2, sticky = E + W)

    root.mainloop()
