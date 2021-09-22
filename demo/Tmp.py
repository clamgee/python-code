import multiprocessing as mp
from multiprocessing import current_process
import threading as td
import time,os
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg

class AClass:
    def __init__(self,input):
        self.num = input

    def run(self):
        print(os.getpid())
        while self.num < 100:
            self.num+=5
            time.sleep(0.5)
            nowproc=mp.current_process()
            print(self.num,nowproc)

def proc(Func):
    p1 = mp.Process(target=Func,daemon=True)
    print(os.getpid())
    p1.start()
    p1.join()

if __name__ =='__main__':
    A = AClass(1)
    proc(A.run())


# import sys
# from PySide6 import QtCore,QtWidgets
# import typing
# # define a new slot that receives a string and has
# # 'saySomeWords' as its name
# class Communicate(QtCore.QObject):
#     speak = QtCore.Signal(str)
#     def __init__(self):
#         super(Communicate, self).__init__()
#         self.ButtonA = None
#         print('in class %s',self.ButtonA)
#         self.speak.connect(self.saySomeWords)
#     @QtCore.Slot(str)
#     def saySomeWords(self,words):
#         print(words)

# if __name__=='__main__':
#     someone = Communicate()
#     # connect signal and slot
#     # someone.speak.connect(saySomeWords)
#     # emit 'speak' signal
#     someone.speak.emit("Hello everybody!")