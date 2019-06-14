from PyQt5.uic import loadUi #使用.ui介面模組
from PyQt5.QtCore import pyqtSlot,QDate,QTime,QDateTime,QTimer,Qt #插入資訊模組
from PyQt5.QtWidgets import QApplication,QDialog,QFileDialog,QMainWindow,QGraphicsScene,QHeaderView,QTableWidget,QTableWidgetItem #PyQt5介面與繪圖模組
from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import datetime
import time
import csv
import pandas as pd
import numpy as np

class CandlestickItem(pg.GraphicsObject):
    def __init__(self):
        pg.GraphicsObject.__init__(self)
        self.lastbar = None
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
        self.low,self.high = (self.data['low'].values.min(),self.data['high'].values.max()) if len(data)>0 else (0,1)
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
        if not self.rect == (rect.left(),rect.right()) or self.picturemain is None or self.lastbar != self.data.iloc[-1,0]:
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

# csvpf=pd.read_csv('result.csv')
# csvpf['ndatetime']=pd.to_datetime(csvpf['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
# print(csvpf.tail(5))
# print(csvpf.info())
# print(csvpf.shape)
# data=csvpf[['ndatetime','open','high','low','close']]
# item=CandlestickItem()
# app = QtGui.QApplication([])
# plt=pg.PlotWidget()

# plt.addItem(item)
# plt.showGrid(y=True)
# plt.plotItem.hideAxis('left')
# plt.plotItem.showAxis('right')
# item.set_data(data)
# xmax=int(len(item.pictures))
# xmin=int(max(0,(xmax-item.countK)))
# print(xmax,xmin)
# ymin=item.data.loc[xmin:xmax,['low']].values.min()
# ymax=item.data.loc[xmin:xmax,['high']].values.max()
# plt.setXRange(xmin,xmax)
# plt.setYRange(ymin,ymax)
# plt.show()


class TMW(QMainWindow): #主視窗
    def __init__(self):
        super(TMW,self).__init__()
        loadUi(r'TMW.ui',self)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setHorizontalHeaderLabels(['買價','成交價','賣價'])

if __name__ == "__main__":
    import sys
    App=QApplication(sys.argv)
    TMWindow=TMW()
    csvpf=pd.read_csv('result.csv')
    csvpf['ndatetime']=pd.to_datetime(csvpf['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
    print(csvpf.tail(5))
    print(csvpf.info())
    print(csvpf.shape)
    data=csvpf[['ndatetime','open','high','low','close']]
    # TMWindow.bestfive['close']=TMWindow.bestfive['close'].map(lambda x:data.iloc[-1,4]+(TMWindow.bestfive['close'][TMWindow.bestfive['close']==x].index[0]-13))
    item=CandlestickItem()
    KLWidget=pg.PlotWidget()
    KLWidget.addItem(item)
    TMWindow.gridLayout_3.addWidget(KLWidget)
    item.set_data(data)
    bestfive=pd.DataFrame(np.arange(27).reshape(27),columns=['close'])
    bestfive['bid']=''
    bestfive['ask']=''
    i=0
    print(bestfive.shape[0])
    while i < bestfive.shape[0]:
            TMWindow.tableWidget.setItem(i,1,QTableWidgetItem(str(bestfive.iloc[i,0])))
            print(bestfive.iloc[i,0])
            i=i+1

    TMWindow.show()
    sys.exit(App.exec_())