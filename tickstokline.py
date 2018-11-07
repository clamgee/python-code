#匯入所需module
import datetime
import time
import numpy as np
import pandas as pd
from mpl_finance import candlestick2_ohlc
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

class dataprocess:
    def __init__(self,type,name):
        self.name=name
        self.type=type
        self.klinepd=pd.DataFrame(columns=['date','time','open','high','low','close','volume'])
        self.contractkpd=pd.DataFrame(columns=['ndatetime','open','high','low','close','volume'])
        self.newlist=[]
        self.lastlist=[]
        self.tmpcontract=0
        # self.fig, self.aㄌ = plt.subplots()
        # self.ax.set_autoscaley_on(True)
        plt.ion()
        self.fig=plt.figure()
        self.ax=self.fig.add_subplot(1,1,1)
        self.ax.set_autoscaley_on(True)
        # self.fig.show()
        self.fig.canvas.draw()

    def drawbar(self,ndatetime,nopen,nhigh,nlow,nclose):
        start=time.time()
        self.ax.cla()
        candlestick2_ohlc(
            self.ax,
            nopen,
            nhigh,
            nlow,
            nclose,
            width=0.6,colorup='r',colordown='g',alpha=1
        )
        self.ax.autoscale_view()
        self.fig.canvas.flush_events()        
        end=time.time()
        ep=round((end-start),6)
        print('繪圖時間: ',ep)

    def Ticks(self,nDate,nTimehms,nTimemillismicros,nBid,nAsk,nClose,nQty):
        nTime=str(nTimehms)
        while len(nTime)<6:
            nTime='0'+nTime
        nTimemicro=str(nTimemillismicros)
        while len(nTimemicro)<6:
            nTimemicro='0'+nTimemicro
        # nTime=datetime.datetime.strptime(nTime,'%H%M%S').strftime('%H:%M:%S')+"."+nTimemicro.strip()
        ndatetime=datetime.datetime.strptime(str(nDate)+" "+nTime,'%Y%m%d %H%M%S').strftime('%Y/%m/%d %H:%M:%S')+"."+nTimemicro.strip()
        self.newlist=[ndatetime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty)]
        self.contractk(self.newlist[0],self.newlist[1],self.newlist[2],self.newlist[3],self.newlist[4])
        return self.newlist
    
    def contractk(self,xdatetime,nBid,nAsk,nClose,nQty):
        ndatetime=datetime.datetime.strptime(xdatetime,'%Y/%m/%d %H:%M:%S.%f')
        if self.contractkpd.shape[0]==0 or self.tmpcontract==0 or self.tmpcontract==12000:
            self.contractkpd.loc[ndatetime]=[ndatetime,nClose,nClose,nClose,nClose,nQty]
            self.tmpcontract=nQty
        elif (self.tmpcontract+nQty)>12000:
            self.contractkpd.iloc[-1,2]=max(self.contractkpd.iloc[-1,2],nClose)
            self.contractkpd.iloc[-1,3]=min(self.contractkpd.iloc[-1,3],nClose)
            self.contractkpd.iloc[-1,4]=nClose
            self.contractkpd.iloc[-1,5]=12000
            nQty=self.tmpcontract+nQty-12000
            self.tmpcontract=nQty
            self.contractkpd.loc[ndatetime]=[ndatetime,nClose,nClose,nClose,nClose,nQty]
        else:
            self.contractkpd.iloc[-1,2]=max(self.contractkpd.iloc[-1,2],nClose)
            self.contractkpd.iloc[-1,3]=min(self.contractkpd.iloc[-1,3],nClose)
            self.contractkpd.iloc[-1,4]=nClose
            self.tmpcontract+=nQty
            self.contractkpd.iloc[-1,5]=self.tmpcontract
        # self.contractkpd.reset_index(drop=True)
        return self.contractkpd.iloc[-1:].values









        
