import pandas as pd
import pyqtgraph as pg
import numpy as np
from pyqtgraph import QtCore,QtGui,GraphicsItem

class CandleItem(pg.GraphicsObject):
    def __init__(self,parent=None):
        pg.GraphicsObject.__init__(self)
        # super(CandleItem, self).__init__(parent)
        self.data = parent
        print(self.data.Tick12Kpd.tail(5))
        self.lastbar = None
        self.picturemain = QtGui.QPicture() #主K線圖
        self.picturelast = QtGui.QPicture() #最後一根K線圖
        self.pictures = []
        self.PaintChange = False
        self.setFlag(self.ItemUsesExtendedStyleOption)
        self.rect = None
        self.high = self.data.Tick12Kpd.high.max()
        print('原生',self.high)
        self.low = self.data.Tick12Kpd.low.min()
        self.lastidx = parent.lastidx
        self.countK = 87 #設定要顯示多少K線
        self.generatePicture()
        self.informViewBoundsChanged()
        self._updateView() #強制圖形更新


    def set_data(self):
        # self.data = parent.Tick12Kpd
        if self.high < self.data.High:
            self.high = self.data.High
            print('比對:',self.high)
        if self.low > self.data.Low:
            self.low = self.data.Low
        if self.lastidx != self.data.lastidx:
            self.PaintChange = True
            self.lastidx = self.data.lastidx
        # else :
        #     print('繪圖資料有誤!!',self.lastidx,',',parent.lastidx)
        self.generatePicture()
        self.informViewBoundsChanged()
        self._updateView() #強制圖形更新
        # print('set_data: ',self.data.tail(1))
    
    def generatePicture(self):    
        # 重畫或者最後一根K線
        if int(len(self.pictures))>1:
            self.pictures.pop()
        w = 1.0 / 3.0
        start = len(self.pictures)
        # print('圖片長度: ',start)
        stop = self.lastidx + 1
        for (t, x) in self.data.Tick12Kpd.loc[start:stop, ['open', 'high', 'low', 'close']].iterrows():
            picture = QtGui.QPicture()
            p = QtGui.QPainter(picture)
            if x.open>x.close:
                p.setBrush(pg.mkBrush('g'))
                p.setPen(pg.mkPen('g'))
            elif x.open<x.close:
                p.setBrush(pg.mkBrush('r'))
                p.setPen(pg.mkPen('r'))
            else:
                p.setBrush(pg.mkBrush('w'))
                p.setPen(pg.mkPen('w'))
            p.drawLine(QtCore.QPointF(t, x.low), QtCore.QPointF(t, x.high))
            p.drawRect(QtCore.QRectF(t-w, x.open, w*2, x.close-x.open))
            p.end()
            self.pictures.append(picture)
        
    def paint(self,painter,*args):
        if self.PaintChange:
            self.picturemain = self.createPic(0,self.lastidx)
            self.picturemain.play(painter)
            self.picturelast = self.createPic(self.lastidx,self.lastidx+1)
            self.picturelast.play(painter)
            self.PaintChange = False
            # print('重繪')            
        else:
            self.picturemain.play(painter)
            self.picturelast = self.createPic(self.lastidx,self.lastidx+1)
            self.picturelast.play(painter)
            # print('快圖')
    # 圖片產生----------------------------------------------------------------------
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
        self.PaintChange = False
        self.setFlag(self.ItemUsesExtendedStyleOption)
        self.rect = None
        self.low = 0
        self.high = 0
        self.lastidx = 0

    def set_data(self,nidx,ndata):
        if self.data is None:
            self.data = ndata.reset_index(drop=True)
            self.lastidx = nidx
            self.columnname = self.data.columns[-1]
            self.PaintChange = True
        elif self.lastidx == nidx:
            self.data.at[self.lastidx,self.columnname] = ndata.at[self.lastidx,self.columnname]
        elif nidx is not None and nidx > self.lastidx:
            col = ndata.columns.tolist()
            for row in col :
                self.data.at[self.lastidx,row]=ndata.at[self.lastidx,row]
            self.data=self.data.append(ndata.tail(nidx-self.lastidx),ignore_index=True)
            self.lastidx = nidx
            self.PaintChange = True
        else :
            print('繪圖資料有誤!!',self.name,nidx)
            pass
        if self.data[self.columnname].max()>self.high:
            self.high=self.data[self.columnname].max()
        if self.data[self.columnname].min()<self.low:
            self.low=self.data[self.columnname].min()

        self.generatePicture()
        self.informViewBoundsChanged()
        self._updateView() #強制圖形更新
    
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
            if x[-1]<0:
                p.setBrush(pg.mkBrush('g'))
                p.setPen(pg.mkPen(color='g',width=0.1))
            elif x[-1]>0:
                p.setBrush(pg.mkBrush('r'))
                p.setPen(pg.mkPen(color='r',width=0.1))
            else:
                p.setBrush(pg.mkBrush('w'))
                p.setPen(pg.mkPen(color='w',width=0.1))
            p.drawRect(QtCore.QRectF(t-w, 0, w*2, x[-1]))
            p.end()
            self.pictures.append(picture)
        
    def paint(self, painter, *args):
        if self.PaintChange:
            self.picturemain = self.createPic(0,self.lastidx)
            self.picturemain.play(painter)
            self.picturelast = self.createPic(self.lastidx,self.lastidx+1)
            self.picturelast.play(painter)
            self.PaintChange = False
            # print('重繪')            
        else:
            self.picturemain.play(painter)
            self.picturelast = self.createPic(self.lastidx,self.lastidx+1)
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
