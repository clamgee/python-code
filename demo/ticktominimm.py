import numpy as np
import pandas as pd
import os
import sys
import datetime
import time
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem, QFrame
from PyQt5.QtCore import QRectF
from PyQt5.uic import loadUi
from pyqtgraph import QtCore,QtGui
import pyqtgraph as pg

direct=os.path.abspath('../data')
file = os.listdir('../data')
print(direct+'\\'+file[-3])
line=[]
with open(direct+'\\'+file[-3]) as file :
    lines = file.read().splitlines()
    for rows in lines:
        row=rows.split(',')
        line.append([row[0],row[1],row[2],row[3],row[4],row[5]])

tick2min=pd.DataFrame(line,columns=['ndatetime','nbid','nask','close','volume','deal'])
tick2min['ndatetime']= pd.to_datetime(tick2min['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
tick2min=tick2min[(tick2min.ndatetime.dt.hour>=8) & (tick2min.ndatetime.dt.hour<15)]
# data=df1min[(df1min.ndatetime.dt.hour<15) & (df1min.ndatetime.dt.hour>=8)]
tick2min=tick2min.sort_values(by=['ndatetime'],ascending=True)
tick2min=tick2min.reset_index(drop=True)
tick2min[['nbid','nask','close','volume','deal']]=tick2min[['nbid','nask','close','volume','deal']].astype(int)

df1min=pd.DataFrame(columns=['ndatetime','open','high','low','close','volume','dealminus'])
df1min['ndatetime']= pd.to_datetime(df1min['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
df1min[['open','high','low','close','volume','dealminus']]=df1min[['open','high','low','close','volume','dealminus']].astype(int)

mm=0
mm1=0
interval=1
high=0
low=0
lastidx=0
start=time.time()
for idx,row in tick2min.iterrows():
    if idx==0 or row.ndatetime>=mm1:
        mm=row.ndatetime.replace(second=0,microsecond=0)
        mm1=mm+datetime.timedelta(minutes=interval)
        if idx ==0 :
            tmpdeal=row[5]
        else:
            tmpdeal=df1min.at[lastidx,'dealminus']+row[5]
        df1min=df1min.append(pd.DataFrame([[mm,row[3],row[3],row[3],row[3],row[4],tmpdeal]],columns=['ndatetime','open','high','low','close','volume','dealminus']),ignore_index=True,sort=False)
        high = low = row[3]
        lastidx=df1min.last_valid_index()
    elif row.ndatetime < mm1 :
        df1min.at[lastidx,'close']=row[3]
        df1min.at[lastidx,'volume']+=row[4]
        df1min.at[lastidx,'dealminus']+=row[5]
        if high < row[3] or low > row[3]:
            df1min.at[lastidx,'high']=high=max(high,row[3])
            df1min.at[lastidx,'low']=low=min(low,row[3])
    else:
        print('有錯誤:',mm,',',mm1,',',idx,row.ndatetime)
print('消耗: ',time.time()-start)
data=df1min.dropna()
data=data.reset_index(drop=True)
print(data.head())
print(data.tail())
print(data.info())

class CandlestickItem(pg.GraphicsObject):
    def __init__(self):
        pg.GraphicsObject.__init__(self)
        self.data = None
        self.lastbar = None
        self.picturemain = QtGui.QPicture() #主K線圖
        self.picturelast = QtGui.QPicture() #最後一根K線圖
        self.pictures = []
        self.setFlag(self.ItemUsesExtendedStyleOption)
        self.rect = None
        self.low = 0
        self.high = 0
        self.highavg = ''
        self.lowavg = ''
        self.lastidx = 0
        self.countK = 60 #設定要顯示多少K線

    def set_data(self,nidx,nhigh,nlow,ndata):
        if self.lastidx == nidx:
            if self.high < nhigh :
                self.data.at[self.lastidx,'high']=self.high=nhigh 
            if self.low > nlow:
                self.data.at[self.lastidx,'low']=self.low=nlow
            self.data.at[self.lastidx,'close'] = ndata.at[self.lastidx,'close']
            self.data.at[self.lastidx,'volume'] = ndata.at[self.lastidx,'volume']
        elif nidx is not None and nidx > self.lastidx and self.lastidx!=0:
            col = ndata.columns.tolist()
            for row in col :
                self.data.at[self.lastidx,row]=ndata.at[self.lastidx,row]
            self.data=self.data.append(ndata.tail(nidx-self.lastidx),ignore_index=True)
            self.lastidx = nidx

        elif self.lastidx==0:
            self.data = ndata.reset_index(drop=True)
            self.high = nhigh
            self.low = nlow
            if self.data.last_valid_index()==nidx:
                self.lastidx = nidx
            else:
                print('繪圖Index資料有誤2')
        else :
            print('繪圖資料有誤!!',nidx)

        # self.len = self.data.shape[0]
        self.generatePicture()
        self.informViewBoundsChanged()
        if not self.scene() is None:
            self.scene().update() #強制圖形更新
    
    def generatePicture(self):    
        # 重畫或者最後一根K線
        if int(len(self.pictures))>1:
            self.pictures.pop()
        w = 1.0 / 3.0
        start = len(self.pictures)
        if self.lastidx is None:
            self.lastidx=0
        stop = self.lastidx + 1

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
            if self.highavg != '' and (stop-start)>1:
                p.setPen(pg.mkPen('b'))
                p.setBrush(pg.mkBrush('b'))
                p.drawLine(QtCore.QPointF(t - 1, self.highavg), QtCore.QPointF(t, x.high_avg))
            # print('圖: ', x.high_avg)
            p.end()
            self.pictures.append(picture)
        
    def paint(self, painter, opt, w):
        rect = opt.exposedRect
        xmin,xmax = (max(0,int(rect.left())),min(int(len(self.pictures)),int(rect.right())))
        if not self.rect == (rect.left(),rect.right()) or self.picturemain is None:# or self.lastbar != self.data.index.values[-1]:
            self.rect = (rect.left(),rect.right())
            self.picturemain = self.createPic(xmin,xmax-1)
            self.picturemain.play(painter)
            self.picturelast = self.createPic(xmax-1,xmax)
            self.picturelast.play(painter)
            # print('重繪')            
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

class MainWindows(QMainWindow):
    def __init__(self):
        super(MainWindows, self).__init__()
        loadUi(r'MG.ui', self)
        self.l = pg.GraphicsLayout()
        self.GV.setCentralItem(self.l)
        # self.MyAxis = pg.AxisItem(orientation='bottom')
        # self.MyAxis.setTicks([dict_tmp.items()])
        # self.draw1(axisItems={'bottom': self.MyAxis})
        self.kitem = CandlestickItem()
        YCline = pg.InfiniteLine(angle=0, movable=False)
        YCline.setPos(17159)
        self.draw1 = self.l.addPlot()
        self.draw1.addItem(self.kitem)
        # data = mindf.loc[1065:1365,['ndatetime','open','high','low','close']].reset_index(drop=True)
        self.draw1.addItem(YCline)
        # data =data.reindex(list(range(0,300)))
        # data = data.reset_index(drop=True)
        
        self.kitem.set_data(data.last_valid_index(),data.high.max(),data.low.min(),data)
        # self.draw1 = self.l.addPlot(axisItems={'bottom': self.MyAxis},y=data)
        self.draw1.setTitle('test')
        self.draw1.showAxis('left',show=False)
        self.draw1.showAxis('top',show=False)
        self.draw1.showAxis('right',show=True)
        self.l.nextRow()
        self.draw2=self.l.addPlot()
        baridx=data.index.tolist()
        bardeal=data.dealminus.tolist()
        self.bar = pg.BarGraphItem(x=baridx,height=bardeal,width=0.3,bush='r')
        self.draw2.addItem(self.bar)
        self.draw2.setXLink(self.draw1)
        self.draw2.showAxis('left',show=False)
        self.draw2.showAxis('top',show=False)
        self.draw2.showAxis('right',show=True)

        # self.draw1.setXRange(7100,7500)
        # self.draw1.setYRange(12000,17000)
        # self.l.nextRow()
        # self.draw3=self.l.addPlot()
        # self.bar = pg.BarGraphItem(x=data2index,height=data2,width=0.3,bush='r')
        # self.draw3.addItem(self.bar)
        self.l.layout.setRowStretchFactor(0, 3)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MG = MainWindows()

    MG.show()
    sys.exit(app.exec_())