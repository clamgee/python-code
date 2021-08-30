#匯入所需module
import datetime
import time
import numpy as np
import pandas as pd
import os

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
        self.ticksum = 0
        self.ticklst = []
        self.tickclose = 0
        direct=os.path.abspath('../data')
        filelist = os.listdir('../data')
        file = filelist[-1]
        tmpdf = pd.read_csv(direct+'\\'+file,header=None,names=['ndatetime','nbid','nask','close','volume','deal'])
        self.yesterdayclose = tmpdf.at[tmpdf.last_valid_index(),'close']
        print(self.yesterdayclose)
        del tmpdf
        self.hisbol = 1 # 1:下載歷史資料至list, 2: 處理歷史list 3: 即時
        self.contractkpd=pd.read_csv('../result.dat',low_memory=False)
        self.contractkpd['ndatetime']=pd.to_datetime(self.contractkpd['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
        self.contractkpd.sort_values(by=['ndatetime'],ascending=True)
        self.contractkpd=self.contractkpd.reset_index(drop=True)
        self.contractkpd[['open','high','low','close','volume']]=self.contractkpd[['open','high','low','close','volume']].astype(int)
        self.contractkpd['high_avg'] = self.contractkpd.high.rolling(self.MA).mean().round(0)
        self.contractkpd['low_avg'] = self.contractkpd.low.rolling(self.MA).mean().round(0)
        self.contractkpd['dealbid']=0
        self.contractkpd['dealask']=0
        self.contractkpd['dealminus']=0
        self.contractkpd[['dealbid','dealask','dealminus']]=self.contractkpd[['dealbid','dealask','dealminus']].astype(int)
        self.lastidx = self.contractkpd.last_valid_index()
        self.High=self.contractkpd.at[self.lastidx,'high']
        self.Low=self.contractkpd.at[self.lastidx,'low']
        self.lasttick=self.contractkpd.at[self.lastidx,'ndatetime']
        self.drawMA = False
        self.tmpcontract=0
        self.CheckHour=None
        self.mindf = None
        self.mm=0
        self.mm1=0
        self.minlastidx=0
        self.minhigh=0
        self.minlow=0
        self.interval=1

    def hisprocess(self,nlist):
        for row in nlist:
            # if row[0]>=self.lasttick:
            tmphour=row[0].hour
            if (tmphour==8 and self.CheckHour==4) or (tmphour==15 and (self.CheckHour is None or self.CheckHour==13)):
                self.contractkpd=self.contractkpd.append(pd.DataFrame([[row[0],row[3],row[3],row[3],row[3],row[4],0,0,0,0,0]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg','dealbid','dealask','dealminus']),ignore_index=True,sort=False)
                self.High=self.Low=row[3]
                self.tmpcontract=row[4]
                self.ticksum=row[4]
                self.lastidx = self.contractkpd.last_valid_index()

            elif self.tmpcontract==0 or self.tmpcontract==12000 :
                self.contractkpd=self.contractkpd.append(pd.DataFrame([[row[0],row[3],row[3],row[3],row[3],row[4],0,0,self.contractkpd.at[self.lastidx,'dealbid'],self.contractkpd.at[self.lastidx,'dealask'],self.contractkpd.at[self.lastidx,'dealminus']]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg','dealbid','dealask','dealminus']),ignore_index=True,sort=False)
                self.High=self.Low=row[3]
                self.tmpcontract=row[4]
                self.ticksum+=row[4]
                self.lastidx = self.contractkpd.last_valid_index()

            elif (self.tmpcontract+row[4])>12000:
                if row[3] > self.High or row[3] < self.Low :
                    self.contractkpd.at[self.lastidx,'high']=self.High=max(self.contractkpd.at[self.lastidx,'high'],row[3])
                    self.contractkpd.at[self.lastidx,'low']=self.Low=min(self.contractkpd.at[self.lastidx,'low'],row[3])
                self.contractkpd.at[self.lastidx,'close']=row[3]
                self.contractkpd.at[self.lastidx,'volume']=12000
                self.ticksum+=row[4]
                self.tmpcontract=self.tmpcontract+row[4]-12000
                self.contractkpd=self.contractkpd.append(pd.DataFrame([[row[0],row[3],row[3],row[3],row[3],self.tmpcontract,0,0,self.contractkpd.at[self.lastidx,'dealbid'],self.contractkpd.at[self.lastidx,'dealask'],self.contractkpd.at[self.lastidx,'dealminus']]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg','dealbid','dealask','dealminus']),ignore_index=True,sort=False)
                self.High=self.Low=row[3]
                self.lastidx = self.contractkpd.last_valid_index()

            else:
                if row[3] > self.High or row[3] < self.Low:
                    self.contractkpd.at[self.lastidx,'high']=self.High=max(self.contractkpd.at[self.lastidx,'high'],row[3])
                    self.contractkpd.at[self.lastidx,'low']=self.Low=min(self.contractkpd.at[self.lastidx,'low'],row[3])
                self.contractkpd.at[self.lastidx,'close']=row[3]
                self.ticksum+=row[4]
                self.contractkpd.at[self.lastidx,'volume']=self.tmpcontract=self.tmpcontract+row[4]

            if row[5]>0:
                self.contractkpd.at[self.lastidx,'dealbid']+=row[5]
            else:
                self.contractkpd.at[self.lastidx,'dealask']-=row[5]
            self.contractkpd.at[self.lastidx,'dealminus']+=row[5]

            self.lasttick=row[0]
            self.CheckHour=tmphour

        self.contractkpd['high_avg'] = self.contractkpd.high.rolling(self.MA).mean()
        self.contractkpd['low_avg'] = self.contractkpd.low.rolling(self.MA).mean()

    def histicktomin(self,nlist):
        dayticks = pd.DataFrame(nlist,columns=['ndatetime','nbid','nask','close','volume','deal'])
        dayticks['ndatetime']=pd.to_datetime(dayticks['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
        now = time.localtime(time.time()).tm_hour
        if now>14 or now<8 :
            dayticks=dayticks[(dayticks.ndatetime.dt.hour>14) | (dayticks.ndatetime.dt.hour<8)] # 夜盤
        elif now>=8 and now<15:
            dayticks=dayticks[(dayticks.ndatetime.dt.hour>=8) & (dayticks.ndatetime.dt.hour<15)] # 日盤
        dayticks.sort_values(by=['ndatetime'],ascending=True)
        dayticks.index = dayticks.ndatetime
        self.mindf=dayticks['close'].resample('1min',closed='right').ohlc()
        tmpdf=dayticks['volume'].resample('1min').sum()
        self.mindf=pd.concat([self.mindf,tmpdf],axis=1)
        del tmpdf
        tmpdf=dayticks['deal'].resample('1min').sum()
        self.mindf=pd.concat([self.mindf,tmpdf],axis=1)
        del tmpdf
        self.mindf=self.mindf.dropna()
        self.mindf['dealminus']=self.mindf['deal'].cumsum()
        del self.mindf['deal']
        self.mindf=self.mindf.rename_axis('ndatetime').reset_index()
        self.mindf['ndatetime'] = pd.to_datetime(self.mindf['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
        self.mindf['big']=0
        self.mindf['small']=0
        self.mindf[['open','high','low','close','volume','dealminus','big','small']]= self.mindf[['open','high','low','close','volume','dealminus','big','small']].astype(int)
        self.minlastidx=self.mindf.last_valid_index()
        if self.minlastidx!=0:
            self.mm=self.mindf.at[self.minlastidx,'ndatetime'].replace(second=0,microsecond=0)
            self.mm1=self.mm+datetime.timedelta(minutes=self.interval)
            self.minhigh=self.mindf.at[self.minlastidx,'high']
            self.minlow=self.mindf.at[self.minlastidx,'low']
        # print(self.mindf.tail())

    def tick2min(self,ndatetime,nClose,nQty,deal):
        if self.minlastidx==0 or ndatetime>=self.mm1:
            self.mm=ndatetime.replace(second=0,microsecond=0)
            self.mm1=self.mm+datetime.timedelta(minutes=self.interval)
            # print(self.mindf.tail(1))
            tmpdeal=self.mindf.at[self.minlastidx,'dealminus']+deal
            self.mindf=self.mindf.append(pd.DataFrame([[self.mm,nClose,nClose,nClose,nClose,nQty,tmpdeal,self.mindf.at[self.minlastidx,'big'],self.mindf.at[self.minlastidx,'small']]],columns=['ndatetime','open','high','low','close','volume','dealminus','big','small']),ignore_index=True,sort=False)
            self.minhigh = self.minlow = nClose
            self.minlastidx=self.mindf.last_valid_index()
        elif ndatetime < self.mm1 :
            self.mindf.at[self.minlastidx,'close']=nClose
            self.mindf.at[self.minlastidx,'volume']+=nQty
            self.mindf.at[self.minlastidx,'dealminus']+=deal
            if self.minhigh < nClose or self.minlow > nClose:
                self.mindf.at[self.minlastidx,'high']=self.minhigh=max(self.minhigh,nClose)
                self.mindf.at[self.minlastidx,'low']=self.minlow=min(self.minlow,nClose)
        else:
            print('有錯誤:',self.mm,',',self.mm1,',',self.minlastidx,ndatetime)


    def contractk(self,ndatetime,nClose,nQty,deal):
        tmphour=ndatetime.hour
        if (tmphour==8 and self.CheckHour==4) or (tmphour==15 and (self.CheckHour is None or self.CheckHour==13)):
            self.contractkpd=self.contractkpd.append(pd.DataFrame([[ndatetime,nClose,nClose,nClose,nClose,nQty,0,0,0,0,0]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg','dealbid','dealask','dealminus']),ignore_index=True,sort=False)
            self.High=self.Low=nClose
            self.tmpcontract=nQty
            self.ticksum=nQty
            self.drawMA=True
            self.lastidx = self.contractkpd.last_valid_index()
        
        elif self.tmpcontract==0 or self.tmpcontract==12000 :
            self.contractkpd=self.contractkpd.append(pd.DataFrame([[ndatetime,nClose,nClose,nClose,nClose,nQty,0,0,self.contractkpd.at[self.lastidx,'dealbid'],self.contractkpd.at[self.lastidx,'dealask'],self.contractkpd.at[self.lastidx,'dealminus']]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg','dealbid','dealask','dealminus']),ignore_index=True,sort=False)
            self.High=self.Low=nClose
            self.ticksum+=nQty
            self.tmpcontract=nQty
            self.drawMA=True
            self.lastidx = self.contractkpd.last_valid_index()

        elif (self.tmpcontract+nQty)>12000:
            if nClose > self.High or nClose < self.Low :
                self.contractkpd.at[self.lastidx,'high']=self.High=max(self.contractkpd.at[self.lastidx,'high'],nClose)
                self.contractkpd.at[self.lastidx,'low']=self.Low=min(self.contractkpd.at[self.lastidx,'low'],nClose)
            self.contractkpd.at[self.lastidx,'close']=nClose
            self.contractkpd.at[self.lastidx,'volume']=12000
            self.ticksum+=nQty
            self.tmpcontract=self.tmpcontract+nQty-12000
            self.contractkpd=self.contractkpd.append(pd.DataFrame([[ndatetime,nClose,nClose,nClose,nClose,self.tmpcontract,0,0,self.contractkpd.at[self.lastidx,'dealbid'],self.contractkpd.at[self.lastidx,'dealask'],self.contractkpd.at[self.lastidx,'dealminus']]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg','dealbid','dealask','dealminus']),ignore_index=True,sort=False)
            self.lastidx = self.contractkpd.last_valid_index()
            self.High=self.Low=nClose
            self.drawMA=True

        else:
            if nClose > self.High or nClose < self.Low:
                self.contractkpd.at[self.lastidx,'high']=self.High=max(self.contractkpd.at[self.lastidx,'high'],nClose)
                self.contractkpd.at[self.lastidx,'low']=self.Low=min(self.contractkpd.at[self.lastidx,'low'],nClose)
            self.contractkpd.at[self.lastidx,'close']=nClose
            self.ticksum+=nQty
            self.contractkpd.at[self.lastidx,'volume']=self.tmpcontract=self.tmpcontract+nQty
            self.drawMA=False
        if deal > 0 :
            self.contractkpd.at[self.lastidx,'dealbid']+=deal
        else:
            self.contractkpd.at[self.lastidx,'dealask']-=deal
        self.contractkpd.at[self.lastidx,'dealminus']+=deal
        if self.drawMA :
            self.contractkpd['high_avg'] = self.contractkpd.high.rolling(self.MA).mean().round(0)
            self.contractkpd['low_avg'] = self.contractkpd.low.rolling(self.MA).mean().round(0)
        
        self.CheckHour=tmphour

    def Ticks(self,nDate,nTimehms,nTimemillismicros,nBid,nAsk,nClose,nQty):
        nTime=str(nTimehms).zfill(6)
        nTimemicro=str(nTimemillismicros).zfill(6)
        ndatetime=datetime.datetime.strptime(str(nDate)+" "+nTime+"."+nTimemicro.strip(),'%Y%m%d %H%M%S.%f')
        if self.tickclose!=0 and (nClose > self.tickclose or nClose >= nAsk):
            deal = nQty
            self.tickclose = nClose
        elif self.tickclose!=0 and (nClose < self.tickclose or nClose <= nBid):
            deal = 0-nQty
            self.tickclose = nClose
        else:
            if nClose >=nAsk:
                deal = nQty
            else:
                deal = 0 - nQty
            self.tickclose = nClose
        if self.hisbol==1:
            # self.ticksdf=self.ticksdf.append(pd.DataFrame([[ndatetime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty)]],columns=['ndatetime','nbid','nask','close','volume']),ignore_index=True,sort=False)
            self.ticklst.append([ndatetime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty),int(deal)])
            # self.contractk(ndatetime,int(nClose/100),int(nQty))
            # self.lasttick=ndatetime
        elif self.hisbol==3:
            # self.ticksdf=self.ticksdf.append(pd.DataFrame([[ndatetime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty)]],columns=['ndatetime','nbid','nask','close','volume']),ignore_index=True,sort=False)
            self.ticklst.append([ndatetime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty),int(deal)])
            self.tick2min(ndatetime,int(nClose/100),int(nQty),int(deal))
            self.contractk(ndatetime,int(nClose/100),int(nQty),int(deal))
            self.lasttick=ndatetime
        elif self.hisbol==2:
            self.ticklst.append([ndatetime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty),int(deal)])
            self.hisprocess(self.ticklst)
            self.histicktomin(self.ticklst)
            self.hisbol=3

        else:
            print('Ticks處理發生錯誤',',',self.hisbol,',',ndatetime,',',self.lasttick)

