#匯入所需module
import datetime
import time
import numpy as np
import pandas as pd
import os
import multiprocessing as mp
from PySide6.QtCore import QObject,Signal,Slot

class dataprocess(QObject):
    def __init__(self,inputname,inputindex):
        self.name=inputname
        self.commodityIndex = inputindex
        self.queue_signal = Signal(list)
        self.queue_signal.connect(self.receive_data)
        self.Queue = mp.Queue()
    @Slot(list)
    def receive_data(self,nlist):
        print(nlist)