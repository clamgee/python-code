#匯入所需module
import datetime
import time
import numpy as np
import pandas as pd
import os
import multiprocessing as mp
from PySide6.QtCore import QObject, QThread,Signal,Slot
import pyqtgraph as pg
import KlineItem

class DataToTicks(QThread):
    def __init__(self,inputname,inputindex,Passlist):
        super(DataToTicks, self).__init__()
        self.name=inputname
        self.commodityIndex = inputindex
        self.__queue = Passlist[0].queue
        print('Tick內的Queue: ',self.__queue)
        self.__connect12K_List = Passlist[1]
        self.__connect12K_queue = Passlist[2]
        self.__connectMinuteK_List = Passlist[3]
        self.__connectMinuteK_queue = Passlist[4]
        self.TickList = []
        self.ListTransform = False
        self.LastTick = 0
        self.LastTickClose = 0
        self.hisbol = True #是否為歷史Data

    def Ticks(self,nlist):
        # [int(nPtr),str(lDate),str(lTimehms),str(lTimemillismicros),int(nBid),int(nAsk),int(nClose),int(nQty),nhis]
        nPtr=nlist[0]; nDate=str(nlist[1]); nTime=str(nlist[2]).zfill(6); nTimemicro = nlist[3].zfill(6)
        nBid=nlist[4]; nAsk=nlist[5]; nClose=nlist[6]; nQty=nlist[7]; self.hisbol=nlist[8]; deal=0
        ndatetime=datetime.datetime.strptime(nDate+" "+nTime+"."+nTimemicro,'%Y%m%d %H%M%S.%f')
        if self.LastTick < nPtr:
            self.LastTick = nPtr
            if self.LastTickClose != 0:
                if(nClose > self.LastTickClose) or (nClose >= nAsk):
                    deal = nQty
                elif (nClose < self.LastTickClose) or (nClose <= nBid):
                    deal = 0-nQty
                else:
                    try:
                        deal = 0
                    except Exception as e:
                        print(nPtr,self.LastTickClose,'Ticks 處理力道錯誤: ',nlist,'系統資訊: ',e)
            else:
                if nClose >=nAsk:
                    deal = nQty
                else:
                    deal = 0 - nQty
            self.LastTickClose = nClose
            # True:下載歷史資料至list, 2: 處理歷史list 3: 即時
            if self.hisbol:
                self.TickList.append([ndatetime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty),int(deal)])
            else:
                if self.ListTransform == False:
                    self.__connect12K_List.emit(self.TickList)
                    self.__connectMinuteK_List.emit(self.TickList)
                    print('transform List',len(self.TickList))
                    self.ListTransform = True
                    self.TickList.append([ndatetime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty),int(deal)])
                    self.__connect12K_queue.emit([ndatetime,int(nClose/100),int(nQty)])
                    self.__connectMinuteK_queue.emit([ndatetime,int(nClose/100),int(nQty)])
                    self.TickList.append([ndatetime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty),int(deal)])
                else:
                    self.TickList.append([ndatetime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty),int(deal)])
                    self.__connect12K_queue.emit([ndatetime,int(nClose/100),int(nQty)])
                    self.__connectMinuteK_queue.emit([ndatetime,int(nClose/100),int(nQty)])
        else:
            print('捨棄Tick序號: ',nPtr)
            pass

    def run(self):
        while True:
            nlist = self.__queue.get()
            self.Ticks(nlist)

