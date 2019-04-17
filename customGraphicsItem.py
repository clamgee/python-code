import pyqtgraph as pg
from pyqtgraph import QtCore, QtGui
import datetime
import time
import csv
import pandas as pd
import numpy as np

class CandlestickItem(pg.GraphicsObject):
    def __init__(self):
        pg.GraphicsObject.__init__(self)
        self.lastbar = None
        # self.picture = QtGui.QPicture()
        self.picturemain = QtGui.QPicture() #主K線圖
        self.picturelast = QtGui.QPicture() #最後一根K線圖
        self.pictures = []
        self.setFlag(self.ItemUsesExtendedStyleOption)
        self.rect = None
        self.low = 0
        self.high = 0
        self.timelist = []
        self.countK = 60 #設定要顯示多少K線

    def set_data(self,data):
        start=pg.time()
        self.data = data.reset_index(drop=True)
        self.low,self.high = (self.data['low'].min(),self.data['high'].max()) if len(data)>0 else (0,1)
        self.generatePicture()
        self.informViewBoundsChanged()
        # if not self.scene() is None:
        #     self.scene().update() #強制圖形更新
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
        if not self.rect == (rect.left(),rect.right()) or self.picturemain is None: #or self.lastbar != self.data.iloc[-1,0]:
            self.rect = (rect.left(),rect.right())
            self.lastbar = self.data.iloc[-1,0]
            # print('rect: ',self.rect)
            # if (xmax-121)<0:
            self.picturemain = self.createPic(xmin,xmax-1)
            # else:
            #     self.picturemain = self.createPic(xmax-121,xmax-1)
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
item = CandlestickItem()

csvpf=pd.read_csv('result.csv')
csvpf['ndatetime']=pd.to_datetime(csvpf['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
print(csvpf.tail(5))
print(csvpf.info())
print(csvpf.shape)
# print('DataFrame大小: ',csvpf.shape[0])
# csvpf[['open','high','low','close','volume']]=csvpf[['open','high','low','close','volume']].astype(int)
# data=csvpf[['ndatetime','open','high','low','close']]
# with open('data.csv',mode='r',newline='') as file:
#     rows=csv.reader(file)
#     for row in rows:
#         ndatetime=datetime.datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S.%f')
#         newlist=[ndatetime,int(row[1]),int(row[2]),int(row[3]),int(row[4]),int(row[5])]
#         csvpf.loc[ndatetime]=newlist
#         csvpf= csvpf.reset_index(drop=True)
#         
# tmp=data.ndatetime.tail(1)
# print(tmp)

data=csvpf[['ndatetime','open','high','low','close']]
item.set_data(data)

plt = pg.plot()
plt.hideAxis('left')
plt.showAxis('right')
plt.showGrid(False,True)
curve=plt.addItem(item)
x=csvpf.shape[0]-60
plt.setPos(x,0)
plt.setWindowTitle('pyqtgraph example: customGraphicsItem')
QtGui.QApplication.exec_()

