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
filelist = os.listdir('../data')
file = filelist[-1]
file2=filelist[-2]
print(direct+'\\'+file)
tmpdf = pd.read_csv(direct+'\\'+file2,header=None,names=['ndatetime','nbid','nask','close','volume','deal'])
lastclose = tmpdf.at[tmpdf.last_valid_index(),'close']
del tmpdf
dayticks = pd.read_csv(direct+'\\'+file,header=None,names=['ndatetime','nbid','nask','close','volume','deal'])
dayticks['ndatetime']=pd.to_datetime(dayticks['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
# dayticks=dayticks[(dayticks.ndatetime.dt.hour>14) | (dayticks.ndatetime.dt.hour<8)] # 夜盤
dayticks=dayticks[(dayticks.ndatetime.dt.hour>=8) & (dayticks.ndatetime.dt.hour<15)] # 日盤
dayticks.sort_values(by=['ndatetime'],ascending=True)
dayticks.index = dayticks.ndatetime
print(dayticks.tail())
mindf=dayticks['close'].resample('1min',closed='right').ohlc()
tmpdf=dayticks['deal'].resample('1min').sum()
mindf=pd.concat([mindf,tmpdf],axis=1)
mindf=mindf.dropna()
print(mindf.head())
mindf['dealminus']=mindf['deal'].cumsum()
del mindf['deal']
mindf=mindf.rename_axis('ndatetime').reset_index()
mindf.columns = ['ndatetime','open','high','low','close','dealminus']
mindf['ndatetime'] = pd.to_datetime(mindf['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
mindf[['open','high','low','close','dealminus']]= mindf[['open','high','low','close','dealminus']].astype(int)
data=mindf.reset_index(drop=True)
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
            p.setPen(pg.mkPen(color='w'))
            p.drawLine(QtCore.QPointF(t, x.low), QtCore.QPointF(t, x.high))
            p.setPen(pg.mkPen(color='w',width=0.1))
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

class BarItem(pg.GraphicsObject):
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

    def set_data(self,nidx,dealminus,ndata):
        if self.lastidx == nidx:
            self.data.at[self.lastidx,'dealminus'] = ndata.at[self.lastidx,'dealminus']
        elif nidx is not None and nidx > self.lastidx and self.lastidx!=0:
            col = ndata.columns.tolist()
            for row in col :
                self.data.at[self.lastidx,row]=ndata.at[self.lastidx,row]
            self.data=self.data.append(ndata.tail(nidx-self.lastidx),ignore_index=True)
            self.lastidx = nidx

        elif self.lastidx==0:
            self.data = ndata.reset_index(drop=True)
            if self.data.last_valid_index()==nidx:
                self.lastidx = nidx
            else:
                print('繪圖Index資料有誤2')
        else :
            print('繪圖資料有誤!!',nidx)
        if self.data.dealminus.max()>self.high:
            self.high=self.data.dealminus.max()
        if self.data.dealminus.min()<self.low:
            self.low=self.data.dealminus.min()

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

        for (t, x) in self.data.loc[start:stop, ['dealminus']].iterrows():
            picture = QtGui.QPicture()
            p = QtGui.QPainter(picture)
            p.setPen(pg.mkPen(color='w',width=0.1))
            if x.dealminus<0:
                p.setBrush(pg.mkBrush('g'))
            elif x.dealminus>0:
                p.setBrush(pg.mkBrush('r'))
            else:
                p.setBrush(pg.mkBrush('w'))
            p.drawRect(QtCore.QRectF(t-w, 0, w*2, x.dealminus))
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
        self.kitem = CandlestickItem()
        YCline = pg.InfiniteLine(angle=0, movable=False)
        YCline.setPos(lastclose)
        self.MyAxis = pg.AxisItem(orientation='bottom')
        self.draw1 = self.l.addPlot(axisItems={'bottom': self.MyAxis})
        # self.draw1 = self.l.addPlot()
        self.draw1.addItem(self.kitem)
        # data = mindf.loc[1065:1365,['ndatetime','open','high','low','close']].reset_index(drop=True)
        
        self.draw1.addItem(YCline)
        # data =data.reindex(list(range(0,300)))
        # data = data.reset_index(drop=True)
        
        self.kitem.set_data(data.last_valid_index(),data.high.max(),data.low.min(),data)
        dict_tmp=data['ndatetime'][data.ndatetime.dt.minute==0].dt.strftime('%H:%M:%S').to_dict()
        self.MyAxis.setTicks([dict_tmp.items()])
        self.draw1.setTitle('test')
        self.draw1.showAxis('left',show=False)
        self.draw1.showAxis('top',show=False)
        self.draw1.showAxis('right',show=True)
        self.l.nextRow()
        self.MyAxis2 = pg.AxisItem(orientation='bottom')
        self.draw2=self.l.addPlot(axisItems={'bottom': self.MyAxis2})
        self.MyAxis2.setTicks([dict_tmp.items()])
        # self.draw2=self.l.addPlot()
        self.bar = BarItem()
        self.draw2.addItem(self.bar)
        print(data[['ndatetime','dealminus']].head())
        self.bar.set_data(data.last_valid_index(),data.at[data.last_valid_index(),'dealminus'],data[['ndatetime','dealminus']])
        self.draw2.setXLink(self.draw1)
        self.draw2.showAxis('left',show=False)
        self.draw2.showAxis('top',show=False)
        self.draw2.showAxis('right',show=True)


        self.l.layout.setRowStretchFactor(0, 3)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    MG = MainWindows()

    MG.show()
    sys.exit(app.exec_())