# import datetime
import time
# print(time.localtime(time.time()).tm_hour)
import pyqtgraph.examples
import sys
from PyQt5 import QtGui, QtCore
import pandas as pd
import numpy as np

lista = ['r1c1', 'r1c2', 'r1c3']
listb = ['r2c1', 'r2c2', 'r1c3']
listc = ['r3c1', 'r3c2', 'r3c3']
mystruct = {'row1':lista, 'row2':listb, 'row3':listc}


for key in mystruct:
    print(key)
