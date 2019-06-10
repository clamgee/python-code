from PyQt5.uic import loadUi #使用.ui介面模組
from PyQt5.QtCore import pyqtSlot,QDate,QTime,QDateTime,QTimer,Qt #插入資訊模組
from PyQt5.QtWidgets import QApplication,QDialog,QFileDialog,QMainWindow,QGraphicsScene #PyQt5介面與繪圖模組
from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg

class TMW(QMainWindow): #主視窗
    def __init__(self):
        super(TMW,self).__init__()
        loadUi(r'TMW.ui',self)
        self.scense=QGraphicsScene()
    def func(self):
        self.wedget=self.scense.addWidget()

if __name__ == "__main__":
    import sys
    App=QApplication(sys.argv)
    TMWindow=TMW()
    TMWindow.show()
    sys.exit(App.exec_())
