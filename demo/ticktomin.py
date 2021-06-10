import pandas as pd
import numpy as np
import os
import sys
import time
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem, QFrame
from PyQt5.QtCore import QRectF
# from PyQt5.QtGui import QGraphicsLayout
from PyQt5.uic import loadUi
from pyqtgraph import QtCore,QtGui
import pyqtgraph as pg

direct=os.path.abspath('../data')
file = os.listdir('../data')
print(direct+'\\'+file[-1])
dayticks = pd.read_csv(direct+'\\'+file[-1],header=None,names=['ndatetime','nbid','nask','close','volume'])
dayticks['ndatetime']=pd.to_datetime(dayticks['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
dayticks.sort_values(by=['ndatetime'],ascending=True)
dayticks.index = dayticks.ndatetime
mindf=dayticks.resample('60s', how={'close': 'ohlc'})
mindf=mindf.rename_axis('ndatetime').reset_index()
mindf.columns = ['ndatetime','open','high','low','close']
mindf['ndatetime'] = pd.to_datetime(mindf['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
# mindf[['open','high','low','close']]= mindf[['open','high','low','close']].fillna(0.0).astype(int)

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
        elif nidx > self.lastidx and self.lastidx!=0:
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
        stop = self.lastidx + 1

        for (t, x) in self.data.loc[start:stop, ['open', 'high', 'low', 'close', 'high_avg', 'low_avg']].iterrows():
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

            if self.lowavg != '' and (stop-start)>1:
                p.setPen(pg.mkPen('w'))
                p.setBrush(pg.mkBrush('w'))
                p.drawLine(QtCore.QPointF(t - 1, self.lowavg), QtCore.QPointF(t, x.low_avg))
                # p.drawPoint(int(t), int(x.low_avg))

            if t < (self.lastidx+1):
                self.lowavg = x.low_avg
                self.highavg = x.high_avg
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
        self.draw1 = self.l.addPlot()
        self.draw1.addItem(self.kitem)
        data = mindf.loc[1065:1365,['ndatetime','open','high','low','close']]
        data = data.reset_index(drop=True)
        print(data)
        self.kitem.set_data(data.last_valid_index(),data.high.max(),data.low.min(),data)
        # self.draw1 = self.l.addPlot(axisItems={'bottom': self.MyAxis},y=data)
        self.draw1.setTitle('test')
        self.draw1.showAxis('left',show=False)
        self.draw1.showAxis('top',show=False)
        self.draw1.showAxis('right',show=True)
        # self.draw1.setXRange(7100,7500)
        # self.draw1.setYRange(12000,17000)
        # self.l.nextRow()
        # self.draw3=self.l.addPlot()
        # self.bar = pg.BarGraphItem(x=data2index,height=data2,width=0.3,bush='r')
        # self.draw3.addItem(self.bar)
        # self.l.layout.setRowStretchFactor(0, 3)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    MG = MainWindows()

    MG.show()
    sys.exit(app.exec_())