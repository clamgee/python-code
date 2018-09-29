# 先把API com元件初始化
import os

# 第一種讓群益API元件可導入讓Python code使用的方法
#import win32com.client 
#from ctypes import WinDLL,byref
#from ctypes.wintypes import MSG
#SKCenterLib = win32com.client.Dispatch("{AC30BAB5-194A-4515-A8D3-6260749F8577}")
#SKOrderLib = win32com.client.Dispatch("{54FE0E28-89B6-43A7-9F07-BE988BB40299}")
#SKOSQuote = win32com.client.Dispatch("{E3CB8A7C-896F-4828-85FC-8975E56BA2C4}")

# 第二種讓群益API元件可導入Python code內用的物件宣告
import comtypes.client
#comtypes.client.GetModule(os.path.split(os.path.realpath(__file__))[0] + r'\SKCOM.dll')
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

# 下單用的 STOCKORDER 物件(下單時要填股票代號,買賣別,委託價,數量等等的一個物件)
oStock=sk.STOCKORDER()

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

    def buttonLogin_Click(self):
        try:
            skC.SKCenterLib_SetLogPath(os.path.split(os.path.realpath(__file__))[0] + "\\CapitalLog_Order")
            m_nCode = skC.SKCenterLib_Login(self.textID.get().replace(' ',''),self.textPassword.get().replace(' ',''))
            if(m_nCode==0):
                Global_ID["text"] =  self.textID.get().replace(' ','')
                WriteMessage("登入成功",self.listInformation)
            else:
                WriteMessage(m_nCode,self.listInformation)
        except Exception as e:
            messagebox.showerror("error！",e)

