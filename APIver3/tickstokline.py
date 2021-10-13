#匯入所需module
import datetime
import time,os
import numpy as np
import pandas as pd
import multiprocessing as mp
from PySide6.QtCore import QThread


class DataToTicks(QThread):
    def __init__(self,inputname,inputindex,inputTuple):
        super(DataToTicks, self).__init__()
        self.name=inputname
        self.commodityIndex = inputindex
        self.__queue = inputTuple[0]
        self.__connect12K_queue = inputTuple[1]
        self.__connectMinuteK_queue = inputTuple[2]
        self.TickList = []
        self.ListTransform = False
        self.LastTick = 0
        self.LastTickClose = 0
        self.hisbol = True #是否為歷史Data

    def Ticks(self,nlist):
        # [int(nPtr),str(lDate),str(lTimehms),str(lTimemillismicros),int(nBid),int(nAsk),int(nclose),int(nQty),nhis]
        nPtr=nlist[0]; nDate=str(nlist[1]); nTime=str(nlist[2]).zfill(6); nTimemicro = nlist[3].zfill(6)
        nBid=nlist[4]; nAsk=nlist[5]; nclose=nlist[6]; nQty=nlist[7]; self.hisbol=nlist[8]; deal=0
        ndatetime=datetime.datetime.strptime(nDate+" "+nTime+"."+nTimemicro,'%Y%m%d %H%M%S.%f')
        if self.LastTick < nPtr:
            self.LastTick = nPtr
            if self.LastTickClose != 0:
                if(nclose > self.LastTickClose) or (nclose >= nAsk):
                    deal = nQty
                elif (nclose < self.LastTickClose) or (nclose <= nBid):
                    deal = 0-nQty
                else:
                    try:
                        deal = 0
                    except Exception as e:
                        print(nPtr,self.LastTickClose,'Ticks 處理力道錯誤: ',nlist,'系統資訊: ',e)
            else:
                if nclose >=nAsk:
                    deal = nQty
                else:
                    deal = 0 - nQty
            self.LastTickClose = nclose
            # True:下載歷史資料至list, 2: 處理歷史list 3: 即時
            if self.hisbol:
                self.TickList.append([ndatetime,int(nBid/100),int(nAsk/100),int(nclose/100),int(nQty),int(deal)])
            else:
                if self.ListTransform == False:
                    self.__connect12K_queue.put([self.ListTransform,self.TickList,nPtr])
                    self.__connectMinuteK_queue.put([self.ListTransform,self.TickList,nPtr])
                    print('transform List',len(self.TickList))
                    self.ListTransform = True
                    self.TickList.append([ndatetime,int(nBid/100),int(nAsk/100),int(nclose/100),int(nQty),int(deal)])
                    self.__connect12K_queue.put([self.ListTransform,[ndatetime,int(nclose/100),int(nQty)],nPtr])
                    self.__connectMinuteK_queue.put([self.ListTransform,[ndatetime,int(nclose/100),int(nQty),int(deal)],nPtr])
                else:
                    self.TickList.append([ndatetime,int(nBid/100),int(nAsk/100),int(nclose/100),int(nQty),int(deal)])
                    self.__connect12K_queue.put([self.ListTransform,[ndatetime,int(nclose/100),int(nQty)],nPtr])
                    self.__connectMinuteK_queue.put([self.ListTransform,[ndatetime,int(nclose/100),int(nQty),int(deal)],nPtr])
        else:
            print('捨棄Tick序號: ',nPtr)

    def run(self):
        while True:
            nlist = self.__queue.get()
            if nlist is not None :
                self.Ticks(nlist)

