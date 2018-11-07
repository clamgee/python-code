import pyqtgraph as pg
from pyqtgraph import QtCore, QtGui
import datetime
import time
import csv
import pandas as pd
import numpy as np

class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data  ## data must have fields: time, open, close, min, max
        self.generatePicture()
    
    def generatePicture(self):
        start=time.time()
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        w = 1.0 / 3.0
        for (t, x) in data.loc[:, ['open', 'high', 'low', 'close']].iterrows():
            p.drawLine(QtCore.QPointF(t, x.low), QtCore.QPointF(t, x.high))
            if x.open>x.close:
                p.setBrush(pg.mkBrush('g'))
            elif x.open<x.close:
                p.setBrush(pg.mkBrush('r'))
            else:
                p.setBrush(pg.mkBrush('w'))
            p.drawRect(QtCore.QRectF(t-w, x.open, w*2, x.close-x.open))
        # for (t, open, close, min, max) in self.data:
        #     p.drawLine(QtCore.QPointF(t, min), QtCore.QPointF(t, max))
        #     if open > close:
        #         p.setBrush(pg.mkBrush('r'))
        #     else:
        #         p.setBrush(pg.mkBrush('g'))
        #     p.drawRect(QtCore.QRectF(t-w, open, w*2, close-open))
        p.end()
        end=time.time()
        ep=round((end-start),6)
        print('繪圖時間1: ',ep)
    
    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
    
    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())

csvpf=pd.DataFrame(columns=['ndatetime','open','high','low','close','volume'])
print('DataFrame大小: ',csvpf.shape[0])
csvpf[['open','high','low','close','volume']]=csvpf[['open','high','low','close','volume']].astype(int)
data=csvpf[['ndatetime','open','high','low','close']]
# item = CandlestickItem(data)
# plt = pg.plot()
# plt.addItem(item)
QtGui.QApplication.exec_()
with open('data.csv',mode='r',newline='') as file:
    rows=csv.reader(file)
    for row in rows:
        ndatetime=datetime.datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S.%f')
        newlist=[ndatetime,int(row[1]),int(row[2]),int(row[3]),int(row[4]),int(row[5])]
        csvpf.loc[ndatetime]=newlist
        csvpf= csvpf.reset_index(drop=True)
        data=csvpf[['ndatetime','open','high','low','close']]
        start=time.time()
        item = CandlestickItem(data)
        plt = pg.plot()
        plt.addItem(item,)
        plt.showGrid(x=True,y=True,alpha=0.3)
        end=time.time()
        ep=end-start
        print('繪圖時間2: ',ep)
        time.sleep(1)
# data = [ ## fields are (time, open, close, min, max).
#     (1., 10, 13, 5, 15),
#     (2., 13, 17, 9, 20),
#     (3., 17, 14, 11, 23),
#     (4., 14, 15, 5, 19),
#     (5., 15, 9, 8, 22),
#     (6., 9, 15, 8, 16),
# ]
# item = CandlestickItem(data)
