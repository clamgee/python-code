import pandas as pd
import pyqtgraph as pg
import numpy as np
from pyqtgraph import QtCore,QtGui,GraphicsItem

class CandleItem(pg.GraphicsObject):
    def __init__(self):
        pg.GraphicsObject.__init__(self)
        self.picturemain = QtGui.QPicture() #主K線圖
        self.picturelast = QtGui.QPicture() #最後一根K線圖
        self.pictures = []
        self.PaintChange = True
        self.setFlag(self.ItemUsesExtendedStyleOption)
        self.high = 0
        self.low = 0
        self.lastidx = 0
        self.close = 0
        self.countK = 87 #設定要顯示多少K線
        self.nPtr = 0

    def set_data(self,Candledf,nlist):
        self.data = Candledf
        lastidx = nlist[0]; close = nlist[1];self.nPtr = nlist[2]
        if len(self.pictures) == 0:
            self.high = self.data.high.max()
            self.low = self.data.low.min()
            self.lastidx = self.data.last_valid_index()
            self.close = self.data.at[self.lastidx,'close']
        if self.high < close:
            self.high = close
        if self.low > close:
            self.low = close
        if self.lastidx != lastidx:
            self.PaintChange = True
            self.lastidx = self.data.last_valid_index()
        self.generatePicture()
        self.informViewBoundsChanged()
        if self.close != close:
            self.close = self.data.at[self.lastidx,'close']
        if self.scene()!=None:
            self.scene().update()
        # self.update()
    
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
    def __init__(self):
        pg.GraphicsObject.__init__(self)
        self.data = None
        self.columnname = None
        self.picturemain = QtGui.QPicture() #主K線圖
        self.picturelast = QtGui.QPicture() #最後一根K線圖
        self.pictures = []
        self.PaintChange = False
        self.setFlag(self.ItemUsesExtendedStyleOption)
        self.low = 0
        self.high = 0
        self.lastidx = 0
        self.close = 0

    def set_data(self,Candledf,nlist):
        self.data = Candledf
        lastidx = nlist[0]; close = nlist[1]
        self.columnname = self.data.columns[-1]
        if self.high < close:
            self.high = close
        if self.low > close:
            self.low = close
        if self.lastidx != lastidx:
            self.PaintChange = True
            self.lastidx = self.data.last_valid_index()
        self.generatePicture()
        self.informViewBoundsChanged()
        if self.close != close:
            self.close = self.data.at[self.lastidx,self.columnname]
        if self.scene()!=None:
            self.scene().update()
        # self.update()

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
