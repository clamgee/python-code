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
        self.queue = Passlist[0].queue
        print('Tick內的Queue: ',self.queue)
        self.connect12K_List = Passlist[1]
        self.connect12K_queue = Passlist[2]
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
                    self.connect12K_List.emit(self.TickList)
                    print('transform List',len(self.TickList))
                    self.ListTransform = True
                    self.TickList.append([ndatetime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty),int(deal)])
                    self.connect12K_queue.emit([ndatetime,int(nClose/100),int(nQty)])
                    self.TickList.append([ndatetime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty),int(deal)])
                else:
                    self.TickList.append([ndatetime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty),int(deal)])
                    self.connect12K_queue.emit([ndatetime,int(nClose/100),int(nQty)])
        else:
            print('捨棄Tick序號: ',nPtr)
            pass

    def run(self):
        while True:
            nlist = self.queue.get()
            self.Ticks(nlist)

class TicksTo12K(QThread):
    def __init__(self,inputname,inputindex,inputTuple):
        super(TicksTo12K, self).__init__()
        self.name = inputname
        self.commodityIndex = inputindex
        self.__Queue = inputTuple[0].queue
        self.__list = inputTuple[0].listqueue
        self.__Candle12K_Signal = inputTuple[1]
        self.Tick12Kpd=pd.read_csv('../result.dat',low_memory=False)
        self.Tick12Kpd['ndatetime']=pd.to_datetime(self.Tick12Kpd['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
        self.Tick12Kpd.sort_values(by=['ndatetime'],ascending=True)
        self.Tick12Kpd=self.Tick12Kpd.reset_index(drop=True)
        self.Tick12Kpd[['open','high','low','close','volume']]=self.Tick12Kpd[['open','high','low','close','volume']].astype(int)
        self.MA = 87
        self.Tick12Kpd['high_avg'] = self.Tick12Kpd.high.rolling(self.MA).mean().round(0)
        self.Tick12Kpd['low_avg'] = self.Tick12Kpd.low.rolling(self.MA).mean().round(0)
        self.lastidx = self.Tick12Kpd.last_valid_index()
        self.High = self.Tick12Kpd['high'].max()
        self.Low = self.Tick12Kpd['low'].min()
        self.CheckHour = None
        self.HisDone = False
        self.Candle12KPlotItem = KlineItem.CandleItem(self)
        

    @Slot(list)
    def HisListProcess(self,nlist):
        for row in nlist:
            tmphour=row[0].hour
            if (tmphour==8 and self.CheckHour==4) or (tmphour==15 and (self.CheckHour is None or self.CheckHour==13)):
                self.Tick12Kpd=self.Tick12Kpd.append(pd.DataFrame([[row[0],row[3],row[3],row[3],row[3],row[4],0,0]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg']),ignore_index=True,sort=False)
                self.High=self.Low=row[3]
                self.tmpcontract=row[4]
                self.ticksum=row[4]
                self.lastidx = self.Tick12Kpd.last_valid_index()
            elif self.tmpcontract==0 or self.tmpcontract==12000 :
                self.Tick12Kpd=self.Tick12Kpd.append(pd.DataFrame([[row[0],row[3],row[3],row[3],row[3],row[4],0,0]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg']),ignore_index=True,sort=False)
                self.High=self.Low=row[3]
                self.tmpcontract=row[4]
                self.ticksum+=row[4]
                self.lastidx = self.Tick12Kpd.last_valid_index()
            elif (self.tmpcontract+row[4])>12000:
                if row[3] > self.High or row[3] < self.Low :
                    self.Tick12Kpd.at[self.lastidx,'high']=self.High=max(self.Tick12Kpd.at[self.lastidx,'high'],row[3])
                    self.Tick12Kpd.at[self.lastidx,'low']=self.Low=min(self.Tick12Kpd.at[self.lastidx,'low'],row[3])
                self.Tick12Kpd.at[self.lastidx,'close']=row[3]
                self.Tick12Kpd.at[self.lastidx,'volume']=12000
                self.ticksum+=row[4]
                self.tmpcontract=self.tmpcontract+row[4]-12000
                self.Tick12Kpd=self.Tick12Kpd.append(pd.DataFrame([[row[0],row[3],row[3],row[3],row[3],self.tmpcontract,0,0]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg']),ignore_index=True,sort=False)
                self.High=self.Low=row[3]
                self.lastidx = self.Tick12Kpd.last_valid_index()
            else:
                if row[3] > self.High or row[3] < self.Low:
                    self.Tick12Kpd.at[self.lastidx,'high']=self.High=max(self.Tick12Kpd.at[self.lastidx,'high'],row[3])
                    self.Tick12Kpd.at[self.lastidx,'low']=self.Low=min(self.Tick12Kpd.at[self.lastidx,'low'],row[3])
                self.Tick12Kpd.at[self.lastidx,'close']=row[3]
                self.ticksum+=row[4]
                self.Tick12Kpd.at[self.lastidx,'volume']=self.tmpcontract=self.tmpcontract+row[4]
            self.CheckHour=tmphour
        self.Tick12Kpd['high_avg'] = self.Tick12Kpd.high.rolling(self.MA).mean()
        self.Tick12Kpd['low_avg'] = self.Tick12Kpd.low.rolling(self.MA).mean()
        self.HisDone = True
        # print(self.Tick12Kpd.tail(5))
        self.Candle12KPlotItem.set_data()

    def tickto12k(self,nlist):
        ndatetime = nlist[0]; nClose = nlist[1]; nQty = nlist[2]
        tmphour=ndatetime.hour
        if (tmphour==8 and self.CheckHour==4) or (tmphour==15 and (self.CheckHour is None or self.CheckHour==13)):
            self.Tick12Kpd=self.Tick12Kpd.append(pd.DataFrame([[ndatetime,nClose,nClose,nClose,nClose,nQty,0,0]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg']),ignore_index=True,sort=False)
            self.High=self.Low=nClose
            self.tmpcontract=nQty
            self.ticksum=nQty
            self.drawMA=True
            self.lastidx = self.Tick12Kpd.last_valid_index()        
        elif self.tmpcontract==0 or self.tmpcontract==12000 :
            self.Tick12Kpd=self.Tick12Kpd.append(pd.DataFrame([[ndatetime,nClose,nClose,nClose,nClose,nQty,0,0]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg']),ignore_index=True,sort=False)
            self.High=self.Low=nClose
            self.ticksum+=nQty
            self.tmpcontract=nQty
            self.drawMA=True
            self.lastidx = self.Tick12Kpd.last_valid_index()
        elif (self.tmpcontract+nQty)>12000:
            if nClose > self.High or nClose < self.Low :
                self.Tick12Kpd.at[self.lastidx,'high']=self.High=max(self.Tick12Kpd.at[self.lastidx,'high'],nClose)
                self.Tick12Kpd.at[self.lastidx,'low']=self.Low=min(self.Tick12Kpd.at[self.lastidx,'low'],nClose)
            self.Tick12Kpd.at[self.lastidx,'close']=nClose
            self.Tick12Kpd.at[self.lastidx,'volume']=12000
            self.ticksum+=nQty
            self.tmpcontract=self.tmpcontract+nQty-12000
            self.Tick12Kpd=self.Tick12Kpd.append(pd.DataFrame([[ndatetime,nClose,nClose,nClose,nClose,self.tmpcontract,0,0]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg']),ignore_index=True,sort=False)
            self.lastidx = self.Tick12Kpd.last_valid_index()
            self.High=self.Low=nClose
            self.drawMA=True
        else:
            if nClose > self.High or nClose < self.Low:
                self.Tick12Kpd.at[self.lastidx,'high']=self.High=max(self.Tick12Kpd.at[self.lastidx,'high'],nClose)
                self.Tick12Kpd.at[self.lastidx,'low']=self.Low=min(self.Tick12Kpd.at[self.lastidx,'low'],nClose)
            self.Tick12Kpd.at[self.lastidx,'close']=nClose
            self.ticksum+=nQty
            self.Tick12Kpd.at[self.lastidx,'volume']=self.tmpcontract=self.tmpcontract+nQty
            self.drawMA=False

        if self.drawMA :
            self.Tick12Kpd['high_avg'] = self.Tick12Kpd.high.rolling(self.MA).mean().round(0)
            self.Tick12Kpd['low_avg'] = self.Tick12Kpd.low.rolling(self.MA).mean().round(0)
        self.CheckHour=tmphour
        self.Candle12KPlotItem.set_data()
        # print(self.Tick12Kpd.tail(1))

    
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


