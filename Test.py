from PyQt5.uic import loadUi #使用.ui介面模組
from PyQt5.QtCore import pyqtSlot,QDate,QTime,QDateTime,QTimer,Qt #插入資訊模組
from PyQt5.QtWidgets import QApplication,QDialog,QFileDialog,QMainWindow,QGraphicsScene,QHeaderView,QTableWidgetItem #PyQt5介面與繪圖模組
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
        print(self.bestfive.loc[testlist,'close'])





if __name__ == "__main__":
    import sys
    App=QApplication(sys.argv)
    TMWindow=TMW()
    TMWindow.show()

    sys.exit(App.exec_())

# import pandas as pd
# import numpy as np
# import time
# a=pd.DataFrame(np.arange(27).reshape(27),columns=['close'])
# b=pd.DataFrame(np.arange(27).reshape(27),columns=['close'])

# # a['bid']=0
# # a['ask']=0
# a['close']=a['close'].map(lambda x:10500+13-(a['close'][a['close']==x].index[0]))
# dict_bid={'bid':{10499:28,10498:30,10497:22,10496:35,10495:18},'ask':{10500:22,10501:25}}
# # a.set_index('close')
# # a['bid']=a['close'].map(dict_bid['bid']).fillna(value=0).astype(int)
# # print('1: ',a['bid'])
# a['bid']=a.set_index(['close']).update(dict_bid)
# print('2: ',a['close'].tolist())
# a['ask']=a['close'].map(dict_bid['ask']).fillna(value=0).astype(int)
# # b['close']=b['close'].map(lambda x:10505+13-(b['close'][b['close']==x].index[0]))
# # start=time.time()
# # print((a['close']!=b['close']).index.tolist())
# # end=time.time()
# # print(round((end-start),6))
# # print(dict_bid['bid'])
# # total_dict={'bid':{10500:25,10501:22},'ask':{10503:27,10504:21}}
# # print(total_dict['bid'],total_dict['ask'])
# Change=False
# bidlist=a['bid'][a['bid']!=0].index.tolist()
# if a.loc[13,'close'] != 10500 :
#     Change=True
#     print(a.loc[13,'close'],Change)
# tmplist=[15,16,17,18,19]
# if Change is True :
#     bidlist=list(set(bidlist+tmplist))
#     print(bidlist)
