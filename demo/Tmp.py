class Parent(object):
   def __init__(self, name, number):
       self.name = name
       self.number = number


class Child(object):
    def __init__(self, parent, other):
        self.parent = parent
        self.other = other

    def __getattr__(self, name):
        try:
            return getattr(self.parent, name)
        except AttributeError as e:
            raise AttributeError("Child' object has no attribute '%s'" % name)

p = Parent("Foo", 42)
c = Child(p, "parrot")
print(c.name, c.number, c.other)
p.name = "Bar"
print(c.name, c.number, c.other)

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