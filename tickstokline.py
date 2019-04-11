#匯入所需module
import datetime
import time
import numpy as np
import pandas as pd
import pyqtgraph as pg
from pyqtgraph import QtCore, QtGui
# from mpl_finance import candlestick2_ohlc
# import matplotlib.dates as mdates
# import matplotlib.pyplot as plt

class dataprocess:
    def __init__(self,ntype,inputname):
        self.name=inputname
        self.type=ntype
        # self.contractkpd=pd.DataFrame(columns=['ndatetime','open','high','low','close','volume'])
        self.ticksdf=pd.DataFrame(columns=['ndate','ntime','nbid','nask','close','volume'])
        self.ticksdf['ndate']=pd.to_datetime(self.ticksdf['ndate'],format='%Y-%m-%d')
        self.ticksdf['ntime']=pd.to_datetime(self.ticksdf['ntime'],format='%H:%M:%S.%f')
        self.contractkpd=pd.read_csv('result.csv')
        self.contractkpd['ndatetime']=pd.to_datetime(self.contractkpd['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
        self.contractkpd.sort_values(by=['ndatetime'],ascending=True)
        self.newlist=[]
        self.tmpcontract=0
        self.CheckHour=0
        # ----matplotlib
        # plt.ion()
        # self.fig=plt.figure()
        # self.ax=self.fig.add_subplot(1,1,1)
        # self.ax.set_autoscaley_on(True)
        # self.fig.canvas.draw()
        # self.fig.show()    

    # mpl_finacial 
    # def drawbar(self,ndatetime,nopen,nhigh,nlow,nclose):
    #     start=time.time()
    #     self.ax.cla()    
    #     candlestick2_ohlc(
    #         self.ax,
    #         nopen,
    #         nhigh,
    #         nlow,
    #         nclose,
    #         width=0.6,colorup='r',colordown='g',alpha=1
    #     )
    #     self.ax.autoscale_view()
    #     self.fig.canvas.flush_events()    
    #     end=time.time()
    #     ep=round((end-start),6)
    #     print('繪圖時間: ',ep)

    def Ticks(self,nDate,nTimehms,nTimemillismicros,nBid,nAsk,nClose,nQty):
        nTime=str(nTimehms)
        while len(nTime)<6:
            nTime='0'+nTime
        nTimemicro=str(nTimemillismicros)
        while len(nTimemicro)<6:
            nTimemicro='0'+nTimemicro
        # nTime=datetime.datetime.strptime(nTime,'%H%M%S').strftime('%H:%M:%S')+"."+nTimemicro.strip()
        ndatetime=datetime.datetime.strptime(str(nDate)+" "+nTime,'%Y%m%d %H%M%S').strftime('%Y/%m/%d %H:%M:%S')+"."+nTimemicro.strip()
        ndate=datetime.datetime.strptime(str(nDate),'%Y%m%d').date()
        ntime=datetime.datetime.strptime(nTime+"."+nTimemicro.strip(),'%H%M%S.%f').time()
        self.newlist=[ndate,ntime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty)]
        tmplist=[[ndate,ntime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty)]]
        self.ticksdf=self.ticksdf.append(pd.DataFrame(tmplist,columns=['ndate','ntime','nbid','nask','close','volume']),ignore_index=True)
        self.contractk(ndatetime,self.newlist[2],self.newlist[3],self.newlist[4],self.newlist[5])
        return self.newlist
    
    def contractk(self,xdatetime,nBid,nAsk,nClose,nQty):
        ndatetime=datetime.datetime.strptime(xdatetime,'%Y/%m/%d %H:%M:%S.%f')
        tmphour=ndatetime.hour
        if self.contractkpd.shape[0]==0 or self.tmpcontract==0 or self.tmpcontract==12000 or (tmphour==8 and self.CheckHour==4) or (tmphour==15 and self.CheckHour==13):
            self.contractkpd.loc[ndatetime]=[ndatetime,nClose,nClose,nClose,nClose,nQty]
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
    
class CandlestickItem(pg.GraphicsObject):
    def __init__(self):
        pg.GraphicsObject.__init__(self)
        self.lastbar = None
        # self.picture = QtGui.QPicture()
        self.picturemain = QtGui.QPicture() #主K線圖
        self.picturelast = QtGui.QPicture() #最後一根K線圖
        self.pictures=[]
        self.setFlag(self.ItemUsesExtendedStyleOption)
        self.rect = None
        self.low=0
        self.high=0
        self.timelist=[]

    def set_data(self,data):
        start=time.time()
        self.data = data.tail(120).reset_index(drop=True)
        self.low,self.high = (self.data['low'].min(),self.data['high'].max()) if len(data)>0 else (0,1)
        self.generatePicture()
        self.informViewBoundsChanged()
        # if not self.scene() is None:
        #     self.scene().update() #強制圖形更新
        end=time.time()
        if len(self.timelist)<100:
            self.timelist.append((end-start))
        else:
            self.timelist.pop(0)
            self.timelist.append((end-start))
        if sum(self.timelist)!=0 and len(self.timelist)>0:
            ep=int(1/(sum(self.timelist)/len(self.timelist)))
        else:
            ep=0
        print('每100張FPS: ',ep)
    
    def generatePicture(self):    
        # 重畫或者最後一根K線
        if int(len(self.pictures))>1:
            self.pictures.pop()
        w = 1.0 / 3.0
        start = len(self.pictures)
        stop = self.data.shape[0]
        for (t, x) in self.data.loc[start:stop, ['open', 'high', 'low', 'close']].iterrows():
            picture = QtGui.QPicture()
            p = QtGui.QPainter(picture)
            p.setPen(pg.mkPen('w'))
            p.drawLine(QtCore.QPointF(t, x.low), QtCore.QPointF(t, x.high))
            if x.open>x.close:
                p.setBrush(pg.mkBrush('g'))
            elif x.open<x.close:
                p.setBrush(pg.mkBrush('r'))
            else:
                p.setBrush(pg.mkBrush('w'))
            p.drawRect(QtCore.QRectF(t-w, x.open, w*2, x.close-x.open))
            p.end()
            self.pictures.append(picture)
        
    def paint(self, painter, opt, w):
        rect = opt.exposedRect
        xmin,xmax = (max(0,int(rect.left())),min(int(len(self.pictures)),int(rect.right())))
        # self.rect = (rect.left(),rect.right())
        # self.picture = self.createPic(xmin,xmax)
        # self.picture.play(painter)
        if not self.rect == (rect.left(),rect.right()) or self.picturemain is None or self.lastbar != self.data.iloc[-1,0]:
            self.rect = (rect.left(),rect.right())
            self.lastbar = self.data.iloc[-1,0]
            # print('rect: ',self.rect)
            self.picturemain = self.createPic(xmin,xmax-1)
            self.picturemain.play(painter)
            self.picturelast = self.createPic(xmax-1,xmax)
            self.picturelast.play(painter)
            print('重繪')            
        elif not self.picturemain is None:
            self.picturemain.play(painter)
            self.picturelast = self.createPic(xmax-1,xmax)
            self.picturelast.play(painter)
            # print('快圖')

    # 缓存图片
    #----------------------------------------------------------------------
    def createPic(self,xmin,xmax):
        picture = QtGui.QPicture()
        p = QtGui.QPainter(picture)
        [pic.play(p) for pic in self.pictures[xmin:xmax]]
        p.end()
        return picture
    
    def boundingRect(self):
        return QtCore.QRectF(0,self.low,len(self.pictures),(self.high-self.low)) 








        
