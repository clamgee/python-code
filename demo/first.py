import pyqtgraph as pg
import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem, QFrame
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QGraphicsLayout
from PyQt5.uic import loadUi
import sys


tmp = pd.read_csv('../APIver1/result.csv')
tmp['ndatetime'] = pd.to_datetime(tmp['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
data = tmp['close'].tolist()

dict_tmp = tmp['ndatetime'].dt.strftime('%Y/%m/%d %H:%M:%S.%f')
dict_tmp = dict(enumerate(dict_tmp))
# print(list(dict_tmp.keys()))

class MainWindwos(QMainWindow):
    def __init__(self):
        super(MainWindwos, self).__init__()
        loadUi(r'MG.ui', self)
        self.lineplot = pg.PlotDataItem()
        self.lineplot.setData(y=data)
        self.vb = pg.ViewBox()
        self.vb.addItem(self.lineplot)
        self.scene = QGraphicsScene()
        self.scene.addItem(self.vb)
        self.GV.setScene(self.scene)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # lineplot = pg.PlotDataItem()
    # lineplot.setData(y=data)
    # vb = pg.ViewBox()
    # vb.addItem(lineplot)
    # gv = pg.GraphicsView()
    # l = pg.Qt.QtGui.QGraphicsGridLayout()
    # l.setHorizontalSpacing(0)
    # l.setVerticalSpacing(0)
    # l.addItem(vb,0,1)
    # gv.centralWidget.setLayout(l)
    # gv.show()
    MW = MainWindwos()
    MW.show()


    

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


