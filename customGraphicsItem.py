import pyqtgraph as pg
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton
from PyQt5 import QtGui,QtCore
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

class KeyWraper(QWidget):
    """键盘鼠标功能支持的元类"""
    #初始化
    #----------------------------------------------------------------------
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setMouseTracking(True)

    #重载方法keyPressEvent(self,event),即按键按下事件方法
    #----------------------------------------------------------------------
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Up:
            self.onUp()
        elif event.key() == QtCore.Qt.Key_Down:
            self.onDown()
        elif event.key() == QtCore.Qt.Key_Left:
            self.onLeft()
        elif event.key() == QtCore.Qt.Key_Right:
            self.onRight()
        elif event.key() == QtCore.Qt.Key_PageUp:
            self.onPre()
        elif event.key() == QtCore.Qt.Key_PageDown:
            self.onNxt()

    #重载方法mousePressEvent(self,event),即鼠标点击事件方法
    #----------------------------------------------------------------------
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.onRClick(event.pos())
        elif event.button() == QtCore.Qt.LeftButton:
            self.onLClick(event.pos())

    #重载方法mouseReleaseEvent(self,event),即鼠标点击事件方法
    #----------------------------------------------------------------------
    def mouseRelease(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.onRRelease(event.pos())
        elif event.button() == QtCore.Qt.LeftButton:
            self.onLRelease(event.pos())
        self.releaseMouse()

    #重载方法wheelEvent(self,event),即滚轮事件方法
    #----------------------------------------------------------------------
    def wheelEvent(self, event):
        return

    #重载方法paintEvent(self,event),即拖动事件方法
    #----------------------------------------------------------------------
    def paintEvent(self, event):
        self.onPaint()

    # PgDown键
    #----------------------------------------------------------------------
    def onNxt(self):
        pass

    # PgUp键
    #----------------------------------------------------------------------
    def onPre(self):
        pass

    # 向上键和滚轮向上
    #----------------------------------------------------------------------
    def onUp(self):
        pass

    # 向下键和滚轮向下
    #----------------------------------------------------------------------
    def onDown(self):
        pass
    
    # 向左键
    #----------------------------------------------------------------------
    def onLeft(self):
        pass

    # 向右键
    #----------------------------------------------------------------------
    def onRight(self):
        pass

    # 鼠标左单击
    #----------------------------------------------------------------------
    def onLClick(self,pos):
        pass

    # 鼠标右单击
    #----------------------------------------------------------------------
    def onRClick(self,pos):
        pass

    # 鼠标左释放
    #----------------------------------------------------------------------
    def onLRelease(self,pos):
        pass

    # 鼠标右释放
    #----------------------------------------------------------------------
    def onRRelease(self,pos):
        pass

    # 画图
    #----------------------------------------------------------------------
    def onPaint(self):
        pass

class MyStringAxis(pg.AxisItem):
    """时间序列横坐标支持"""
    
    # 初始化 
    #----------------------------------------------------------------------
    def __init__(self, xdict, *args, **kwargs):
        pg.AxisItem.__init__(self, *args, **kwargs)
        self.minVal = 0 
        self.maxVal = 0
        self.xdict  = xdict
        self.x_values = np.asarray(xdict.keys())
        self.x_strings = xdict.values()
        self.setPen(color=(255, 255, 255, 255), width=0.8)
        self.setStyle(tickFont = QFont("Roman times",10,QFont.Bold),autoExpandTextSpace=True)

    # 更新坐标映射表
    #----------------------------------------------------------------------
    def update_xdict(self, xdict):
        self.xdict.update(xdict)
        self.x_values  = np.asarray(self.xdict.keys())
        self.x_strings = self.xdict.values()

    # 将原始横坐标转换为时间字符串,第一个坐标包含日期
    #----------------------------------------------------------------------
    def tickStrings(self, values, scale, spacing):
        strings = []
        for v in values:
            vs = v * scale
            if vs in self.x_values:
                vstr = self.x_strings[np.abs(self.x_values-vs).argmin()]
                vstr = vstr.strftime('%Y-%m-%d %H:%M:%S')
            else:
                vstr = ""
            strings.append(vstr)
        return strings

class CustomViewBox(pg.ViewBox):
    #----------------------------------------------------------------------
    def __init__(self, *args, **kwds):
        pg.ViewBox.__init__(self, *args, **kwds)
        # 拖动放大模式
        #self.setMouseMode(self.RectMode)
        
    ## 右键自适应
    #----------------------------------------------------------------------
    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.autoRange()

class KLineWidget(KeyWraper):
    """顯示主圖"""

    # 視窗標示
    clsId = 0

    # 資料變數
    KlineData = None

    # 是否完成讀取歷史資料
    initCompleted = False
    
    #----------------------------------------------------------------------
    def __init__(self,parent=None):
        # 構造函數
        self.parent = parent
        super(KLineWidget, self).__init__(parent)

        # X軸序號
        self.index    = None    # X軸編號
        self.countK   = 60      # 顯示K線數量

        KLineWidget.clsId += 1
        self.windowId = str(KLineWidget.clsId)

        # 資料變數
        self.KBarData = None
        # 所有K线上信号图
        # self.allColor = deque(['blue','green','yellow','white'])
        # self.sigData  = {}
        # self.sigColor = {}
        # self.sigPlots = {}

        # 所副图上信号图
        # self.allSubColor = deque(['blue','green','yellow','white'])
        # self.subSigData  = {}
        # self.subSigColor = {}
        # self.subSigPlots = {}

        # 初始化完成
        self.initCompleted = False

        # 调用函数
        self.initUi()

    #----------------------------------------------------------------------
    #  初始化相关 
    #----------------------------------------------------------------------
    def initUi(self):
        # 繪圖界面初始化
        self.setWindowTitle(u'K線')
        # 主图
        self.pw = pg.PlotWidget()
        # 界面布局
        self.lay_KL = pg.GraphicsLayout(border=(100,100,100))
        self.lay_KL.setContentsMargins(10, 10, 10, 10)
        self.lay_KL.setSpacing(0)
        self.lay_KL.setBorder(color=(255, 255, 255, 255), width=0.8)
        self.lay_KL.setZValue(0)
        self.KLtitle = self.lay_KL.addLabel(u'')
        self.pw.setCentralItem(self.lay_KL)
        # 设置横坐标
        xdict = {}
        self.axisTime = MyStringAxis(xdict, orientation='bottom')
        # 初始化子图
        self.initplotKline()
        # self.initplotVol()  
        # self.initplotOI()
        # 注册十字光标
        # self.crosshair = Crosshair(self.pw,self)
        # 设置界面
        self.vb = QVBoxLayout()
        self.vb.addWidget(self.pw)
        self.setLayout(self.vb)
        # 初始化完成
        self.initCompleted = True   
    
    def makePI(self,name):
        """生成PlotItem对象"""
        vb = CustomViewBox()
        plotItem = pg.PlotItem(viewBox = vb, name=name ,axisItems={'bottom': self.axisTime})
        plotItem.setMenuEnabled(False)
        plotItem.setClipToView(True)
        plotItem.hideAxis('left')
        plotItem.showAxis('right')
        plotItem.setDownsampling(mode='peak')
        plotItem.setRange(xRange = (0,1),yRange = (0,1))
        plotItem.getAxis('right').setWidth(60)
        plotItem.getAxis('right').setStyle(tickFont = QFont("Roman times",10,QFont.Bold))
        plotItem.getAxis('right').setPen(color=(255, 255, 255, 255), width=0.8)
        plotItem.showGrid(True,True)
        plotItem.hideButtons()
        return plotItem

    def initplotKline(self):
        """初始化K线子图"""
        self.pwKL = self.makePI('_'.join([self.windowId,'PlotKL']))
        self.candle = CandlestickItem()
        self.pwKL.addItem(self.candle)
        self.pwKL.setMinimumHeight(350)
        self.pwKL.setXLink('_'.join([self.windowId,'PlotOI']))
        self.pwKL.hideAxis('bottom')

        self.lay_KL.nextRow()
        self.lay_KL.addItem(self.pwKL)

    def refresh(self):
        # 更新X軸邊界        
        # minutes = int(self.countK/2)
        xmin    = max(0,len(self.candle.pictures))
        try:
            xmax    = len(self.candle.pictures)
        except:
            xmax    = len(self.candle.pictures)
        # self.pwOI.setRange(xRange = (xmin,xmax))
        self.pwKL.setRange(xRange = (xmin,xmax))
        # self.pwVol.setRange(xRange = (xmin,xmax))


    def loadData(self, datas, sigs = None):
        # 更新K線資料
        self.candle.set_data(datas)
        self.refresh()

        # 设置中心点时间
        # 绑定数据，更新横坐标映射，更新Y轴自适应函数，更新十字光标映射
        # self.axisTime.xdict={}
        # xdict = dict(enumerate(datas.index.tolist()))
        # self.axisTime.update_xdict(xdict)
        # self.resignData(self.datas)





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

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    # K线界面
    ui = KLineWidget()
    ui.show()
    ui.KLtitle.setText('rb1701',size='20pt')
    ui.loadData(data)
    
    # ui.refreshAll()
    app.exec_()


