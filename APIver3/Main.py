import sys,os,time
from PySide6.QtCore import QObject, Signal,Slot,QTime,Qt,QThread,QAbstractTableModel,QFile
from PySide6.QtWidgets import QMainWindow,QApplication,QTableWidgetItem,QMessageBox,QHeaderView
from PySide6.QtGui import QAction
from PySide6 import QtCore
import pyqtgraph as pg
import pandas as pd
import numpy as np
# 外部 自寫模組
from UI.MainWindow import Ui_CapitalAPI
import FuncUI,FuncClass,Config_dict
# 使用SKCOM元件
import comtypes.client
import comtypes.gen.SKCOMLib as sk

skC = comtypes.client.CreateObject(sk.SKCenterLib, interface=sk.ISKCenterLib)
skO = comtypes.client.CreateObject(sk.SKOrderLib, interface=sk.ISKOrderLib)
skQ = comtypes.client.CreateObject(sk.SKQuoteLib, interface=sk.ISKQuoteLib)
skR = comtypes.client.CreateObject(sk.SKReplyLib, interface=sk.ISKReplyLib)
# 主視窗物件
class SKMainWindow(QMainWindow):
    def __init__(self,parent=None):
        super(SKMainWindow, self).__init__(parent)
        self.MainUi = Ui_CapitalAPI()
        self.MainUi.setupUi(self)
        self.showMaximized() #主視窗最大化
        # 介面導入
        self.SKMessageUI()  # 系統訊息介面
        self.SKCommodityUI() #商品+5檔+大小單+下單介面
        self.SKLoginUI()  # 登入介面
        self.RightUI() #權益數介面
        # ManuBar連結
        self.MainUi.actionLogin.triggered.connect(self.Login.ui.show)  # 登入介面連結
        self.MainUi.SysDetail.triggered.connect(self.SKMessage.ui.show) #系統資訊介面連結
        self.MainUi.Connectbtn.triggered.connect(self.ConnectFun) #SKCom 報價連線
        self.MainUi.Disconnectbtn.triggered.connect(self.disconnectFun) #SKCom 報價斷線
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
    
    def SKCommodityUI(self):
        self.SKCommodity = FuncUI.CommodityForm()
        self.SKCommodity.ui.show()
        self.SKCommodity.ui.commoditybtn.clicked.connect(self.commodityFunc)
        self.SKCommodity.ui.TDetailbtn.clicked.connect(self.SKTraDetailUI)
    
    def SKTraDetailUI(self):
        self.SKTraDetail = FuncUI.MessageDialog('交易明細') #交易明細
        self.SKTraDetail.ui.show()
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
    # 權益數介面
    def RightUI(self):
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
    # 委託未平倉回報資料表設定格式
    def Reply_Open_Fnc(self):
        self.replypd = pd.DataFrame(
        columns=['商品名稱', '買賣', '委託價格', '委託口數', '委託狀態', '成交口數', '取消口數', '倉位', '條件', '價位格式', '委託序號', '委託書號', '委託日期',
                    '委託時間', '交易時段'])
        self.ReplyCRpdMode = FuncClass.PandasModel()
        self.openpd = pd.DataFrame(
            columns=['市場別', '期貨帳號', '商品', '買賣別', '未平倉部位', '當沖未平倉部位', '平均成本', '一點價值', '單口手續費', '交易稅','登入帳號'])
        self.OpenCRpdMode = FuncClass.PandasModel()
        self.test = 0
    # 報價系統連線功能
    def ConnectFun(self):
        m_nCode = skQ.SKQuoteLib_EnterMonitor()
        if m_nCode==0:
            strMsg = '報價已連線!!!'
        else:
            strMsg = skC.SKCenterLib_GetReturnCodeMessage(m_nCode)
        self.SKMessage.ui.textBrowser.append('EnterMonitor: '+strMsg)

    def disconnectFun(self):
        m_nCode = skQ.SKQuoteLib_LeaveMonitor()
        if m_nCode == 0:
            strMsg='報價已斷線!!!'
        else:
            strMsg = skC.SKCenterLib_GetReturnCodeMessage(m_nCode)
        self.SKMessage.ui.textBrowser.append('LeaveMonitor: '+strMsg)
    # 報價系統結束
    def commodityFunc(self):
        self.SKMessage.ui.textBrowser.append('報價按鈕')


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
        # print(bstrUserID+','+bstrMessage)
        return sComfirmCode

    def OnComplete(self, bstrUserID):
        SKMain.ReplyCRpdMode.UpdateData(SKMain.replypd)
        SKMain.MainUi.Reply_TBW.setModel(SKMain.ReplyCRpdMode)
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
        SKMain.test+=1
        # i=0
        # print(Line)
        # for row in Line:
        #     print('次數: ', SKMain.test, '欄位:',i,'數值:',row)
        #     i+=1

