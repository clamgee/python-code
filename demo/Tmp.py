import multiprocessing as mp
from multiprocessing import current_process
import threading as td
import time,os
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg

num = 10

class AClass:
    def __init__(self,input):
        print('__init__')
        self.num = input
        super(AClass,self).__init__()
    
    # def __new__(cls):
    #     print('__new__')
    #     return super(AClass,cls).__new__(cls)
    
    def __call__(self):
        print('__call__')

A=AClass(num)
B=AClass(num)

print(id(A),id(B))
print(id(num),id(A.num),id(B.num))



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