class TicksTo12K(QThread):
    def __init__(self,inputname,inputindex,inputTuple):
        super(TicksTo12K, self).__init__()
        self.name = inputname
        self.commodityIndex = inputindex
        self.__Queue = inputTuple[0]
        self.__CandleTarget = inputTuple[1]
        self.__CandleItem12K_Event = inputTuple[2]
        self.__Candledf12K = inputTuple[3]
        self.Candledf=pd.read_csv('../result.dat',low_memory=False)
        self.Candledf['ndatetime']=pd.to_datetime(self.Candledf['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
        self.Candledf.sort_values(by=['ndatetime'],ascending=True)
        self.Candledf=self.Candledf.reset_index(drop=True)
        self.Candledf[['open','high','low','close','volume']]=self.Candledf[['open','high','low','close','volume']].astype(int)
        self.MA = 87
        self.Candledf['high_avg'] = self.Candledf.high.rolling(self.MA).mean().round(0)
        self.Candledf['low_avg'] = self.Candledf.low.rolling(self.MA).mean().round(0)
        self.lastidx = self.Candledf.last_valid_index()
        self.High = self.Candledf['high'].max()
        self.Low = self.Candledf['low'].min()
        self.Close = self.Candledf.at[self.lastidx,'close']
        self.CheckHour = None
        self.HisDone = False

    def HisListProcess(self,nlist):
        for row in nlist:
            tmphour=row[0].hour
            if (tmphour==8 and self.CheckHour==4) or (tmphour==15 and (self.CheckHour is None or self.CheckHour==13)):
                self.Candledf=self.Candledf.append(pd.DataFrame([[row[0],row[3],row[3],row[3],row[3],row[4],0,0]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg']),ignore_index=True,sort=False)
                self.High=self.Low=self.Close=row[3]
                self.tmpcontract=row[4]
                self.lastidx = self.Candledf.last_valid_index()
            elif self.tmpcontract==0 or self.tmpcontract==12000 :
                self.Candledf=self.Candledf.append(pd.DataFrame([[row[0],row[3],row[3],row[3],row[3],row[4],0,0]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg']),ignore_index=True,sort=False)
                self.High=self.Low=self.Close=row[3]
                self.tmpcontract=row[4]
                self.lastidx = self.Candledf.last_valid_index()
            elif (self.tmpcontract+row[4])>12000:
                if row[3] > self.High or row[3] < self.Low :
                    self.Candledf.at[self.lastidx,'high']=self.High=max(self.Candledf.at[self.lastidx,'high'],row[3])
                    self.Candledf.at[self.lastidx,'low']=self.Low=min(self.Candledf.at[self.lastidx,'low'],row[3])
                self.Candledf.at[self.lastidx,'close']=self.Close=row[3]
                self.Candledf.at[self.lastidx,'volume']=12000
                self.tmpcontract=self.tmpcontract+row[4]-12000
                self.Candledf=self.Candledf.append(pd.DataFrame([[row[0],row[3],row[3],row[3],row[3],self.tmpcontract,0,0]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg']),ignore_index=True,sort=False)
                self.High=self.Low=self.Close=row[3]
                self.lastidx = self.Candledf.last_valid_index()
            else:
                if row[3] > self.High or row[3] < self.Low:
                    self.Candledf.at[self.lastidx,'high']=self.High=max(self.Candledf.at[self.lastidx,'high'],row[3])
                    self.Candledf.at[self.lastidx,'low']=self.Low=min(self.Candledf.at[self.lastidx,'low'],row[3])
                self.Candledf.at[self.lastidx,'close']=self.Close=row[3]
                self.Candledf.at[self.lastidx,'volume']=self.tmpcontract=self.tmpcontract+row[4]
            self.CheckHour=tmphour
        self.Candledf['high_avg'] = self.Candledf.high.rolling(self.MA).mean()
        self.Candledf['low_avg'] = self.Candledf.low.rolling(self.MA).mean()

    def tickto12k(self,nlist):
        ndatetime = nlist[0]; nclose = nlist[1]; nQty = nlist[2]
        tmphour=ndatetime.hour
        if (tmphour==8 and self.CheckHour==4) or (tmphour==15 and (self.CheckHour is None or self.CheckHour==13)):
            self.Candledf=self.Candledf.append(pd.DataFrame([[ndatetime,nclose,nclose,nclose,nclose,nQty,0,0]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg']),ignore_index=True,sort=False)
            self.High=self.Low=self.Close=nclose
            self.tmpcontract=nQty
            self.drawMA=True
            self.lastidx = self.Candledf.last_valid_index()        
        elif self.tmpcontract==0 or self.tmpcontract==12000 :
            self.Candledf=self.Candledf.append(pd.DataFrame([[ndatetime,nclose,nclose,nclose,nclose,nQty,0,0]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg']),ignore_index=True,sort=False)
            self.High=self.Low=self.Close=nclose
            self.tmpcontract=nQty
            self.drawMA=True
            self.lastidx = self.Candledf.last_valid_index()
        elif (self.tmpcontract+nQty)>12000:
            if nclose > self.High or nclose < self.Low :
                self.Candledf.at[self.lastidx,'high']=self.High=max(self.Candledf.at[self.lastidx,'high'],nclose)
                self.Candledf.at[self.lastidx,'low']=self.Low=min(self.Candledf.at[self.lastidx,'low'],nclose)
            self.Candledf.at[self.lastidx,'close']=self.Close=nclose
            self.Candledf.at[self.lastidx,'volume']=12000
            self.tmpcontract=self.tmpcontract+nQty-12000
            self.Candledf=self.Candledf.append(pd.DataFrame([[ndatetime,nclose,nclose,nclose,nclose,self.tmpcontract,0,0]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg']),ignore_index=True,sort=False)
            self.lastidx = self.Candledf.last_valid_index()
            self.High=self.Low=self.Close=nclose
            self.drawMA=True
        else:
            if nclose > self.High or nclose < self.Low:
                self.Candledf.at[self.lastidx,'high']=self.High=max(self.Candledf.at[self.lastidx,'high'],nclose)
                self.Candledf.at[self.lastidx,'low']=self.Low=min(self.Candledf.at[self.lastidx,'low'],nclose)
            self.Candledf.at[self.lastidx,'close']=self.Close=nclose
            self.Candledf.at[self.lastidx,'volume']=self.tmpcontract=self.tmpcontract+nQty
            self.drawMA=False

        if self.drawMA :
            self.Candledf['high_avg'] = self.Candledf.high.rolling(self.MA).mean().round(0)
            self.Candledf['low_avg'] = self.Candledf.low.rolling(self.MA).mean().round(0)
        self.CheckHour=tmphour

    def run(self):
        while True:
            nlist = self.__Queue.get()
            if nlist != None:
                self.HisDone = nlist[0]
                if self.HisDone:
                    self.tickto12k(nlist[1])
                    if self.__CandleTarget.value == self.name:
                        self.__Candledf12K.list12K = [self.lastidx,self.Close]
                        self.__Candledf12K.df12K = self.Candledf
                        self.__CandleItem12K_Event.put(nlist[2])
                else:
                    self.HisListProcess(nlist[1])
                    if self.__CandleTarget.value == self.name:
                        self.__Candledf12K.df12K = self.Candledf
                        self.__CandleItem12K_Event.put(nlist[2])

class TicksToMinuteK(QThread):
    def __init__(self,inputname,inputindex,inputTuple):
        super(TicksToMinuteK, self).__init__()
        self.name = inputname
        self.commodityIndex = inputindex
        self.__Queue = inputTuple[0]
        self.__CandleTarget = inputTuple[1]
        self.__CandleItemMinK_Event = inputTuple[2]
        self.__CandleMinuteDealMinus_Event = inputTuple[3]
        self.__CandledfMinK = inputTuple[4]
        self.Candledf = None
        self.HisDone = False
        self.mm=0
        self.mm1=0
        self.lastidx=0
        self.High=0
        self.Low=0
        self.Close=0
        self.interval=1

    def HisListProcess(self,nlist):
        dayticks = pd.DataFrame(nlist,columns=['ndatetime','nbid','nask','close','volume','deal'])
        # dayticks.drop(['deal'], axis=1, inplace=True)
        dayticks['ndatetime']=pd.to_datetime(dayticks['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
        now = time.localtime(time.time()).tm_hour
        if now>14 or now<8 :
            dayticks=dayticks[(dayticks.ndatetime.dt.hour>14) | (dayticks.ndatetime.dt.hour<8)] # 夜盤
        elif now>=8 and now<15:
            dayticks=dayticks[(dayticks.ndatetime.dt.hour>=8) & (dayticks.ndatetime.dt.hour<15)] # 日盤
        dayticks.sort_values(by=['ndatetime'],ascending=True)
        dayticks.index = dayticks.ndatetime
        self.Candledf=dayticks['close'].resample('1min',closed='right').ohlc()
        tmpdf=dayticks['volume'].resample('1min').sum()
        self.Candledf=pd.concat([self.Candledf,tmpdf],axis=1)
        del tmpdf
        tmpdf=dayticks['deal'].resample('1min').sum()
        self.Candledf=pd.concat([self.Candledf,tmpdf],axis=1)
        self.Candledf['dealminus'] = self.Candledf['deal'].cumsum()
        del self.Candledf['deal']
        del tmpdf
        del dayticks
        self.Candledf=self.Candledf.dropna()
        self.Candledf=self.Candledf.rename_axis('ndatetime').reset_index()
        self.Candledf['ndatetime'] = pd.to_datetime(self.Candledf['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
        self.lastidx=self.Candledf.last_valid_index()
        self.mm=self.Candledf.at[self.lastidx,'ndatetime'].replace(second=0,microsecond=0)
        self.mm1=self.mm+datetime.timedelta(minutes=self.interval)
        self.High=self.Candledf.at[self.lastidx,'high']
        self.Low=self.Candledf.at[self.lastidx,'low']
        self.Close=self.Candledf.at[self.lastidx,'close']

    def TicksToMinuteK(self,nlist):
        ndatetime = nlist[0]; nclose = nlist[1]; nQty = nlist[2] ; ndeal = nlist[3]
        if self.mm1==0 or ndatetime>=self.mm1:
            self.mm=ndatetime.replace(second=0,microsecond=0)
            self.mm1=self.mm+datetime.timedelta(minutes=self.interval)
            tmpdeal=self.Candledf.at[self.lastidx,'dealminus']+ndeal
            self.Candledf=self.Candledf.append(pd.DataFrame([[self.mm,nclose,nclose,nclose,nclose,nQty,tmpdeal]],columns=['ndatetime','open','high','low','close','volume','dealminus']),ignore_index=True,sort=False)
            self.High = self.Low = self.Close = nclose
            self.lastidx=self.Candledf.last_valid_index()
        elif ndatetime < self.mm1 :
            self.Candledf.at[self.lastidx,'close']=self.Close=nclose
            self.Candledf.at[self.lastidx,'volume']+=nQty
            self.Candledf.at[self.lastidx,'dealminus']+=ndeal
            if self.High < nclose or self.Low > nclose:
                self.Candledf.at[self.lastidx,'high']=self.High=max(self.High,nclose)
                self.Candledf.at[self.lastidx,'low']=self.Low=min(self.Low,nclose)
        else:
            print('有錯誤:',self.mm,',',self.mm1,',',self.lastidx,ndatetime)
        # print(self.lastidx,ndatetime,nclose,self.Low)
    
    def run(self):
        while True:
            nlist = self.__Queue.get()
            if nlist != None:
                self.HisDone = nlist[0]
                if self.HisDone:
                    self.TicksToMinuteK(nlist[1])
                    if self.__CandleTarget.value == self.name:
                        self.__CandledfMinK.listMinK = [self.lastidx,self.Close]
                        self.__CandledfMinK.listMinDealMinus = [self.lastidx,self.Candledf.at[self.lastidx,'dealminus']]
                        self.__CandledfMinK.dfMinK = self.Candledf
                        self.__CandleItemMinK_Event.put(nlist[2])
                        self.__CandleMinuteDealMinus_Event.put(nlist[2])
                else:
                    self.HisListProcess(nlist[1])
                    if self.__CandleTarget.value == self.name:
                        self.__CandledfMinK.dfMinK = self.Candledf
                        self.__CandleItemMinK_Event.put(nlist[2])
