import pyqtgraph as pg
import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem, QFrame
from PyQt5.QtCore import QRectF
from PyQt5.uic import loadUi
import sys

app = QApplication(sys.argv)
tmp = pd.read_csv('../APIver1/result.csv')
tmp['ndatetime'] = pd.to_datetime(tmp['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
data = tmp['close'].tolist()

dict_tmp = tmp['ndatetime'].dt.strftime('%Y/%m/%d %H:%M:%S.%f')
dict_tmp = dict(enumerate(dict_tmp))
# print(list(dict_tmp.keys()))

lineplot = pg.PlotWidget()
lineplot.plot(data)
vb = pg.ViewBox()
vb.addItem(lineplot)

# class MainWindows(QMainWindow):
#     def __init__(self):
#         super(MainWindows, self).__init__()
#         loadUi(r'MG.ui', self)
#         self.lineplot = pg.PlotWidget()
#         self.lineplot.plot(data)
#         self.vb = pg.ViewBox()
#         self.vb.addItem(self.lineplot)
#         self.scene = QGraphicsScene()
#         self.scene.addItem(self.vb)
#         self.GV.setScene(self.scene)
#         self.vrect = self.GV.sceneRect()
#         self.width = self.vrect.width()
#         self.height = self.vrect.height()
#         self.srect = self.scene.sceneRect()
#         print('srect:',self.srect)
#         self.GV.mapFromScene(self.srect)
#         # self.scene.setSceneRect(0, 0, 800, 600)


if __name__ == '__main__':
    
    # MW = MainWindows()
    # print(MW.GV.geometry())
    # MW.show()
    vb.show()
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
# class MainWindwos(QMainWindow):
#     def __init__(self):
#         super(MainWindwos, self).__init__()
#         loadUi(r'MG.ui', self)
#         self.scene = QGraphicsScene()
#         self.scene.addItem(plot)
#         self.GV(self.scene)
#
#


