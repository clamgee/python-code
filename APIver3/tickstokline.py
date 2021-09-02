#匯入所需module
import datetime
import time
import numpy as np
import pandas as pd
import os
import multiprocessing as mp
from PySide6.QtCore import QObject, QThread,Signal,Slot

class ticksTo12Kprocess(QThread):
    queue_signal = Signal(list)
    def __init__(self,inputname,inputindex):
        super(ticksTo12Kprocess, self).__init__()
        self.name=inputname
        self.commodityIndex = inputindex
        self.queue_signal.connect(self.receive_ticks)
        self.Queue = mp.Queue()
    @Slot(list)
    def receive_ticks(self,nlist):
        self.Queue.put(nlist)
    
    def run(self):
        while True:
            nlist = self.Queue.get()
            print('run',nlist)