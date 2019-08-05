from PyQt5.uic import loadUi #使用.ui介面模組
from PyQt5.QtCore import pyqtSlot,QDate,QTime,QDateTime,QTimer,Qt #插入資訊模組
from PyQt5.QtWidgets import QApplication,QDialog,QFileDialog,QMainWindow,QGraphicsScene,QHeaderView,QTableWidgetItem,QStyleFactory #PyQt5介面與繪圖模組
from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import pandas as pd
import numpy as np
import time

class TMW(QMainWindow): #主視窗
    def __init__(self):
        super(TMW,self).__init__()
        loadUi(r'TMW.ui',self)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.pushButton.clicked.connect(self.tableupdate)
        self.trade_act=0
        self.bid_btn.clicked.connect(self.bidfunc)
        self.ask_btn.clicked.connect(self.askfunc)
        QApplication.setStyle(QStyleFactory.create('cleanlooks'))
    
    def bidfunc(self):
        self.bid_btn.setStyleSheet('color: white;\n''background-color: red;')
        if self.bid_btn.isChecked():
            self.ask_btn.setChecked(False)
            self.ask_btn.setStyleSheet('background-color: ')            
        else:
            self.bid_btn.setStyleSheet('background-color: ;''color:')
    
    def askfunc(self):
        self.ask_btn.setStyleSheet('background-color: green')
        if self.ask_btn.isChecked():
            self.bid_btn.setChecked(False)
            self.bid_btn.setStyleSheet('background-color: ;''color:')
        else :
            self.ask_btn.setStyleSheet('background-color: ')


    def tableupdate(self):
        self.bestfive=pd.DataFrame(np.arange(27).reshape(27),columns=['close'])
        self.bestfive['bid']=0
        self.bestfive['ask']=0
        self.bestfive=self.bestfive[['close','bid','ask']].astype(int)
        self.bestfive['closeTBitem']=''
        self.bestfive['bidTBitem']=''
        self.bestfive['askTBitem']=''
        i=0
        while i < 27 :
            self.bestfive.loc[i,'closeTBitem']=QTableWidgetItem('')
            self.tableWidget.setItem(i,1,self.bestfive.loc[i,'closeTBitem'])
            self.bestfive.loc[i,'bidTBitem']=QTableWidgetItem('')
            self.tableWidget.setItem(i,0,self.bestfive.loc[i,'bidTBitem'])
            self.bestfive.loc[i,'askTBitem']=QTableWidgetItem('')
            self.tableWidget.setItem(i,2,self.bestfive.loc[i,'askTBitem'])
            self.bestfive.loc[i,'closeTBitem'].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.bestfive.loc[i,'bidTBitem'].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.bestfive.loc[i,'askTBitem'].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            i+=1
        self.bestfive.loc[13,'closeTBitem'].setBackground(Qt.yellow)
        self.bestfive.loc[13,'bidTBitem'].setBackground(Qt.yellow)
        self.bestfive.loc[13,'askTBitem'].setBackground(Qt.yellow)
        self.bestfive['close']=self.bestfive['close'].map(lambda x : 10500+13-(self.bestfive['close'][self.bestfive['close']==x].index[0]))
        self.bestfive['closeTBitem'].map(lambda x:x.setText(str(self.bestfive.loc[self.bestfive['closeTBitem'][self.bestfive['closeTBitem']==x].index[0],'close'])))
        print(self.bestfive.query('close==10500').index[0])
        self.bidlist=[]






if __name__ == "__main__":
    import sys
    App=QApplication(sys.argv)
    TMWindow=TMW()
    TMWindow.show()

    sys.exit(App.exec_())

