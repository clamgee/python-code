import pyqtgraph as pg
import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem, QFrame
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QGraphicsLayout
from PyQt5.uic import loadUi
import sys

# pg.GraphicsView

tmp = pd.read_csv('../APIver1/result.csv')
tmp['ndatetime'] = pd.to_datetime(tmp['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
data = tmp['close'].tolist()
data2 = tmp['volume'].tolist()
data2index = tmp.index.tolist()


dict_tmp = tmp['ndatetime'].dt.strftime('%Y/%m/%d %H:%M:%S.%f')
dict_tmp = dict(enumerate(dict_tmp))
# print(list(dict_tmp.keys()))
# pg.GraphicsView.setCentralWidget()

class MainWindows(QMainWindow):
    def __init__(self):
        super(MainWindows, self).__init__()
        loadUi(r'MG.ui', self)
        self.l = pg.GraphicsLayout()
        self.GV.setCentralItem(self.l)
        self.draw1 = self.l.addPlot(y=data)
        self.l.nextRow()
        self.draw2 = self.l.addPlot()
        self.bar = pg.BarGraphItem(x=data2index,height=data2,width=0.3,bush='r')
        self.draw2.addItem(self.bar)






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


