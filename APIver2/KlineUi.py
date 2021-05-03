import numpy as np
import pandas as pd
import pyqtgraph as pg
from pyqtgraph import QtCore,QtGui

class CandlestickItem(pg.GraphicsObject):
    def __init__(self):
        pg.GraphicsObject.__init__(self)
        #self.lastbar = None
        # self.picture = QtGui.QPicture()
        self.picturemain = QtGui.QPicture() #主K線圖
        self.picturelast = QtGui.QPicture() #最後一根K線圖
        self.pictures = []
        self.setFlag(self.ItemUsesExtendedStyleOption)
        self.rect = None
        self.low = 0
        self.high = 0
        self.FPS = 0
        self.highavg = ''
        self.lowavg = ''
        self.len = 0
        self.timelist = []
        self.countK = 60 #設定要顯示多少K線

    def set_data(self,data):
        start=pg.time()
        self.data = data
        self.len = self.data.last_valid_index()
        self.low,self.high = (self.data['low'].min(),self.data['high'].max()) if len(data)>0 else (0,1)
        self.generatePicture()
        self.informViewBoundsChanged()
        if not self.scene() is None:
            self.scene().update() #強制圖形更新
        end=pg.time()
        if len(self.timelist)<100:
            self.timelist.append((end-start))
        else:
            self.timelist.pop(0)
            self.timelist.append((end-start))
        if sum(self.timelist)!=0 and len(self.timelist)>0:
            ep=int(1/(sum(self.timelist)/len(self.timelist)))
        else:
            ep=0
        self.FPS = ep
    
    def generatePicture(self):    
        # 重畫或者最後一根K線
        if int(len(self.pictures))>1:
            self.pictures.pop()
        w = 1.0 / 3.0
        start = len(self.pictures)
        stop = self.data.shape[0]

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
            if self.highavg != '':
                p.setPen(pg.mkPen('b'))
                p.setBrush(pg.mkBrush('b'))
                p.drawLine(QtCore.QPointF(t - 1, self.highavg), QtCore.QPointF(t, x.high_avg))
            # print('圖: ', x.high_avg)

            if self.lowavg != '':
                p.setPen(pg.mkPen('w'))
                p.setBrush(pg.mkBrush('w'))
                p.drawLine(QtCore.QPointF(t - 1, self.lowavg), QtCore.QPointF(t, x.low_avg))
                # p.drawPoint(int(t), int(x.low_avg))

            if t < self.len:
                self.lowavg = x.low_avg
                self.highavg = x.high_avg
            p.end()
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
