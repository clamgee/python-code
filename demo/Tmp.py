import multiprocessing as mp
from multiprocessing import current_process, set_executable, Manager
import PySide6
from PySide6.QtCore import QObject, QThread, Signal,Slot
from PySide6.QtWidgets import QWidget
from threading import Thread
from PySide6.QtWidgets import QApplication
import time,os
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg
import pandas as pd
import numpy as np
from multiprocessing import *
import multiprocessing.sharedctypes as sharedctypes
import dill
import ctypes
# global pass1_signal,pass_signal
# pass_signal = Signal(list)
# pass1_signal = Signal(str)

class QSignal(QObject):
    pass_signal = Signal(list)

class Q(QWidget): 
    def __init__(self,parent):
        self.Qdata = mp.Queue()
        self.pass_signal = parent.pass_signal
        self.pass_signal.connect(self.receive)

    def receive(self,nlist):
        print(nlist)

class Testthread(QThread):
    def __init__(self,*args):
        super(Testthread,self).__init__()
        self.name = args[0]
        self.idx = args[1]
        self.msgtuple = args[2]
        # self.msgtuple = dill.loads(args[2])
        self.Func = 0
        # print(C.__getattribute__(C.pass_signal))

    def func(self):
        self.Func = self.Func + self.idx
        print(self.Func)

    def run(self):
            self.func()
            self.msgtuple.emit([1,2])
            time.sleep(2)

class MyProcess(mp.Process):  # 定义一个类，继承Process类
    def __init__(self,func,*args):
        super(MyProcess, self).__init__()  # 实现父类的初始化方法
        self.name1 = args[0]
        self.idx = args[1]
        self.msgtuple = args[2]
        self.target = func

    def run(self):  # 必须实现的方法，是启动进程的方法
        TD = self.target(self.name1,self.idx,self.msgtuple)
        TD.run()
        nowproc=mp.current_process()
        print('子进程:', os.getpid(), os.getppid(),nowproc)


class AClass:
    def __init__(self,inputsignal):
        self.name ='A'
        self.index = 1
        # self.msgtuple = signal
        self.A = MyProcess(Testthread,self.name,self.index,inputsignal)
        self.A.start()

        # self.B = MyProcess(self.creattd,'B',0,self.msgtuple)
        # self.B.start()
   
    def creattd(self,func,*args):
        print(args[0],args[1],)
        TD = func(args[0],args[1])
        TD.run()
        print(TD.currentThread())

def creattd(*args):
    print(args[0],args[1],args[2])
    TD = Testthread(args[0],args[1],args[2])
    TD.start()
    print(TD.currentThread())


if __name__ =='__main__':
    mp.set_start_method('spawn')
    app = QApplication()
    # B = MyProcess(creattd,'A',1,(1,2))
    # B.start()
    Sig = QSignal()
    global C
    C = Q(parent=Sig)
    # psgl = dill.dumps(C)
    # QT = Testthread('A',1)
    # QT.start()
    B = AClass(Sig.pass_signal)
    app.exec_()


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