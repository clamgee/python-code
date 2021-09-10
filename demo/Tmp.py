from PySide6.QtCore import QThread, Signal,Slot
from PySide6.QtWidgets import QApplication
import multiprocessing as mp

class DataQueue(mp.Queue):
    def __init__(self,inputname,inputidx):
        super(DataQueue,self).__init__()
        self.name = inputname
        self.idx = inputidx
        
    def run(self,a):
        self.put(a)



if __name__=='__main__':
    Q = DataQueue('TX00',0,0)
    print(Q.name,Q.idx)


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