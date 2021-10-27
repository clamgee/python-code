#匯入所需module
import datetime
import time,os
import numpy as np
import pandas as pd
import multiprocessing as mp
from PySide6.QtCore import QThread,QTime,Qt


class DataToTicks(QThread):
    def __init__(self,inputname,inputindex,inputTuple):
        super(DataToTicks, self).__init__()
        self.name=inputname
        self.commodityIndex = inputindex
        self.__queue = inputTuple[0]
        self.__connect12K_queue = inputTuple[1]
        self.__connectMinuteK_queue = inputTuple[2]
        self.__PowerQueue = inputTuple[3]
        self.__NS = inputTuple[4]
        self.__SaveNotify = inputTuple[5]
        self.TickList = []
        self.FTlist = []
        self.ListTransform = False
        self.LastTick = 0
        self.hisbol = True #是否為歷史Data
        self.__FileSave = True
        self.__bid = 0
        self.__ask = 0
        self.__checkhour = None

    def Ticks(self,nlist):
        # [int(nPtr),str(lDate),str(lTimehms),str(lTimemillismicros),int(nBid),int(nAsk),int(nclose),int(nQty),nhis]
        nPtr=nlist[0]; nDate=str(nlist[1]); nTime=str(nlist[2]).zfill(6); nTimemicro = nlist[3].zfill(6)
        nBid=nlist[4]; nAsk=nlist[5]; nclose=nlist[6]; nQty=nlist[7]; self.hisbol=nlist[8]; deal=0
        ndatetime=datetime.datetime.strptime(nDate+" "+nTime+"."+nTimemicro,'%Y%m%d %H%M%S.%f')
        tmptime = ndatetime.hour
        if self.LastTick < nPtr:
            self.LastTick = nPtr
            if abs(nclose-nBid) >= abs(nclose-nAsk) :
                deal = nQty
                self.__bid += nQty
            else:
                deal = 0 - nQty
                self.__ask -= nQty
            if tmptime == 8 and self.__checkhour == 4 :
                self.__ask = self.__bid = 0
            self.__checkhour = tmptime 
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
                    self.__PowerQueue.put([self.__bid,self.__ask])
                else:
                    self.TickList.append([ndatetime,int(nBid/100),int(nAsk/100),int(nclose/100),int(nQty),int(deal)])
                    self.__connect12K_queue.put([self.ListTransform,[ndatetime,int(nclose/100),int(nQty)],nPtr])
                    self.__connectMinuteK_queue.put([self.ListTransform,[ndatetime,int(nclose/100),int(nQty),int(deal)],nPtr])
                    self.__PowerQueue.put([self.__bid,self.__ask])
                if self.__NS.listFT[0] == self.name:
                    self.FTlist.append([ndatetime]+self.__NS.listFT[1:])
        else:
            print('捨棄Tick序號: ',nPtr)

    def run(self):
        while True:
            nlist = self.__queue.get()
            if nlist is not None :
                self.Ticks(nlist)
            
            if self.__SaveNotify.value and self.__FileSave:
                ticksdf = pd.DataFrame(columns=['ndatetime','nbid','nask','close','volume','deal'])
                ticksdf =ticksdf.append(pd.DataFrame(self.TickList,columns=['ndatetime','nbid','nask','close','volume','deal']),ignore_index=True,sort=False)
                ticksdf['ndatetime']=pd.to_datetime(ticksdf['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
                filename = 'Ticks' + ticksdf.iloc[-1, 0].date().strftime('%Y-%m-%d') + '.txt'
                ticksdf.to_csv('../data/'+filename, header=False, index=False)
                df1=pd.read_csv('../filename.txt')
                df1=df1.append(pd.DataFrame([[filename]],columns=['filename']),ignore_index=True)
                df1.to_csv('../filename.txt',index=False)
                del df1
                del ticksdf
                now = time.localtime()
                localtime = QTime(now.tm_hour, now.tm_min, now.tm_sec).toString(Qt.ISODate)
                print(localtime,' Ticks已存檔!!')
                self.__FileSave = False

class TicksTo12K(QThread):
    def __init__(self,inputname,inputindex,inputTuple):
        super(TicksTo12K, self).__init__()
        self.name = inputname
        self.commodityIndex = inputindex
        self.__Queue = inputTuple[0]
        self.__CandleTarget = inputTuple[1]
        self.__CandleItem12K_Event = inputTuple[2]
        self.__Candledf12K = inputTuple[3]
        self.__SaveNotify = inputTuple[4]
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
        self.__FileSave = True

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
                        self.__CandleItem12K_Event.set()
                else:
                    self.HisListProcess(nlist[1])
                    if self.__CandleTarget.value == self.name:
                        self.__Candledf12K.df12K = self.Candledf
                        if self.__CandleItem12K_Event.is_set() is False:
                            self.__CandleItem12K_Event.set()

            if self.__SaveNotify.value and self.__FileSave:
                result=self.Candledf.drop(columns=['high_avg','low_avg'])            
                result.sort_values(by=['ndatetime'],ascending=True)
                result.to_csv('../result.dat',header=True, index=False,mode='w')
                now = time.localtime()
                localtime = QTime(now.tm_hour, now.tm_min, now.tm_sec).toString(Qt.ISODate)
                print(localtime,' 12K已存檔!!')
                self.__FileSave = False

class TicksToMinuteK(QThread):
    def __init__(self,inputname,inputindex,inputTuple):
        super(TicksToMinuteK, self).__init__()
        self.name = inputname
        self.commodityIndex = inputindex
        self.__Queue = inputTuple[0]
        self.__CandleTarget = inputTuple[1]
        self.__CandleItemMinK_Event = inputTuple[2]
        self.__CandleMinuteDealMinus_Event = inputTuple[3]
        self.__CandleMinuteBig_Event = inputTuple[4]
        self.__CandleMinuteSmall_Event = inputTuple[5]
        self.__NS = inputTuple[6]
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
        try:
            self.mm=self.Candledf.at[self.lastidx,'ndatetime'].replace(second=0,microsecond=0)
            self.mm1=self.mm+datetime.timedelta(minutes=self.interval)
        except Exception:
            pass
        self.High=self.Candledf.at[self.lastidx,'high']
        self.Low=self.Candledf.at[self.lastidx,'low']
        self.Close=self.Candledf.at[self.lastidx,'close']
        self.Candledf['big']=int(self.__NS.listFT[2]-self.__NS.listFT[1])
        self.Candledf['small']=int(self.__NS.listFT[3]-self.__NS.listFT[4])
        self.Candledf[['open','high','low','close','volume','dealminus','big','small']]= self.Candledf[['open','high','low','close','volume','dealminus','big','small']].astype(int)

    def TicksToMinuteK(self,nlist):
        ndatetime = nlist[0]; nclose = nlist[1]; nQty = nlist[2] ; ndeal = nlist[3]
        small=int(self.__NS.listFT[3]-self.__NS.listFT[4]); big=int(self.__NS.listFT[2]-self.__NS.listFT[1])
        if self.mm1==0 or ndatetime>=self.mm1:
            self.mm=ndatetime.replace(second=0,microsecond=0)
            self.mm1=self.mm+datetime.timedelta(minutes=self.interval)
            tmpdeal=self.Candledf.at[self.lastidx,'dealminus']+ndeal
            self.Candledf=self.Candledf.append(pd.DataFrame([[self.mm,nclose,nclose,nclose,nclose,nQty,tmpdeal,big,small]],columns=['ndatetime','open','high','low','close','volume','dealminus','big','small']),ignore_index=True,sort=False)
            self.High = self.Low = self.Close = nclose
            self.lastidx=self.Candledf.last_valid_index()
        elif ndatetime < self.mm1 :
            self.Candledf.at[self.lastidx,'close']=self.Close=nclose
            self.Candledf.at[self.lastidx,'volume']+=nQty
            self.Candledf.at[self.lastidx,'dealminus']+=ndeal
            self.Candledf.at[self.lastidx,'big']=big
            self.Candledf.at[self.lastidx,'small']=small
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
                        self.__NS.listMinK = [self.lastidx,self.Close]
                        self.__NS.listMinDealMinus = [self.lastidx,self.Candledf.at[self.lastidx,'dealminus']]
                        self.__NS.listMinBig = [self.lastidx,self.Candledf.at[self.lastidx,'big']]
                        self.__NS.listMinSmall = [self.lastidx,self.Candledf.at[self.lastidx,'small']]
                        self.__NS.dfMinK = self.Candledf                       
                        if self.__CandleItemMinK_Event.is_set() is False: 
                            self.__CandleItemMinK_Event.set()
                        if self.__CandleMinuteDealMinus_Event.is_set() is False:
                            self.__CandleMinuteDealMinus_Event.set()
                        if self.__CandleMinuteBig_Event.is_set() is False:
                            self.__CandleMinuteBig_Event.set()
                        if self.__CandleMinuteSmall_Event.is_set() is False:
                            self.__CandleMinuteSmall_Event.set()
                else:
                    self.HisListProcess(nlist[1])
                    if self.__CandleTarget.value == self.name:
                        self.__NS.dfMinK = self.Candledf
                        self.__CandleItemMinK_Event.set()
