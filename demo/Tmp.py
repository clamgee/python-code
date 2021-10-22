import pandas as pd
import numpy as np
import multiprocessing as mp
import time
import pyqtgraph as pg
from PySide6.QtCore import QAbstractTableModel,Qt,QTime
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtGui import QFont
print(time.localtime().tm_hour)

# Candledf=pd.read_csv('../result.dat',low_memory=False)
# Candledf['ndatetime']=pd.to_datetime(Candledf['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')

a = pg.GraphicsObject()
a._updateView()
b=pg.plot()
b.addItem(a)
b.updateMatrix(propagate=True)