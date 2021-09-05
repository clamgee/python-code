import datetime
nlist = ['a','b','c']
k1 = nlist[0];k2 = nlist[1];k3 = nlist[2]
print(k1,k2,k3)

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