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
        self.MA=87
        # self.contractkpd=pd.DataFrame(columns=['ndatetime','open','high','low','close','volume'])
        self.ticksdf=pd.DataFrame(columns=['ndatetime','nbid','nask','close','volume'])
        self.ticksdf['ndatetime']=pd.to_datetime(self.ticksdf['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
        self.contractkpd=pd.read_csv('../result.dat')
        self.contractkpd['ndatetime']=pd.to_datetime(self.contractkpd['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
        self.contractkpd.sort_values(by=['ndatetime'],ascending=True)
        self.contractkpd=self.contractkpd.reset_index(drop=True)
        self.contractkpd['high_avg'] = self.contractkpd.high.rolling(self.MA).mean().round(2)
        self.contractkpd['low_avg'] = self.contractkpd.low.rolling(self.MA).mean().round(2)
        self.lastidx = self.contractkpd.last_valid_index()
        self.High=self.contractkpd.at[self.lastidx,'high']
        self.Low=self.contractkpd.at[self.lastidx,'low']
        self.lasttick=self.contractkpd.at[self.lastidx,'ndatetime']
        self.drawMA = False
        self.tmpcontract=0
        self.CheckHour=None

    def contractk(self,ndatetime,nClose,nQty):
        tmphour=ndatetime.hour
        if self.tmpcontract==0 or self.tmpcontract==12000 or (tmphour==8 and self.CheckHour==4) or (tmphour==15 and (self.CheckHour is None or self.CheckHour==13)):
            self.contractkpd=self.contractkpd.append(pd.DataFrame([[ndatetime,nClose,nClose,nClose,nClose,nQty, '', '']],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg']),ignore_index=True,sort=False)
            self.High=self.Low=nClose
            self.tmpcontract=nQty
            self.drawMA=True
            self.lastidx = self.contractkpd.last_valid_index()
        elif (self.tmpcontract+nQty)>12000:
            if nClose > self.High or nClose < self.Low :
                self.contractkpd.at[self.lastidx,'high']=self.High=max(self.contractkpd.at[self.lastidx,'high'],nClose)
                self.contractkpd.at[self.lastidx,'low']=self.Low=min(self.contractkpd.at[self.lastidx,'low'],nClose)
            self.contractkpd.at[self.lastidx,'close']=nClose
            self.contractkpd.at[self.lastidx,'volume']=12000
            self.tmpcontract=self.tmpcontract+nQty-12000
            self.contractkpd=self.contractkpd.append(pd.DataFrame([[ndatetime,nClose,nClose,nClose,nClose,self.tmpcontract, '', '']],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg']),ignore_index=True,sort=False)
            self.High=self.Low=nClose
            self.drawMA=True
            self.lastidx = self.contractkpd.last_valid_index()
        else:
            if nClose > self.High or nClose < self.Low:
                self.contractkpd.at[self.lastidx,'high']=self.High=max(self.contractkpd.at[self.lastidx,'high'],nClose)
                self.contractkpd.at[self.lastidx,'low']=self.Low=min(self.contractkpd.at[self.lastidx,'low'],nClose)
            self.contractkpd.at[self.lastidx,'close']=nClose
            # self.tmpcontract=self.tmpcontract+nQty
            self.contractkpd.at[self.lastidx,'volume']=self.tmpcontract=self.tmpcontract+nQty
            self.drawMA=False
        # else:
        #     print('Ticks Error!!: ',ndatetime,',',nClose,',',nQty)
        
        if self.drawMA :
            self.contractkpd['high_avg'] = self.contractkpd.high.rolling(self.MA).mean().round(2)
            self.contractkpd['low_avg'] = self.contractkpd.low.rolling(self.MA).mean().round(2)
        
        self.CheckHour=tmphour

    def Ticks(self,nDate,nTimehms,nTimemillismicros,nBid,nAsk,nClose,nQty):
        nTime=str(nTimehms).zfill(6)
        nTimemicro=str(nTimemillismicros).zfill(6)
        ndatetime=datetime.datetime.strptime(str(nDate)+" "+nTime+"."+nTimemicro.strip(),'%Y%m%d %H%M%S.%f')
        if ndatetime > self.lasttick:
            self.ticksdf=self.ticksdf.append(pd.DataFrame([[ndatetime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty)]],columns=['ndatetime','nbid','nask','close','volume']),ignore_index=True,sort=False)
            self.contractk(ndatetime,int(nClose/100),int(nQty))
            self.lasttick=ndatetime
