#匯入所需module
import datetime
import time
import numpy as np
import pandas as pd


class dataprocess:
    def __init__(self,type,name):
        self.name=name
        self.type=type
        self.klinepd=pd.DataFrame(columns=['date','time','open','high','low','close','volume'])
        self.contractkpd=pd.DataFrame(columns=['ndatetime','open','high','low','close','volume'])
        self.newlist=[]
        self.tmpcontract=0
    
    def Ticks(self,sMarketNo,sIndex,nPtr,nTimehms,nTimemillismicros,nBid,nAsk,nClose,nQty,nSimulate):
        nTime=str(nTimehms)
        while len(nTime)<6:
            nTime='0'+nTime
        nTimemicro=str(nTimemillismicros)
        while len(nTimemicro)<6:
            nTimemicro='0'+nTimemicro
        nTime=datetime.datetime.strptime(nTime,'%H%M%S').strftime('%H:%M:%S')+"."+nTimemicro.strip()
        nDate=datetime.datetime.now().strftime('%Y/%m/%d')
        self.newlist=[nDate,nTime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty)]
        return self.newlist
    
    def contractk(self,nDate,nTime,nBid,nAsk,nClose,nQty):
        ndatetime=datetime.datetime.strptime(nDate+' '+nTime,'%Y/%m/%d %H:%M:%S.%f')
        if self.tmpcontract==0 or self.tmpcontract==12000:
            self.contractkpd.loc['ndatetime']=[ndatetime,nClose,nClose,nClose,nClose,nQty]
            self.tmpcontract=nQty
        elif (self.tmpcontract+nQty) < 12000:
            self.contractkpd.iloc[-1,2]=max(self.contractkpd.iloc[-1,2],nClose)
            self.contractkpd.iloc[-1,3]=min(self.contractkpd.iloc[-1,3],nClose)
            self.contractkpd.iloc[-1,4]=nClose
            self.contractkpd.iloc[-1,5]+=nQty
            self.tmpcontract+=nQty
        elif (self.tmpcontract+nQty)>12000:
            self.contractkpd.iloc[-1,2]=max(self.contractkpd.iloc[-1,2],nClose)
            self.contractkpd.iloc[-1,3]=min(self.contractkpd.iloc[-1,3],nClose)
            self.contractkpd.iloc[-1,4]=nClose
            self.contractkpd.iloc[-1,5]=12000
            nQty=self.tmpcontract+nQty-12000
            self.contractkpd.loc['ndatetime']=[ndatetime,nClose,nClose,nClose,nClose,nQty]
        else:
            self.contractkpd.iloc[-1,2]=max(self.contractkpd.iloc[-1,2],nClose)
            self.contractkpd.iloc[-1,3]=min(self.contractkpd.iloc[-1,3],nClose)
            self.contractkpd.iloc[-1,4]=nClose
            self.contractkpd.iloc[-1,5]+=nQty
            self.tmpcontract+=nQty
        return self.contractkpd.iloc[-1:].values







        
