# from PyQt5.uic import loadUi #使用.ui介面模組
# from PyQt5.QtCore import pyqtSlot,QDate,QTime,QDateTime,QTimer,Qt #插入資訊模組
# from PyQt5.QtWidgets import QApplication,QDialog,QFileDialog,QMainWindow,QGraphicsScene,QHeaderView,QTableWidgetItem #PyQt5介面與繪圖模組
# from PyQt5 import QtCore, QtGui, QtWidgets
# import pyqtgraph as pg

# class TMW(QMainWindow): #主視窗
#     def __init__(self):
#         super(TMW,self).__init__()
#         loadUi(r'TMW.ui',self)
#         self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
#         a = QTableWidgetItem('1')
#         self.tableWidget.setItem(0,1,a)

# if __name__ == "__main__":
#     import sys
#     App=QApplication(sys.argv)
#     TMWindow=TMW()
#     TMWindow.show()
#     sys.exit(App.exec_())


import pandas as pd
import numpy as np
a=pd.DataFrame(np.arange(27).reshape(27),columns=['close'])
a['bid']=''
a['ask']=''
a['close']=a['close'].map(lambda x:10500+13-(a['close'][a['close']==x].index[0]))
dict_bid={10499:28,10498:30,10497:22,10496:35,10495:18}
a.set_index('close')
a['bid']=a['close'].map(dict_bid).fillna(value=0).astype(int)

print(a['close'])
