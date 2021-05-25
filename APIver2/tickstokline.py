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
        # self.ticksdf=pd.DataFrame(columns=['ndatetime','nbid','nask','close','volume'])
        # self.ticksdf['ndatetime']=pd.to_datetime(self.ticksdf['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
        self.ticklst = []
        self.hisbol = 1 # 1:下載歷史資料至list, 2: 處理歷史list 3: 即時
        self.contractkpd=pd.read_csv('../result.dat')
        self.contractkpd['ndatetime']=pd.to_datetime(self.contractkpd['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
        self.contractkpd.sort_values(by=['ndatetime'],ascending=True)
        self.contractkpd=self.contractkpd.reset_index(drop=True)
        self.contractkpd[['open','high','low','close','volume']]=self.contractkpd[['open','high','low','close','volume']].astype(int)
        self.contractkpd['high_avg'] = self.contractkpd.high.rolling(self.MA).mean().round(0)
        self.contractkpd['low_avg'] = self.contractkpd.low.rolling(self.MA).mean().round(0)
        self.lastidx = self.contractkpd.last_valid_index()
        self.High=self.contractkpd.at[self.lastidx,'high']
        self.Low=self.contractkpd.at[self.lastidx,'low']
        self.lasttick=self.contractkpd.at[self.lastidx,'ndatetime']
        self.drawMA = False
        self.tmpcontract=0
        self.CheckHour=None

    def hisprocess(self,nlist):
        for row in nlist:
            if row[0]>=self.lasttick:
                tmphour=row[0].hour
                if self.tmpcontract==0 or self.tmpcontract==12000 or (tmphour==8 and self.CheckHour==4) or (tmphour==15 and (self.CheckHour is None or self.CheckHour==13)):
                    self.contractkpd=self.contractkpd.append(pd.DataFrame([[row[0],row[3],row[3],row[3],row[3],row[4], '', '']],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg']),ignore_index=True,sort=False)
                    self.High=self.Low=row[3]
                    self.tmpcontract=row[4]
                    self.drawMA=True
                    self.lastidx = self.contractkpd.last_valid_index()
                elif (self.tmpcontract+row[4])>12000:
                    if row[3] > self.High or row[3] < self.Low :
                        self.contractkpd.at[self.lastidx,'high']=self.High=max(self.contractkpd.at[self.lastidx,'high'],row[3])
                        self.contractkpd.at[self.lastidx,'low']=self.Low=min(self.contractkpd.at[self.lastidx,'low'],row[3])
                    self.contractkpd.at[self.lastidx,'close']=row[3]
                    self.contractkpd.at[self.lastidx,'volume']=12000
                    self.tmpcontract=self.tmpcontract+row[4]-12000
                    self.contractkpd=self.contractkpd.append(pd.DataFrame([[row[0],row[3],row[3],row[3],row[3],self.tmpcontract, '', '']],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg']),ignore_index=True,sort=False)
                    self.High=self.Low=row[3]
                    self.drawMA=True
                    self.lastidx = self.contractkpd.last_valid_index()
                else:
                    if row[3] > self.High or row[3] < self.Low:
                        self.contractkpd.at[self.lastidx,'high']=self.High=max(self.contractkpd.at[self.lastidx,'high'],row[3])
                        self.contractkpd.at[self.lastidx,'low']=self.Low=min(self.contractkpd.at[self.lastidx,'low'],row[3])
                    self.contractkpd.at[self.lastidx,'close']=row[3]
                    # self.tmpcontract=self.tmpcontract+row[4]
                    self.contractkpd.at[self.lastidx,'volume']=self.tmpcontract=self.tmpcontract+row[4]
                    self.drawMA=False
                # else:
                #     print('Ticks Error!!: ',ndatetime,',',nClose,',',row[4])
                
                if self.drawMA :
                    self.contractkpd['high_avg'] = self.contractkpd.high.rolling(self.MA).mean()
                    self.contractkpd['low_avg'] = self.contractkpd.low.rolling(self.MA).mean()
                self.lasttick=row[0]
                self.CheckHour=tmphour
        self.hisbol=3


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
            self.contractkpd['high_avg'] = self.contractkpd.high.rolling(self.MA).mean().round(0)
            self.contractkpd['low_avg'] = self.contractkpd.low.rolling(self.MA).mean().round(0)
        
        self.CheckHour=tmphour

    def Ticks(self,nDate,nTimehms,nTimemillismicros,nBid,nAsk,nClose,nQty):
        nTime=str(nTimehms).zfill(6)
        nTimemicro=str(nTimemillismicros).zfill(6)
        ndatetime=datetime.datetime.strptime(str(nDate)+" "+nTime+"."+nTimemicro.strip(),'%Y%m%d %H%M%S.%f')
        if self.hisbol==1:
            # self.ticksdf=self.ticksdf.append(pd.DataFrame([[ndatetime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty)]],columns=['ndatetime','nbid','nask','close','volume']),ignore_index=True,sort=False)
            self.ticklst.append([ndatetime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty)])
            # self.contractk(ndatetime,int(nClose/100),int(nQty))
            # self.lasttick=ndatetime
        elif self.hisbol==3:
            # self.ticksdf=self.ticksdf.append(pd.DataFrame([[ndatetime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty)]],columns=['ndatetime','nbid','nask','close','volume']),ignore_index=True,sort=False)
            self.ticklst.append([ndatetime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty)])
            self.contractk(ndatetime,int(nClose/100),int(nQty))
            self.lasttick=ndatetime
        elif self.hisbol==2:
            self.ticklst.append([ndatetime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty)])
            self.hisprocess(self.ticklst)
        else:
            print('Ticks處理發生錯誤',',',self.hisbol,',',ndatetime,',',self.lasttick)

