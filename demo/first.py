import pyqtgraph as pg
import pandas as pd
from PyQt5.QtWidgets import QMainWindow,QWidget,QGridLayout,QApplication
import sys

tmp = pd.read_csv('../APIver1/result.csv')
tmp['ndatetime'] = pd.to_datetime(tmp['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
data = tmp['close'].tolist()

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

class MainWindwos(QMainWindow):
    def __init__(self):
        self.setWindowTitle('主視窗')
        self



pw = pg.PlotWidget(data)


# pg.plot(data, pen=(255,255,0), name="Red curve")
# pg.plot(data, title="Simplest possible plotting example")


if __name__ == '__main__':
    app = pg.QtGui.QApplication(sys.argv)
    sys.exit(app.exec_())