class SKQuoteLibEvents:
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
        Line = bstrStockData.split(';')
        ListCommodity=[]
        for row in Line:
            rowstuff = row.split(',')
            if rowstuff[0].replace(' ','')!='##' and rowstuff[0]!='':
                ListCommodity.append(rowstuff[0])#+','+rowstuff[1]])
                # SKMain.SKMessage.ui.textBrowser.append(rowstuff[0]+','+rowstuff[1])
            else:
                pass
        SKMain.SKCommodity.ui.Commodity_comboBox.addItems(ListCommodity)

    def OnNotifyServerTime(self, sHour, sMinute, sSecond, nTotal):
        nTime = QTime(sHour, sMinute, sSecond)
        rTime = QTime(8,30,00)
        # if rTime == nTime:
        #     SKMain.ConnectFun()
        # jTime = QTime(13, 50, 00)
        # # jTime=datetime.datetime.strptime('13:50:00','%H:%M:%S').time()
        # if nTime == jTime and SKMain.Future.ticklst is not None:
        #     ticksdf = pd.DataFrame(columns=['ndatetime','nbid','nask','close','volume','deal'])
        #     ticksdf =ticksdf.append(pd.DataFrame(SKMain.Future.ticklst,columns=['ndatetime','nbid','nask','close','volume','deal']),ignore_index=True,sort=False)
        #     ticksdf['ndatetime']=pd.to_datetime(ticksdf['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
        #     filename = 'Ticks' + ticksdf.iloc[-1, 0].date().strftime('%Y-%m-%d') + '.txt'
        #     ticksdf.to_csv('../data/'+filename, header=False, index=False)
        #     df1=pd.read_csv('filename.txt')
        #     df1=df1.append(pd.DataFrame([[filename]],columns=['filename']),ignore_index=True)
        #     df1.to_csv('filename.txt',index=False)
        #     del df1
        #     del ticksdf
        #     result=SKMain.Future.contractkpd.drop(columns=['high_avg','low_avg','dealbid','dealask','dealminus'])            
        #     result.sort_values(by=['ndatetime'],ascending=True)
        #     result.to_csv('../result.dat',header=True, index=False,mode='w')
        nTime = QTime(sHour, sMinute, sSecond).toString(Qt.ISODate)
        SKMain.MainUi.statusBar.showMessage('帳號:' + str(SKMain.SKID) + '\t伺服器時間:' + nTime)

# comtypes使用此方式註冊callback
SKQuoteEvent = SKQuoteLibEvents()
SKQuoteLibEventHandler = comtypes.client.GetEvents(skQ, SKQuoteEvent)
SKOrderEvent = SKOrderLibEvent()
SKOrderLibEventHandler = comtypes.client.GetEvents(skO, SKOrderEvent)
SKReplyEvent = SKReplyLibEvent()
SKReplyLibEventHandler = comtypes.client.GetEvents(skR, SKReplyEvent)

if __name__=='__main__':
    SKApp = QApplication(sys.argv)
    SKMain = SKMainWindow()
    SKMain.show()

    sys.exit(SKApp.exec_())
