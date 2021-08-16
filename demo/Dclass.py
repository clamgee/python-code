import pythoncom, time
import comtypes.client as cc

# cc.GetModule('C:\\SKCOM\\x86\\SKCOM.dll')
import comtypes.gen.SKCOMLib as sk

ts=sk.SKSTOCK()

skC=cc.CreateObject(sk.SKCenterLib,interface=sk.ISKCenterLib)
skQ=cc.CreateObject(sk.SKQuoteLib,interface=sk.ISKQuoteLib)

#Some Configure
ID='U120196256'
PW='7652uy'

#想取得報價的股票代碼
strStocks='TX00'

#define functions
def getStock(nMarket, nIndex, ts):
    skQ.SKQuoteLib_GetStockByIndex(nMarket, nIndex, ts)
    print(ts.bstrStockName, ts.bstrStockNo,  ts.nClose/10**ts.sDecimal)

#建立事件類別
class skQ_events:
    def OnConnection(self, nKind, nCode):
        if nCode == 0 :
            if nKind == 3001 :
                print("skQ OnConnection, nkind= ", nKind)
            elif (nKind == 3003):
                #等到回報3003 確定連線報價伺服器成功後，才登陸要報價的股票
                skQ.SKQuoteLib_RequestStocks(1, strStocks)
                print("skQ OnConnection, request stocks, nkind= ", nKind)
    def OnNotifyQuote(self, sMarketNo, sStockIdx):
        getStock(sMarketNo, sStockIdx, ts)

#Event sink
EventQ=skQ_events()
#make connection to event sink
ConnectionQ = cc.GetEvents(skQ, EventQ)        

#Login
print("Login,", skC.SKCenterLib_GetReturnCodeMessage(skC.SKCenterLib_Login(ID,PW)))
time.sleep(1)

#登錄報價伺服器
print("EnterMonitor,", skC.SKCenterLib_GetReturnCodeMessage(skQ.SKQuoteLib_EnterMonitor()))
#每秒 pump event 一次，這裡示範15秒

# for i in range(15):
#     time.sleep(1)
while True:
    pythoncom.PumpWaitingMessages()
