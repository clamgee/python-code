#匯入所需module
import datetime
import time
import numpy as np
import pandas as pd
import os
import multiprocessing as mp
from PySide6.QtCore import QObject, QThread,Signal,Slot

class DataToTicks(QThread):
    queue_signal = Signal(list)
    def __init__(self,inputname,inputindex):
        super(DataToTicks, self).__init__()
        self.name=inputname
        self.commodityIndex = inputindex
        self.queue_signal.connect(self.receive_ticks)
        self.Queue = mp.Queue()
        self.TickList = []
        self.ListTransform = False
        self.LastTick = 0
        self.LastTickClose = 0
        self.hisbol = True #是否接受歷史Data
    @Slot(list)
    def receive_ticks(self,nlist):
        self.Queue.put(nlist)
    
    def Ticks(self,nlist):
        nPtr=nlist[0]
        nDate=str(nlist[1])
        nTime=str(nlist[2]).zfill(6)
        nTimemicro = nlist[3].zfill(6)
        nBid=nlist[4]
        nAsk=nlist[5]
        nClose=nlist[6]
        nQty=nlist[7]
        self.hisbol=nlist[8]
        if self.LastTick < nPtr:
            self.LastTick = nPtr
            ndatetime=datetime.datetime.strptime(nDate+" "+nTime+"."+nTimemicro,'%Y%m%d %H%M%S.%f')
            if self.LastTickClose != 0:
                if(nClose > self.LastTickClose) or (nClose >= nAsk):
                    deal = nQty
                elif (nClose < self.LastTickClose) or (nClose <= nBid):
                    deal = 0-nQty
                else:
                    deal = 0
                    print(nPtr,self.LastTickClose,'Ticks 處理力道錯誤: ',nlist)
            else:
                if nClose >=nAsk:
                    deal = nQty
                else:
                    deal = 0 - nQty
            self.LastTickClose = nClose
            # 1:下載歷史資料至list, 2: 處理歷史list 3: 即時
            if self.hisbol==True:
                self.TickList.append([ndatetime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty),int(deal)])
            else:
                if self.ListTransform == False:
                    self.parent12.list_signal.emit(self.TickList)
                    self.TickList.append([ndatetime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty),int(deal)])
                    self.parent12.tick_signal.emit([ndatetime,int(nClose/100),int(nQty),nPtr])
                    self.ListTransform = True
                else:
                    self.parent12.tick_signal.emit(nPtr,ndatetime,int(nClose/100),int(nQty))
        else:
            pass
    
    def run(self):
        while True:
            nlist = self.Queue.get()
            self.Ticks(nlist)

class TicksTo12K(QThread):
    list_signal = Signal(list)
    queue_signal = Signal(list)
    def __init__(self,inputname,inputindex):
        super(TicksTo12K, self).__init__()
        self.name = inputname
        self.commodityIndex = inputindex
        self.LastTick = 0
        self.list_signal.connect(self.HisListProcess)
        self.queue_signal.connect(self.TickQueue)
        self.Tick12Kpd=pd.read_csv('../result.dat',low_memory=False)
        self.Tick12Kpd['ndatetime']=pd.to_datetime(self.Tick12Kpd['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
        self.Tick12Kpd.sort_values(by=['ndatetime'],ascending=True)
        self.Tick12Kpd=self.Tick12Kpd.reset_index(drop=True)
        self.Tick12Kpd[['open','high','low','close','volume']]=self.Tick12Kpd[['open','high','low','close','volume']].astype(int)
        self.MA = 87
        self.Tick12Kpd['high_avg'] = self.Tick12Kpd.high.rolling(self.MA).mean().round(0)
        self.Tick12Kpd['low_avg'] = self.Tick12Kpd.low.rolling(self.MA).mean().round(0)
        self.CheckHour = None

    @Slot(list)
    def HisListProcess(self,nlist):
        for row in nlist:
            tmphour=row[0].hour
            if (tmphour==8 and self.CheckHour==4) or (tmphour==15 and (self.CheckHour is None or self.CheckHour==13)):
                self.Tick12Kpd=self.Tick12Kpd.append(pd.DataFrame([[row[0],row[3],row[3],row[3],row[3],row[4],0,0,0,0,0]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg','dealbid','dealask','dealminus']),ignore_index=True,sort=False)
                self.High=self.Low=row[3]
                self.tmpcontract=row[4]
                self.ticksum=row[4]
                self.lastidx = self.Tick12Kpd.last_valid_index()

            elif self.tmpcontract==0 or self.tmpcontract==12000 :
                self.Tick12Kpd=self.Tick12Kpd.append(pd.DataFrame([[row[0],row[3],row[3],row[3],row[3],row[4],0,0,self.Tick12Kpd.at[self.lastidx,'dealbid'],self.Tick12Kpd.at[self.lastidx,'dealask'],self.Tick12Kpd.at[self.lastidx,'dealminus']]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg','dealbid','dealask','dealminus']),ignore_index=True,sort=False)
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
                self.Tick12Kpd=self.Tick12Kpd.append(pd.DataFrame([[row[0],row[3],row[3],row[3],row[3],self.tmpcontract,0,0,self.Tick12Kpd.at[self.lastidx,'dealbid'],self.Tick12Kpd.at[self.lastidx,'dealask'],self.Tick12Kpd.at[self.lastidx,'dealminus']]],columns=['ndatetime','open','high','low','close','volume','high_avg','low_avg','dealbid','dealask','dealminus']),ignore_index=True,sort=False)
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


    @Slot(list)
    def TickQueue(self,nlist):
