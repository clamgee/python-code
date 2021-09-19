import multiprocessing as mp
from multiprocessing import current_process
import threading as td
import time,os
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg

class AClass:
    def __init__(self,input):
        self.num = input

class BClass:
    def __init__(self) -> None:
        self.new = [1,2]

B = BClass()
A = AClass(B.new)

for i in range(5):
    B.new.append(i)
    print(id(A.num),id(B.new))
    print(A.num,' , ',B.new)


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