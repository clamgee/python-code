import pyqtgraph as pg
import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QApplication, QGraphicsView, QGraphicsScene
from PyQt5.uic import loadUi
import sys

tmp = pd.read_csv('../APIver1/result.csv')
tmp['ndatetime'] = pd.to_datetime(tmp['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
data = tmp['close'].tolist()

dict_tmp = tmp['ndatetime'].dt.strftime('%Y/%m/%d %H:%M:%S.%f')
dict_tmp = dict(enumerate(dict_tmp))
# print(list(dict_tmp.keys()))

# win = pg.GraphicsWindow()
# straxis = pg.AxisItem(orientation='bottom')
# straxis.setTicks([dict_tmp.items()])
# plot = win.addPlot(axisItems={'bottom': straxis})
# plot.plot(list(dict_tmp.keys()), data)


def makeKL(name):
    vb = pg.ViewBox()
    Plotitem = pg.PlotItem(viewBox=vb, name=name, axisItems=axisTime)
    Plotitem.setMenuEnabled(False)
    Plotitem.setClipToView(True)
    Plotitem.hideAxis('left')
    Plotitem.showAxis('right')
    Plotitem.setRange(xRange=(0, 1), yRange=(0, 1))
    Plotitem.getAxis('right').setWidth(60)
    Plotitem.showGrid(x=True, y=True)
    Plotitem.hideButtons()
    return Plotitem

class StringAxis(pg.AxisItem):
    def __init__(self, data, *args, **kwargs):
        pg.AxisItem.__init__(self, *args, **kwargs)
        self.tmpdata = data['ndatetime'].dt.strftime('%Y/%m/%d %H:%M:%S.%f').to_dict()


class MainWindwos(QMainWindow):
    def __init__(self):
        super(MainWindwos, self).__init__()
        loadUi(r'MG.ui', self)
        self.vb = makeKL('Line')
        self.drawline = pg.PlotWidget()
        self.drawline(x=tmp.index.tolist(), y=tmp['close'].tolist(), p='g')
        self.vb.addItem(self.drawline)
        self.secnse = QGraphicsScene()
        self.secnse.addItem(self.vb)
        self.secnse.setFocus(self.vb)
        self.graphicsView.mapToScene(self.secnse)
#


if __name__ == '__main__':
    app = QApplication(sys.argv)


    sys.exit(app.exec_())