class TicksTo12K(QThread):
    def __init__(self,inputname,inputindex,inputTuple):
        super(TicksTo12K, self).__init__()
        self.name = inputname
        self.commodityIndex = inputindex
        self.__Queue = inputTuple[0].queue
        self.__list = inputTuple[0].listqueue
        self.__Candle12K_Signal = inputTuple[1]
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
        self.CheckHour = None
        self.HisDone = False
        self.Candle12KPlotItem = KlineItem.CandleItem(self)        

    @Slot(list)
    def HisListProcess(self,nlist):
        for row in nlist:
            tmphour=row[0].hour
            if (tmphour==8 and self.CheckHour==4) or (tmphour==15 and (self.CheckHour is None or self.CheckHour==13)):
                self.Candledf=self.Candledf.append(pd.DataFrame([[row[0],row[3],row[3],row[3],row[3],row[4],0,0]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg']),ignore_index=True,sort=False)
                self.High=self.Low=row[3]
                self.tmpcontract=row[4]
                self.ticksum=row[4]
                self.lastidx = self.Candledf.last_valid_index()
            elif self.tmpcontract==0 or self.tmpcontract==12000 :
                self.Candledf=self.Candledf.append(pd.DataFrame([[row[0],row[3],row[3],row[3],row[3],row[4],0,0]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg']),ignore_index=True,sort=False)
                self.High=self.Low=row[3]
                self.tmpcontract=row[4]
                self.ticksum+=row[4]
                self.lastidx = self.Candledf.last_valid_index()
            elif (self.tmpcontract+row[4])>12000:
                if row[3] > self.High or row[3] < self.Low :
                    self.Candledf.at[self.lastidx,'high']=self.High=max(self.Candledf.at[self.lastidx,'high'],row[3])
                    self.Candledf.at[self.lastidx,'low']=self.Low=min(self.Candledf.at[self.lastidx,'low'],row[3])
                self.Candledf.at[self.lastidx,'close']=row[3]
                self.Candledf.at[self.lastidx,'volume']=12000
                self.ticksum+=row[4]
                self.tmpcontract=self.tmpcontract+row[4]-12000
                self.Candledf=self.Candledf.append(pd.DataFrame([[row[0],row[3],row[3],row[3],row[3],self.tmpcontract,0,0]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg']),ignore_index=True,sort=False)
                self.High=self.Low=row[3]
                self.lastidx = self.Candledf.last_valid_index()
            else:
                if row[3] > self.High or row[3] < self.Low:
                    self.Candledf.at[self.lastidx,'high']=self.High=max(self.Candledf.at[self.lastidx,'high'],row[3])
                    self.Candledf.at[self.lastidx,'low']=self.Low=min(self.Candledf.at[self.lastidx,'low'],row[3])
                self.Candledf.at[self.lastidx,'close']=row[3]
                self.ticksum+=row[4]
                self.Candledf.at[self.lastidx,'volume']=self.tmpcontract=self.tmpcontract+row[4]
            self.CheckHour=tmphour
        self.Candledf['high_avg'] = self.Candledf.high.rolling(self.MA).mean()
        self.Candledf['low_avg'] = self.Candledf.low.rolling(self.MA).mean()
        self.HisDone = True
        # print(self.Candledf.tail(5))
        self.Candle12KPlotItem.set_data()

    def tickto12k(self,nlist):
        ndatetime = nlist[0]; nClose = nlist[1]; nQty = nlist[2]
        tmphour=ndatetime.hour
        if (tmphour==8 and self.CheckHour==4) or (tmphour==15 and (self.CheckHour is None or self.CheckHour==13)):
            self.Candledf=self.Candledf.append(pd.DataFrame([[ndatetime,nClose,nClose,nClose,nClose,nQty,0,0]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg']),ignore_index=True,sort=False)
            self.High=self.Low=nClose
            self.tmpcontract=nQty
            self.ticksum=nQty
            self.drawMA=True
            self.lastidx = self.Candledf.last_valid_index()        
        elif self.tmpcontract==0 or self.tmpcontract==12000 :
            self.Candledf=self.Candledf.append(pd.DataFrame([[ndatetime,nClose,nClose,nClose,nClose,nQty,0,0]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg']),ignore_index=True,sort=False)
            self.High=self.Low=nClose
            self.ticksum+=nQty
            self.tmpcontract=nQty
            self.drawMA=True
            self.lastidx = self.Candledf.last_valid_index()
        elif (self.tmpcontract+nQty)>12000:
            if nClose > self.High or nClose < self.Low :
                self.Candledf.at[self.lastidx,'high']=self.High=max(self.Candledf.at[self.lastidx,'high'],nClose)
                self.Candledf.at[self.lastidx,'low']=self.Low=min(self.Candledf.at[self.lastidx,'low'],nClose)
            self.Candledf.at[self.lastidx,'close']=nClose
            self.Candledf.at[self.lastidx,'volume']=12000
            self.ticksum+=nQty
            self.tmpcontract=self.tmpcontract+nQty-12000
            self.Candledf=self.Candledf.append(pd.DataFrame([[ndatetime,nClose,nClose,nClose,nClose,self.tmpcontract,0,0]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg']),ignore_index=True,sort=False)
            self.lastidx = self.Candledf.last_valid_index()
            self.High=self.Low=nClose
            self.drawMA=True
        else:
            if nClose > self.High or nClose < self.Low:
                self.Candledf.at[self.lastidx,'high']=self.High=max(self.Candledf.at[self.lastidx,'high'],nClose)
                self.Candledf.at[self.lastidx,'low']=self.Low=min(self.Candledf.at[self.lastidx,'low'],nClose)
            self.Candledf.at[self.lastidx,'close']=nClose
            self.ticksum+=nQty
            self.Candledf.at[self.lastidx,'volume']=self.tmpcontract=self.tmpcontract+nQty
            self.drawMA=False

        if self.drawMA :
            self.Candledf['high_avg'] = self.Candledf.high.rolling(self.MA).mean().round(0)
            self.Candledf['low_avg'] = self.Candledf.low.rolling(self.MA).mean().round(0)
        self.CheckHour=tmphour
        self.Candle12KPlotItem.set_data()
        # print(self.Candledf.tail(1))
    
    def run(self):
        while True:
            if self.HisDone:
                nlist = self.__Queue.get()
                self.tickto12k(nlist)
                self.__Candle12K_Signal.emit(self.Candle12KPlotItem)
            else:
                if self.__list.empty() is not True:
                    nlist = self.__list.get()
                    self.HisListProcess(nlist)
                    self.__Candle12K_Signal.emit(self.Candle12KPlotItem)
                else:
                    pass

class TicksToMinuteK(QThread):
    def __init__(self,inputname,inputindex,inputTuple):
        super(TicksToMinuteK, self).__init__()
        self.name = inputname
        self.commodityIndex = inputindex
        self.__Queue = inputTuple[0].queue
        self.__list = inputTuple[0].listqueue
        self.__CandleMinuteK_Signal = inputTuple[1]
        self.Candledf = None
        self.HisDone = False
        self.mm=0
        self.mm1=0
        self.lastidx=0
        self.High=0
        self.Low=0
        self.interval=1

    def HisListProcess(self,nlist):
        dayticks = pd.DataFrame(nlist,columns=['ndatetime','nbid','nask','close','volume','deal'])
        dayticks.drop(['deal'], axis=1, inplace=True)
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
        self.Candledf=self.Candledf.dropna()
        self.Candledf=self.Candledf.rename_axis('ndatetime').reset_index()
        self.Candledf['ndatetime'] = pd.to_datetime(self.Candledf['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
        self.Minutelastidx=self.Candledf.last_valid_index()
        if self.Minutelastidx!=0:
            self.mm=self.Candledf.at[self.Minutelastidx,'ndatetime'].replace(second=0,microsecond=0)
            self.mm1=self.mm+datetime.timedelta(minutes=self.interval)
            self.High=self.Candledf.at[self.Minutelastidx,'high']
            self.Low=self.Candledf.at[self.Minutelastidx,'low']
        self.HisDone = True
        self.CandleMinuteKPlotItem = KlineItem.CandleItem(self)
        print(self.Candledf.tail(5))

    def TicksToMinuteK(self,nlist):
        ndatetime = nlist[0]; nClose = nlist[1]; nQty = nlist[2]
        if self.lastidx==0 or ndatetime>=self.mm1:
            self.mm=ndatetime.replace(second=0,microsecond=0)
            self.mm1=self.mm+datetime.timedelta(minutes=self.interval)
            # print(self.Candledf.tail(1))
            self.Candledf=self.Candledf.append(pd.DataFrame([[self.mm,nClose,nClose,nClose,nClose,nQty]],columns=['ndatetime','open','high','low','close','volume']),ignore_index=True,sort=False)
            self.High = self.Low = nClose
            self.lastidx=self.Candledf.last_valid_index()
        elif ndatetime < self.mm1 :
            self.Candledf.at[self.lastidx,'close']=nClose
            self.Candledf.at[self.lastidx,'volume']+=nQty
            if self.High < nClose or self.Low > nClose:
                self.Candledf.at[self.lastidx,'high']=self.High=max(self.High,nClose)
                self.Candledf.at[self.lastidx,'low']=self.Low=min(self.Low,nClose)
        else:
            print('有錯誤:',self.mm,',',self.mm1,',',self.lastidx,ndatetime)
        # print(self.lastidx,ndatetime,nClose,self.Low)
    
    def run(self):
        while True:
            if self.HisDone:
                nlist = self.__Queue.get()
                self.TicksToMinuteK(nlist)
                self.CandleMinuteKPlotItem.set_data()
                self.__CandleMinuteK_Signal.emit(self.CandleMinuteKPlotItem)
            else:
                if self.__list.empty() is not True:
                    nlist = self.__list.get()
                    self.HisListProcess(nlist)
                    # self.CandleMinuteKPlotItem.set_data()
                    self.__CandleMinuteK_Signal.emit(self.CandleMinuteKPlotItem)
                else:
                    pass

