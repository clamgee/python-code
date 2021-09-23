import multiprocessing as mp
from multiprocessing import current_process, set_executable
import PySide6
from PySide6.QtCore import QThread
from PySide6.QtWidgets import QApplication
import time,os
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg
app = QApplication()

class Testthread(QThread):
    def __init__(self,*args):
        QThread.__init__(self)
        self.name1 = args[0]
        self.idx = args[1]
        self.msgtuple = args[2]
        self.Func = 0

    def func(self):
        self.Func = self.idx + self.msgtuple[0] + self.msgtuple[1]
        # print(self.name,self.idx,self.msgtuple[0],self.msgtuple[1])
        print(self.Func)

    def run(self):
        while True:
            self.func()
            print(os.getpid())
            time.sleep(2)

class MyProcess(mp.Process):  # 定义一个类，继承Process类
    def __init__(self,*args):
        super(MyProcess, self).__init__()  # 实现父类的初始化方法
        self.name1 = args[0]
        self.idx = args[1]
        self.msgtuple = args[2]

    def run(self):  # 必须实现的方法，是启动进程的方法
        # self.target(self.name1,self.idx,self.msgtuple)
        self.target = Testthread(self.name1,self.idx,self.msgtuple)
        print('id',self.target.currentThread())
        self.target.start()
        nowproc=mp.current_process()
        print('子进程:', os.getpid(), os.getppid(),nowproc)

class AClass:
    def __init__(self):
        self.name ='A'
        self.index = 1
        self.msgtuple = (1,2)
        self.A = MyProcess(self.name,self.index,self.msgtuple)
        self.A.daemon = True
        self.A.start()

        # self.B = MyProcess(self.creattd,'B',0,self.msgtuple)
        # self.B.start()
   
    def creattd(self,*args):
        self.TD = Testthread(args[0],args[1],args[2])
        self.TD.start()

if __name__ =='__main__':
    B=AClass()
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