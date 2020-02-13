import pyqtgraph as pg
import pandas as pd
import numpy as np
import sys

tmp = pd.read_csv('../APIver1/result.csv')
tmp['ndatetime'] = pd.to_datetime(tmp['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
data = tmp[['close']].
# a = pg.LinearRegionItem(data)
pg.plot(data, pen=(255,0,0), name="Red curve")
# pg.plot(data, title="Simplest possible plotting example")


if __name__ == '__main__':
    app = pg.QtGui.QApplication(sys.argv)
    sys.exit(app.exec_())