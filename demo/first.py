import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QWidget
import pandas as pd
tmp = pd.read_csv('../APIver1/result.csv')
print(tmp.tail(5))