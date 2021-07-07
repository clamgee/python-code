# import datetime
import time
# print(time.localtime(time.time()).tm_hour)
import pyqtgraph.examples
import sys
from PyQt5 import QtGui, QtCore

lista = ['r1c1', 'r1c2', 'r1c3']
listb = ['r2c1', 'r2c2', 'r1c3']
listc = ['r3c1', 'r3c2', 'r3c3']
mystruct = {'row1':lista, 'row2':listb, 'row3':listc}

def change():
    i=0
    for i in range(10):
        time.sleep(1000)
        n = 0
        for key in mystruct:
            m = 0
            for item in mystruct[key]:
                item=str(m+n+i)
                print(item)
                m += 1
            n += 1
        i+=1

class MyTable(QtGui.QTableWidget):
    def __init__(self, thestruct, *args):
        QtGui.QTableWidget.__init__(self, *args)
        self.data = thestruct
        n = 0
        for key in self.data:
            m = 0
            for item in self.data[key]:
                newitem = QtGui.QTableWidgetItem(item)
                self.setItem(m, n, newitem)
                m += 1
            n += 1
        self.itemSelectionChanged.connect(self.print_row)

    def print_row(self):
        items = self.selectedItems()
        print(str(items[0].text()))

def main(args):
    app = QtGui.QApplication(args)
    table = MyTable(mystruct, 3, 3)
    table.show()

    change()
    sys.exit(app.exec_())

if __name__=="__main__":
    main(sys.argv)