from PySide6.QtCore import QThread, Signal,Slot
from PySide6.QtWidgets import QApplication
import multiprocessing as mp

def threadfunc(func,*args):
    f

class Main:
    def __init__(self) -> None:
        self.name = 'main'
        self.subclass = sub(5,self)
        print(self.mainfunc(5))
    def mainfunc(self,i):
        sum = 12+i
        return sum

class sub:
    def __init__(self,j,parent=None):
        super(sub,self).__init__()
        self.name = 'sub'
        self.j = j
        self.parent = parent
        print(self.parent.__file__())
        # self.subfunc(self.parent.mainfunc(self.j))
        self.subfunc(self.j)

    def subfunc(self,j):
        total = j*j
        print('sub: ',total)

if __name__ == '__main__':
    main = Main()

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