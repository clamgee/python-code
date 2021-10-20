import pandas as pd
import numpy as np
import multiprocessing as mp
import time
import pyqtgraph as pg
from PySide6.QtCore import QAbstractTableModel,Qt,QTime
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtGui import QFont
if __name__ == '__main__':
    ns = mp.Manager().Namespace()
    ns.MPower = pd.DataFrame(np.arange(16).reshape(4,4), columns=['ComQty','ComCont','DealCont','DealQty'])
    i=0
    while i < 4 :
        j=0
        while j < 4:
            ns.MPower.at[i,ns.MPower.columns[j]] = QTableWidgetItem('').setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            # ns.MPower.at[i,ns.MPower.columns[j]].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            j+=1
        i+=1
   
    print(ns.MPower)
    print(type(ns.MPower.at[1,ns.MPower.columns[1]]))
    a = QTableWidgetItem()
    f = QFont()
    f.setBold(True)

# Candledf=pd.read_csv('../result.dat',low_memory=False)
# Candledf['ndatetime']=pd.to_datetime(Candledf['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')

