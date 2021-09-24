import multiprocessing as mp
from multiprocessing import current_process, set_executable
import PySide6
from PySide6.QtCore import QObject, QThread, Signal,Slot
from threading import Thread
from PySide6.QtWidgets import QApplication
import time,os
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg
app = QApplication()
import pickle

class Q(QObject): 
    pass_signal = Signal(list)
    pass1_signal = Signal(str)
    def __init__(self):
        super(Q,self).__init__()
        self.Qdata = mp.Queue()
        self.pass_signal.connect(self.receive)
    def __getattribute__(self, name: str):
        return super().__getattribute__(name)
    @Slot(list)
    def receive(self,nlist):
        print(nlist)

global C
C = Q()

class Testthread(QThread):
    def __init__(self,*args):
        super(Testthread,self).__init__()
        self.name = args[0]
        self.idx = args[1]
        self.msgtuple = args[2]
        self.Func = 0
        # print(C.__getattribute__(C.pass_signal))

    def func(self):
        self.Func = self.Func + self.idx + self.msgtuple[0] + self.msgtuple[1]
        print(self.Func)

    def run(self):
        while self.Func < 20:
            self.func()
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
    def __init__(self):
        self.name ='A'
        self.index = 1
        self.msgtuple = (1,2)
        self.A = MyProcess(Testthread,self.name,self.index,self.msgtuple)
        self.A.start()

        # self.B = MyProcess(self.creattd,'B',0,self.msgtuple)
        # self.B.start()
   
    def creattd(self,func,*args):
        print(args[0],args[1],args[2])
        TD = func(args[0],args[1],args[2])
        TD.run()
        print(TD.currentThread())

def creattd(*args):
    print(args[0],args[1],args[2])
    TD = Testthread(args[0],args[1],args[2])
    TD.start()
    print(TD.currentThread())


if __name__ =='__main__':
    # mp.set_start_method('spawn')
    # B = MyProcess(creattd,'A',1,(1,2))
    # B.start()
    B = AClass()
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