#下半部-下單
class FrameOrder(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.grid()
        self.FrameOrder = Frame(self)
        self.FrameOrder.master["background"] = "#ffecec" 
        self.createWidgets()

    def createWidgets(self):
        self.label = Label(self)
        self.label["text"] = "證券委託"
        self.label["background"] = "#ffecec"
        self.label["font"] = 20
        self.label.grid(column = 0,row = 0)

        #初始化
        self.LabelInitialize = Label(self)
        self.LabelInitialize["text"] = "1.下單物件初始"
        self.LabelInitialize["background"] = "#ffecec"
        self.LabelInitialize["font"] = 20
        self.LabelInitialize.grid(column = 0, row = 1)
            #按鈕
        self.btnInitialize = Button(self)
        self.btnInitialize["text"] = "下單初始設定"
        self.btnInitialize["background"] = "#ff9797"
        self.btnInitialize["foreground"] = "#000000"
        self.btnInitialize["font"] = 20
        self.btnInitialize["command"] = self.btnInitialize_Click
        self.btnInitialize.grid(column = 1, row = 1)

       #讀取憑證
        self.LabelReadCert = Label(self)
        self.LabelReadCert["text"] = "2.讀取憑證"
        self.LabelReadCert["background"] = "#ffecec"
        self.LabelReadCert["font"] = 20
        self.LabelReadCert.grid(column = 2, row = 1)
            #按鈕
        self.btnReadCert = Button(self)
        self.btnReadCert["text"] = "讀取憑證"
        self.btnReadCert["background"] = "#ff9797"
        self.btnReadCert["foreground"] = "#000000"
        self.btnReadCert["font"] = 20
        self.btnReadCert["command"] = self.btnReadCert_Click
        self.btnReadCert.grid(column = 3, row = 1)

        #讀取憑證
        self.LabelGetAccount = Label(self)
        self.LabelGetAccount["text"] = "3.取得下單帳號"
        self.LabelGetAccount["background"] = "#ffecec"
        self.LabelGetAccount["font"] = 20
        self.LabelGetAccount.grid(column = 4, row = 1)
            #按鈕
        self.btnGetAccount = Button(self)
        self.btnGetAccount["text"] = "載入帳號"
        self.btnGetAccount["background"] = "#ff9797"
        self.btnGetAccount["foreground"] = "#000000"
        self.btnGetAccount["font"] = 20
        self.btnGetAccount["command"] = self.btnGetAccount_Click
        self.btnGetAccount.grid(column = 5, row =  1)

        #選帳號
        self.labelStockAccount = Label(self)
        self.labelStockAccount["text"] = "4.證券帳號"
        self.labelStockAccount["background"] = "#ffecec"
        self.labelStockAccount["font"] = 20
        self.labelStockAccount.grid(column = 6,row = 1)
            #輸入框
        self.boxStockAccount = Combobox(self,state='readonly')
        self.boxStockAccount.grid(column = 7, row = 1)

        #商品代碼
        self.LabelStockNo = Label(self)
        self.LabelStockNo["text"] = "商品代碼"
        self.LabelStockNo["background"] = "#ffecec"
        self.LabelStockNo["font"] = 20
        self.LabelStockNo.grid(column = 0, row = 3)
            #輸入框
        self.txtStockNo = Entry(self)
        self.txtStockNo.grid(column = 0, row = 4)

        #上市櫃-興櫃
        self.LabelPrime = Label(self)
        self.LabelPrime["text"] = "上市櫃-興櫃"
        self.LabelPrime["background"] = "#ffecec"
        self.LabelPrime["font"] = 20
        self.LabelPrime.grid(column = 1, row = 3)
            #輸入框
        self.boxPrime = Combobox(self,state='readonly')
        self.boxPrime['values'] = ("上市櫃","興櫃")
        self.boxPrime.grid(column = 1, row = 4)

        #買賣別
        self.LabelBidAsk = Label(self)
        self.LabelBidAsk["text"] = "買賣別"
        self.LabelBidAsk["background"] = "#ffecec"
        self.LabelBidAsk["font"] = 20
        self.LabelBidAsk.grid(column = 2, row = 3)
            #輸入框
        self.boxBidAsk = Combobox(self,state='readonly')
        self.boxBidAsk['values'] = ("買進","賣出")
        self.boxBidAsk.grid(column = 2, row = 4)

        #委託條件
        self.LabelPeriod = Label(self)
        self.LabelPeriod["text"] = "委託條件"
        self.LabelPeriod["background"] = "#ffecec"
        self.LabelPeriod["font"] = 20
        self.LabelPeriod.grid(column = 3, row = 3)
            #輸入框
        self.boxPeriod = Combobox(self,state='readonly')
        self.boxPeriod['values'] = ("盤中","盤後","零股")
        self.boxPeriod.grid(column = 3, row = 4)

        #當沖與否
        self.LabelFlag = Label(self)
        self.LabelFlag["text"] = "當沖與否"
        self.LabelFlag["background"] = "#ffecec"
        self.LabelFlag["font"] = 20
        self.LabelFlag.grid(column = 4, row = 3)
            #輸入框
        self.boxFlag = Combobox(self,state='readonly')
        self.boxFlag['values'] = ("現股","融資","融券","無券")
        self.boxFlag.grid(column = 4, row = 4)

        #委託價
        self.LabelPrice = Label(self)
        self.LabelPrice["text"] = "委託價"
        self.LabelPrice["background"] = "#ffecec"
        self.LabelPrice["font"] = 20
        self.LabelPrice.grid(column = 5, row = 3)
            #輸入框
        self.txtPrice = Entry(self)
        self.txtPrice.grid(column = 5, row = 4)

        #委託量
        self.LabelQty = Label(self)
        self.LabelQty["text"] = "委託量"
        self.LabelQty["background"] = "#ffecec"
        self.LabelQty["font"] = 20
        self.LabelQty.grid(column = 6, row = 3)
            #輸入框
        self.txtQty = Entry(self)
        self.txtQty.grid(column = 6, row = 4)

        #btnSendStockOrder
        self.btnSendStockOrder = Button(self)
        self.btnSendStockOrder["text"] = "送出委託"
        self.btnSendStockOrder["background"] = "#ff9797"
        self.btnSendStockOrder["foreground"] = "#000000"
        self.btnSendStockOrder["font"] = 20
        self.btnSendStockOrder["command"] = self.btnSendStockOrder_Click
        self.btnSendStockOrder.grid(column = 7, row =  2)
        #SendStockOrderAsync
        #self.btnSendStockOrderAsync = Button(self)
        #self.btnSendStockOrderAsync["text"] = "非同步送單"
        #self.btnSendStockOrderAsync["background"] = "#ff9797"
        #self.btnSendStockOrderAsync["foreground"] = "#000000"
        #self.btnSendStockOrderAsync["font"] = 20
        #self.btnSendStockOrderAsync["command"] = self.btnSendStockOrderAsync_Click
        #self.btnSendStockOrderAsync.grid(column = 7, row = 4)

        global GlobalboxStockAccount,GlobaltxtStockNo,GlobalboxPrime,GlobalboxPeriod,GlobalboxFlag,GlobalboxBidAsk,GlobaltxtPrice,GlobaltxtQty
        GlobalboxStockAccount = self.boxStockAccount
        GlobaltxtStockNo = self.txtStockNo
        GlobalboxPrime = self.boxPrime
        GlobalboxPeriod = self.boxPeriod
        GlobalboxFlag = self.boxFlag
        GlobalboxBidAsk = self.boxBidAsk
        GlobaltxtPrice = self.txtPrice
        GlobaltxtQty = self.txtQty



    #下單function
    global sPrime,sPeriod,sFlag,sBuySell
    #1.下單物件初始
    def btnInitialize_Click(self):
        try:
            m_nCode = skO.SKOrderLib_Initialize()
            SendReturnMessage("Order", m_nCode, "SKOrderLib_Initialize",GlobalListInformation)
        except Exception as e:
            messagebox.showerror("error！",e)    

    #2.讀取憑證    
    def btnReadCert_Click(self):
        try:
            m_nCode = skO.ReadCertByID(Global_ID["text"])
            SendReturnMessage("Order", m_nCode, "ReadCertByID",GlobalListInformation)
        except Exception as e:
            messagebox.showerror("error！",e)

    #3.取得下單帳號
    def btnGetAccount_Click(self):
        try:
            m_nCode = skO.GetUserAccount()
            SendReturnMessage("Order", m_nCode, "GetUserAccount",GlobalListInformation)
        except Exception as e:
            messagebox.showerror("error！",e)

    #4.下單送出
    def btnSendStockOrder_Click(self):
        self.SendStockOrder_Click(False)

    def btnSendStockOrderAsync_Click(self):
        self.SendStockOrder_Click(True)

    def SendStockOrder_Click(self, bAsyncOrder):
        try:
            if GlobalboxPrime.get()=="上市櫃":
                sPrime=0
            elif GlobalboxPrime.get()=="興櫃":
                sPrime=1
            
            if GlobalboxPeriod.get()=="盤中":
                sPeriod=0
            elif GlobalboxPeriod.get()=="盤後":
                sPeriod=1
            elif GlobalboxPeriod.get()=="零股":
                sPeriod=2
            
            if GlobalboxFlag.get()=="現股":
                sFlag=0
            elif GlobalboxFlag.get()=="融資":
                sFlag=1
            elif GlobalboxFlag.get()=="融券":
                sFlag=2
            elif GlobalboxFlag.get()=="無券":
                sFlag=3
            
            if GlobalboxBidAsk.get()=="買進":
                sBuySell=0
            elif GlobalboxBidAsk.get()=="賣出":
                sBuySell=1
            # 建立下單用的參數物件
            oStock=sk.STOCKORDER()
            # 填入完整帳號
            oStock.bstrFullAccount = GlobalboxStockAccount.get()
            # 填入股票代號
            oStock.bstrStockNo = GlobaltxtStockNo.get()
            # 上市、上櫃、興櫃
            oStock.sPrime = sPrime
            # 盤中、盤後、零股
            oStock.sPeriod = sPeriod
            # 現股、融資、融券
            oStock.sFlag = sFlag
            # 買賣別
            oStock.sBuySell = sBuySell
            # 委託價
            oStock.bstrPrice = GlobaltxtPrice.get()
            # 委託數量
            oStock.nQty = int(GlobaltxtQty.get())
            message,m_nCode = skO.SendStockOrder(Global_ID["text"], bAsyncOrder, oStock)
            SendReturnMessage("Order", m_nCode, "SendStockOrder",GlobalListInformation)
        except Exception as e:
            messagebox.showerror("error！",e)

class SKOrderLibEvent:
    def OnAccount(self,bstrLogInID,bstrAccountData):
        strValues = bstrAccountData.split(',')
        strAccount = strValues[1] + strValues[3]
        if strValues[0] == 'TS':
            GlobalboxStockAccount['values'] = (strAccount)

#SKOrderLibEventHandler = win32com.client.WithEvents(SKOrderLib, SKOrderLibEvent)
SKOrderEvent=SKOrderLibEvent()
SKOrderLibEventHandler = comtypes.client.GetEvents(skO, SKOrderEvent)

if __name__ == '__main__':
    root = Tk()
    FrameLogin(master = root)
    #TabControl
    root.TabControl = Notebook(root)
    root.TabControl.add(FrameOrder(master = root),text="Order")
    root.TabControl.grid(column = 0, row = 2, sticky = E + W)
    root.mainloop()
