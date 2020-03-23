#匯入所需module
import datetime
import time
import numpy as np
import pandas as pd
# from mpl_finance import candlestick2_ohlc
# import matplotlib.dates as mdates
# import matplotlib.pyplot as plt
# setting about combobox
KLINETYPESET = (
    "0 = 1分鐘線","4 = 完整日線","5 = 週線","6 = 月線",
)

KLINEOUTTYPESET = (
    "0 = 舊版輸出格式", "1 = 新版輸出格式",
)

TRADESESSIONSET = (
    "0 = 全盤K線(國內期選用)", "1 = AM盤K線(國內期選用)",
)

class dataprocess:
    def __init__(self,inputname):
        self.name=inputname
        # self.contractkpd=pd.DataFrame(columns=['ndatetime','open','high','low','close','volume'])
        self.ticksdf=pd.DataFrame(columns=['ndate','ntime','nbid','nask','close','volume'])
        self.ticksdf['ndate']=pd.to_datetime(self.ticksdf['ndate'],format='%Y-%m-%d')
        self.ticksdf['ntime']=pd.to_datetime(self.ticksdf['ntime'],format='%H:%M:%S.%f')
        self.contractkpd=pd.read_csv('result.dat')
        self.contractkpd['ndatetime']=pd.to_datetime(self.contractkpd['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
        self.contractkpd.sort_values(by=['ndatetime'],ascending=True)
        self.contractkpd=self.contractkpd.reset_index(drop=True)
        self.newlist=[]
        self.tmpcontract=0
        self.CheckHour=0

    def contractk(self,xdatetime,nBid,nAsk,nClose,nQty):
        ndatetime=datetime.datetime.strptime(xdatetime,'%Y-%m-%d %H:%M:%S.%f')
        tmphour=ndatetime.hour
        if self.contractkpd.shape[0]==0 or self.tmpcontract==0 or self.tmpcontract==12000 or (tmphour==8 and self.CheckHour==4) or (tmphour==15 and self.CheckHour==13):
            self.contractkpd=self.contractkpd.append(pd.DataFrame([[ndatetime,nClose,nClose,nClose,nClose,nQty]],columns=['ndatetime','open','high','low','close','volume']),ignore_index=True)
            self.tmpcontract=nQty
        elif (self.tmpcontract+nQty)>12000:
            self.contractkpd.iloc[-1,2]=max(self.contractkpd.iloc[-1,2],nClose)
            self.contractkpd.iloc[-1,3]=min(self.contractkpd.iloc[-1,3],nClose)
            self.contractkpd.iloc[-1,4]=nClose
            self.contractkpd.iloc[-1,5]=12000
            self.tmpcontract=self.tmpcontract+nQty-12000
            self.contractkpd.loc[ndatetime]=[ndatetime,nClose,nClose,nClose,nClose,self.tmpcontract]
        else:
            self.contractkpd.iloc[-1,2]=max(self.contractkpd.iloc[-1,2],nClose)
            self.contractkpd.iloc[-1,3]=min(self.contractkpd.iloc[-1,3],nClose)
            self.contractkpd.iloc[-1,4]=nClose
            self.tmpcontract=self.tmpcontract+nQty
            self.contractkpd.iloc[-1,5]=self.tmpcontract
        # self.contractkpd.reset_index(drop=True)
        self.CheckHour=tmphour
        return self.contractkpd.iloc[-1:].values

    def Ticks(self,nDate,nTimehms,nTimemillismicros,nBid,nAsk,nClose,nQty):
        nTime=str(nTimehms).zfill(6)
        # while len(nTime)<6:
        #     nTime='0'+nTime
        nTimemicro=str(nTimemillismicros).zfill(6)
        # while len(nTimemicro)<6:
        #     nTimemicro='0'+nTimemicro
        # nTime=datetime.datetime.strptime(nTime,'%H%M%S').strftime('%H:%M:%S')+"."+nTimemicro.strip()
        ndatetime=datetime.datetime.strptime(str(nDate)+" "+nTime,'%Y%m%d %H%M%S').strftime('%Y-%m-%d %H:%M:%S')+"."+nTimemicro.strip()
        ndate=datetime.datetime.strptime(str(nDate),'%Y%m%d').date()
        ntime=datetime.datetime.strptime(nTime+"."+nTimemicro.strip(),'%H%M%S.%f').time()
        self.newlist=[ndate,ntime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty)]
        tmplist=[[ndate,ntime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty)]]
        self.ticksdf=self.ticksdf.append(pd.DataFrame(tmplist,columns=['ndate','ntime','nbid','nask','close','volume']),ignore_index=True)
        self.contractk(ndatetime,self.newlist[2],self.newlist[3],self.newlist[4],self.newlist[5])
        return self.newlist
    









        
