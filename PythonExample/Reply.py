# 先把API com元件初始化
import os

# 第一種讓群益API元件可導入讓Python code使用的方法
#import win32com.client 
#from ctypes import WinDLL,byref
#from ctypes.wintypes import MSG
#SKCenterLib = win32com.client.Dispatch("{AC30BAB5-194A-4515-A8D3-6260749F8577}")
#SKReplyLib = win32com.client.Dispatch("{72D98963-03E9-42AB-B997-BB2E5CCE78DD}")

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
            skC.SKCenterLib_SetLogPath(os.path.split(os.path.realpath(__file__))[0] + "\\CapitalLog_Reply")
            m_nCode = skC.SKCenterLib_Login(self.textID.get().replace(' ',''),self.textPassword.get().replace(' ',''))
            if(m_nCode==0):
                Global_ID["text"] =  self.textID.get().replace(' ','')
                WriteMessage("登入成功",self.listInformation)
            else:
                WriteMessage(m_nCode,self.listInformation)
        except Exception as e:
            messagebox.showerror("error！",e)
    def GetID(self):
        return self.textID.get().replace(' ','')

#下半部-回報
class FrameReply(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.grid()
        self.FrameReply = Frame(self)
        self.FrameReply.master["background"] = "#ffecec"
        self.createWidgets()

    def createWidgets(self):
        #ID
        # self.labelID = Label(self)
        # self.labelID["text"] = "ID："
        # self.labelID.grid(column = 0, row = 0)

        #Connect
        self.btnConnect = Button(self)
        self.btnConnect["text"] = "回報連線"
        self.btnConnect["background"] = "#ff9797"
        self.btnConnect["font"] = "20"
        self.btnConnect.grid(column = 0, row = 1)
        self.btnConnect["command"] = self.btnConnect_Click

        #Disconnect
        self.btnDisconnect = Button(self)
        self.btnDisconnect["text"] = "回報斷線"
        self.btnDisconnect["background"] = "#ff9797"
        self.btnDisconnect["font"] = "20"
        self.btnDisconnect.grid(column = 1, row = 1)

        #ConnectSignal
        # self.ConnectSignal = Label(self)
        # self.ConnectSignal["text"] = "【FALSE】"
        # self.ConnectSignal.grid(column = 2, row = 1)

        #訊息欄
        self.listInformation = Listbox(self, height = 25, width = 100)
        self.listInformation.grid(column = 0, row = 2, sticky = E + W, columnspan = 4)

        global ReplyInformation
        ReplyInformation = self.listInformation

    def btnConnect_Click(self):
        try:
            m_nCode = skR.SKReplyLib_ConnectByID(frLogin.GetID())
            SendReturnMessage("Reply", m_nCode, "SKQuoteLib_EnterMonitor",GlobalListInformation)
        except Exception as e:
            messagebox.showerror("error！",e)

class SKReplyLibEvent:
    def OnNewData(self,strUserID,StrData):
        WriteMessage(strUserID + " " +StrData ,ReplyInformation)

#SKReplyLibEventHandler = win32com.client.WithEvents(SKReplyLib, SKReplyLibEvent)
SKReplyEvent=SKReplyLibEvent()
SKReplyLibEventHandler = comtypes.client.GetEvents(skR, SKReplyEvent)

if __name__ == '__main__':
    root = Tk()
    frLogin = FrameLogin(master = root)
    #TabControl
    root.TabControl = Notebook(root)
    root.TabControl.add(FrameReply(master = root),text="Reply")
    root.TabControl.grid(column = 0, row = 2, sticky = E + W)
    root.mainloop()
