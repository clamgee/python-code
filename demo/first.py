import pyqtgraph as pg
from pyqtgraph import GraphicsLayoutWidget
import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem, QFrame
from PyQt5.QtCore import QRectF,QEvent
from PyQt5.uic import loadUi
import sys
import os

# pg.GraphicsView

tmp = pd.read_csv('../result.dat')
tmp['ndatetime'] = pd.to_datetime(tmp['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
data = tmp['close'].tolist()
data2 = tmp['volume'].tolist()
data2index = tmp.index.tolist()
print(tmp.iloc[-2:])


# dict_tmp = tmp['ndatetime'].dt.strftime('%Y/%m/%d %H:%M:%S.%f').tolist()
# print(dict_tmp.head())
# dict_tmp=dict_tmp.to_dict()

dict_tmp = tmp['ndatetime'].dt.strftime('%Y/%m/%d %H:%M:%S.%f').to_dict()
#dict_tmp.items()
# print(list(dict_tmp.keys()))
# pg.GraphicsView.setCentralWidget()

class MainWindows(QMainWindow):
    def __init__(self):
        super(MainWindows, self).__init__()
        pg.setConfigOption('leftButtonPan', False)
        loadUi(r'MG.ui', self)
        self.MyAxis = pg.AxisItem(orientation='bottom')
        self.MyAxis.setTicks([dict_tmp.items()])
        self.P1 = self.GW.addPlot(row=0,col=0,axisItems={'bottom': self.MyAxis},y=data)
        self.P1.setXRange(9500,9558)
        self.P2 = self.GW.addPlot(row=1,col=0)
        self.GW.ci.layout.setRowStretchFactor(0,3)
        # self.draw1(axisItems={'bottom': self.MyAxis})
        # self.draw1 = self.l.addPlot(axisItems={'bottom': self.MyAxis},y=data)
        # self.draw1.setTitle('test')
        # self.draw1.showAxis('left',show=False)
        # self.draw1.showAxis('top',show=False)
        # self.draw1.showAxis('right',show=True)
        # self.draw1.setXRange(7100,7500)
        # self.draw1.setYRange(12000,17000)
        # self.l.nextRow()
        # self.draw3=self.l.addPlot()
        self.bar = pg.BarGraphItem(x=data2index,height=data2,width=0.3,bush='r')
        self.P2.addItem(self.bar)

        # self.draw3.addItem(self.bar)
        # self.l.layout.setRowStretchFactor(0, 3)
        self.P1.setMouseEnabled(x=False, y=False)
        self.P1.setMenuEnabled(False)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    MG = MainWindows()

    MG.show()
    sys.exit(app.exec_())


# def makeKL(name):
#     vb = pg.ViewBox()
#     # Plotitem = pg.PlotItem(viewBox=vb, name=name, axisItems=axisTime)
#     Plotitem = pg.PlotItem(viewBox=vb, name=name, axisItems=None)
#     Plotitem.setMenuEnabled(False)
#     Plotitem.setClipToView(True)
#     Plotitem.hideAxis('left')
#     Plotitem.showAxis('right')
#     Plotitem.setRange(xRange=(0, 1), yRange=(0, 1))
#     Plotitem.getAxis('right').setWidth(60)
#     Plotitem.showGrid(x=True, y=True)
#     Plotitem.hideButtons()
#     return Plotitem
#
# class StringAxis(pg.AxisItem):
#     def __init__(self, data, *args, **kwargs):
#         pg.AxisItem.__init__(self, *args, **kwargs)
#         self.tmpdata = data['ndatetime'].dt.strftime('%Y/%m/%d %H:%M:%S.%f').to_dict()
#
#

#
#

