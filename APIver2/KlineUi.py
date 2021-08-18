import numpy as np
import pandas as pd
import pyqtgraph as pg
import numpy as np
from pyqtgraph import QtCore,QtGui

class CandleItem(pg.GraphicsObject):
    def __init__(self):
        pg.GraphicsObject.__init__(self)
        self.data = None
        self.lastbar = None
        # self.picture = QtGui.QPicture()
        self.picturemain = QtGui.QPicture() #主K線圖
        self.picturelast = QtGui.QPicture() #最後一根K線圖
        self.pictures = []
        self.setFlag(self.ItemUsesExtendedStyleOption)
        self.rect = None
        self.low = 0
        self.high = 0
        # self.FPS = 0
        self.highavg = ''
        self.lowavg = ''
        # self.timelist = []
        self.lastidx = 0
        self.countK = 60 #設定要顯示多少K線

    def set_data(self,nidx,nhigh,nlow,ndata):
        if self.data is None:
            self.data = ndata.reset_index(drop=True)
            self.high = nhigh
            self.low = nlow
            self.lastidx = nidx
        elif self.lastidx == nidx:
            if self.high < nhigh :
                self.data.at[self.lastidx,'high']=self.high=nhigh 
            if self.low > nlow:
                self.data.at[self.lastidx,'low']=self.low=nlow
            self.data.at[self.lastidx,'close'] = ndata.at[self.lastidx,'close']
            self.data.at[self.lastidx,'volume'] = ndata.at[self.lastidx,'volume']
        elif nidx > self.lastidx:
            col = ndata.columns.tolist()
            for row in col :
                self.data.at[self.lastidx,row]=ndata.at[self.lastidx,row]
            self.data=self.data.append(ndata.tail(nidx-self.lastidx),ignore_index=True)
            self.lastidx = nidx
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

        for (t, x) in self.data.loc[start:stop, ['open', 'high', 'low', 'close']].iterrows():
            picture = QtGui.QPicture()
            p = QtGui.QPainter(picture)
            # p.setPen(pg.mkPen(color='w',width=0.4))
            # p.setPen(pg.mkPen(color='w',width=0.1))
            if x.open>x.close:
                p.setBrush(pg.mkBrush('g'))
                p.setPen(pg.mkPen(color='g'))
            elif x.open<x.close:
                p.setBrush(pg.mkBrush('r'))
                p.setPen(pg.mkPen(color='r'))
            else:
                p.setBrush(pg.mkBrush('w'))
                p.setPen(pg.mkPen(color='w'))
            p.drawRect(QtCore.QRectF(t-w, x.open, w*2, x.close-x.open))
            p.drawLine(QtCore.QPointF(t, x.low), QtCore.QPointF(t, x.high))
            self.pictures.append(picture)
        
    def paint(self, painter, opt, w):
        rect = opt.exposedRect
        xmin,xmax = (max(0,int(rect.left())),min(int(len(self.pictures)),int(rect.right())))
        # self.rect = (rect.left(),rect.right())
        # self.picture = self.createPic(xmin,xmax)
        # self.picture.play(painter)
        if not self.rect == (rect.left(),rect.right()) or self.picturemain is None:# or self.lastbar != self.data.index.values[-1]:
            self.rect = (rect.left(),rect.right())
            #self.lastbar = self.data.index.values[-1]
            # print('rect: ',self.rect)
            # if (xmax-121)<0:
            self.picturemain = self.createPic(xmin,xmax-1)
            # else:
            #     self.picturemain = self.createPic(xmax-121,xmax-1)
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
    def __init__(self,inputname):
        pg.GraphicsObject.__init__(self)
        self.name = inputname
        self.data = None
        self.columnname = None
        self.picturemain = QtGui.QPicture() #主K線圖
        self.picturelast = QtGui.QPicture() #最後一根K線圖
        self.pictures = []
        self.setFlag(self.ItemUsesExtendedStyleOption)
        self.rect = None
        self.low = 0
        self.high = 0
        self.lastidx = 0
        self.countK = 60 #設定要顯示多少K線

    def set_data(self,nidx,ndata):
        if self.data is None:
            self.data = ndata.reset_index(drop=True)
            self.lastidx = nidx
            self.columnname = self.data.columns[-1]
        elif self.lastidx == nidx and self.data is not None:
            self.data.at[self.lastidx,self.columnname] = ndata.at[self.lastidx,self.columnname]
        elif nidx is not None and nidx > self.lastidx and self.data is not None:
            col = ndata.columns.tolist()
            for row in col :
                self.data.at[self.lastidx,row]=ndata.at[self.lastidx,row]
            self.data=self.data.append(ndata.tail(nidx-self.lastidx),ignore_index=True)
            self.lastidx = nidx
        else :
            print('繪圖資料有誤!!',self.name,nidx)
            pass
        if self.data[self.columnname].max()>self.high:
            self.high=self.data[self.columnname].max()
        if self.data[self.columnname].min()<self.low:
            self.low=self.data[self.columnname].min()

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

        for (t, x) in self.data.loc[start:stop, [self.columnname]].iterrows():
            picture = QtGui.QPicture()
            p = QtGui.QPainter(picture)
            p.setPen(pg.mkPen(color='w',width=0.1))
            if x[-1]<0:
                p.setBrush(pg.mkBrush('g'))
            elif x[-1]>0:
                p.setBrush(pg.mkBrush('r'))
            else:
                p.setBrush(pg.mkBrush('w'))
            p.drawRect(QtCore.QRectF(t-w, 0, w*2, x[-1]))
            p.end()
            self.pictures.append(picture)
        
    def paint(self, painter, opt, w):
        rect = opt.exposedRect
        xmin,xmax = (max(0,int(rect.left())),min(int(len(self.pictures)),int(rect.right())))
        if not self.rect == (rect.left(),rect.right()) or self.picturemain is None:
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

class KlineWidget(pg.PlotWidget):
    def __init__(self,name):
        pg.PlotWidget.__init__(self)
        self.name=name
        self.showGrid(y=True)
        self.plotItem.hideAxis('left')
        self.plotItem.showAxis('right')
        self.right=None
        self.high=None
        self.low=None
        
    def update(self,xmin,xmax,ymin,ymax,fps):
        self.plotItem.setLabel('top',text='FPS: '+str(fps))        
        if self.right!=xmax or self.high!=ymax or self.low!=ymin:
            self.right=xmax
            # self.plt.setRange(xRange=(xmin,xmax),yRange=(ymin,ymax))
            self.setXRange(xmin,xmax)
            self.setYRange(ymin,ymax)

        # if self.high!=ymax or self.low!=ymin:
        #     self.low=ymin
        #     self.high=ymax
        #     self.plt.setYRange(ymin,ymax)
