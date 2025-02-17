from PySide6.QtCore import QAbstractTableModel, QObject,Qt,QThread,Signal,Slot
import multiprocessing as mp
from multiprocessing.process import current_process
import time,os
import pandas as pd
import numpy as np
import typing
import KlineItem,GlobalVar
# QTableView 資料處理Model
class PandasModel(QAbstractTableModel):
    def __init__(self):
        QAbstractTableModel.__init__(self)

    def UpdateData(self, data):
        self._data = data
        self.layoutAboutToBeChanged.emit()  # 建立變更資料通知訊號發射
        self.dataChanged.emit(self.createIndex(0, 0),self.createIndex(self.rowCount(), self.columnCount()))  # 資料變更區域訊號發射
        self.layoutChanged.emit()  # 資料變更訊號發射

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
                # return str(self._data.at[index.row(), self._data.columns[index.column()]])
            elif role == Qt.TextAlignmentRole:
                return int(Qt.AlignCenter | Qt.AlignVCenter)
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

class Candle12KDrawThread(QThread):
    def __init__(self,inputFunc,inputSignal):
        super().__init__()
        self.Candle12KItem = inputFunc
        self.Candle12KItem_signal = inputSignal
        self.DFBuild_None = True
    def run(self):
        while True:
            nlist = GlobalVar.CandleItem12K_Event.get()
            if nlist is not None : #and GlobalVar.NS.nPtr12K == nlist[2]:
                while self.DFBuild_None: 
                    if nlist[3].shape[0] == 0 or len(nlist) < 4:
                        time.sleep(0.1)
                    else:
                        self.DFBuild_None = False
                self.Candle12KItem.set_data(nlist[3],nlist[:3])
                self.Candle12KItem_signal.emit()
            # GlobalVar.CandleItem12K_Event.wait()            
            # while self.DFBuild_None: 
            #     if GlobalVar.NS.df12K.shape[0] == 0 or len(GlobalVar.NS.list12K) < 3:
            #         time.sleep(0.1)
            #     else:
            #         self.DFBuild_None = False
            # if self.Candle12KItem.nPtr < GlobalVar.NS.list12K[2]:
            #     self.Candle12KItem.set_data(GlobalVar.NS.df12K,GlobalVar.NS.list12K)
            #     self.Candle12KItem_signal.emit()
            # GlobalVar.CandleItem12K_Event.clear() 

class CandleMinKDrawThread(QThread):
    def __init__(self,inputFunc,inputSignal):
        super().__init__()
        self.CandleMinKItem = inputFunc
        self.CandleMinKItem_signal = inputSignal
        self.DFBuild_None = True
    def run(self):
        while True:
            nlist = GlobalVar.CandleItemMinute_Event.get()
            if nlist is not None: #and GlobalVar.NS.nPtrMinK == nlist[2]:           
                while self.DFBuild_None:
                    if nlist[3].shape[0] == 0 or len(nlist) < 4:
                        time.sleep(0.1)
                    else:
                        self.DFBuild_None = False
                self.CandleMinKItem.set_data(nlist[3],nlist[:3])
                self.CandleMinKItem_signal.emit()
            else:
                pass

            # GlobalVar.CandleItemMinute_Event.wait()           
            # while self.DFBuild_None:
            #     if GlobalVar.NS.dfMinK.shape[0] ==0 or len(GlobalVar.NS.listMinK) <3:
            #         time.sleep(0.1)
            #     else:
            #         self.DFBuild_None = False
            # if self.CandleMinKItem.nPtr < GlobalVar.NS.listMinK[2]:
            #     self.CandleMinKItem.set_data(GlobalVar.NS.dfMinK,GlobalVar.NS.listMinK)
            #     self.CandleMinKItem_signal.emit()
            # GlobalVar.CandleItemMinute_Event.clear()  

class CandleMinKDealMinusDrawThread(QThread):
    def __init__(self,inputFunc,inputSignal):
        super().__init__()
        self.CandleMinuteDealMinusItem_signal = inputSignal
        self.CandleMinuteDealMinusItemFunc = inputFunc
        self.DFBuild_None = True
    def run(self):
        while True:
            nlist = GlobalVar.CandleMinuteDealMinus_Event.get()
            if nlist is not None and GlobalVar.NS.nPtrMinDealMinus == nlist[3]:
                while self.DFBuild_None:
                    if nlist[2].shape[0] == 0 or len(nlist) < 4 :
                        time.sleep(0.1)
                    else:
                        self.DFBuild_None = False
                self.CandleMinuteDealMinusItemFunc(nlist[2],nlist[:2])
                self.CandleMinuteDealMinusItem_signal.emit()
            else:
                pass

            # GlobalVar.CandleMinuteDealMinus_Event.wait()
            # while self.DFBuild_None:
            #     if GlobalVar.NS.dfMinK.shape[0] == 0 or len(GlobalVar.NS.listMinDealMinus) < 2 :
            #         time.sleep(0.1)
            #     else:
            #         self.DFBuild_None = False
            # self.CandleMinuteDealMinusItemFunc(GlobalVar.NS.dfMinK[['ndatetime','dealminus']],GlobalVar.NS.listMinDealMinus)
            # self.CandleMinuteDealMinusItem_signal.emit()
            # GlobalVar.CandleMinuteDealMinus_Event.clear()
            
class CandleMinKBigDrawThread(QThread):
    def __init__(self,inputFunc,inputSignal):
        super().__init__()
        self.CandleMinuteBigItem_signal = inputSignal
        self.CandleMinuteBigItemFunc = inputFunc
        self.DFBuild_None = True    
    def run(self):
        while True:
            nlist = GlobalVar.CandleMinuteBig_Event.get()
            if nlist is not None and GlobalVar.NS.nPtrMinBig == nlist[3]:
                while self.DFBuild_None:
                    if nlist[2].shape[0] == 0 or len(nlist) < 4 :
                        time.sleep(0.1)
                    else:
                        self.DFBuild_None = False 
                self.CandleMinuteBigItemFunc(nlist[2],nlist[:2])
                self.CandleMinuteBigItem_signal.emit()
            else:
                pass

            # GlobalVar.CandleMinuteBig_Event.wait()
            # while self.DFBuild_None:
            #     if GlobalVar.NS.dfMinK.shape[0] == 0 or len(GlobalVar.NS.listMinBig) < 2 :
            #         time.sleep(0.1)
            #     else:
            #         self.DFBuild_None = False 
            # self.CandleMinuteBigItemFunc(GlobalVar.NS.dfMinK[['ndatetime','big']],GlobalVar.NS.listMinBig)
            # self.CandleMinuteBigItem_signal.emit()
            # GlobalVar.CandleMinuteBig_Event.clear()  

class CandleMinKSmallDrawThread(QThread):
    def __init__(self,inputFunc,inputSignal):
        super().__init__()
        self.CandleMinuteSmallItem_signal = inputSignal
        self.CandleMinuteSmallItemFunc = inputFunc
        self.DFBuild_None = True
    def run(self):
        while True:
            nlist = GlobalVar.CandleMinuteSmall_Event.get()
            if nlist is not None and GlobalVar.NS.nPtrMinSmall == nlist[3]:
                while self.DFBuild_None:
                    if nlist[2].shape[0] == 0 or len(nlist) < 4 :
                        time.sleep(0.1) 
                    else:
                        self.DFBuild_None = False
                self.CandleMinuteSmallItemFunc(nlist[2],nlist[:2])
                self.CandleMinuteSmallItem_signal.emit()
            else:
                pass

            # GlobalVar.CandleMinuteSmall_Event.wait()
            # while self.DFBuild_None:
            #     if GlobalVar.NS.dfMinK.shape[0] == 0 or len(GlobalVar.NS.listMinSmall) < 2 :
            #         time.sleep(0.1) 
            #     else:
            #         self.DFBuild_None = False
            # self.CandleMinuteSmallItemFunc(GlobalVar.NS.dfMinK[['ndatetime','small']],GlobalVar.NS.listMinSmall)
            # self.CandleMinuteSmallItem_signal.emit()
            # GlobalVar.CandleMinuteSmall_Event.clear() 

class MyProcess(mp.Process):  # 定義一個Class，繼承Process類
    def __init__(self, func,*args):
        super(MyProcess, self).__init__()  # 實踐父類初始化方法
        self.target = func
        self.args = (args[0],args[1],args[2])

    def run(self):  # 必須的，啟動進程方法
        self.Thd = self.target(self.args[0],self.args[1],self.args[2]) #將QThread丟進來執行
        self.Thd.start()
        print(self.Thd.name,current_process().name)

# class DomDataProcess(mp.Process):
#     def __init__(self,*args):
#         super(DomDataProcess,self).__init__()
#         self.__Event = args[0]
#         self.__Queue = args[1]
#         self.__Domdf = args[2]
#         self.df = pd.DataFrame(np.arange(24).reshape(6,4), columns=['買量','買價','賣價','賣量']) #多空力道 DataFrame
#         self.df[['買量','買價','賣價','賣量']]=self.df[['買量','買價','賣價','賣量']].astype(str)
#         self.df.at[5,'買價']=str('')
#         self.df.at[5,'賣價']=str('')
#         self.__Domdf.Domdf = self.df
        
#     def run(self):
#         while True:
#             ndict = self.__Queue.get()
#             if ndict!=None:
#                 for (t, x) in self.df.loc[0:4,['買量','買價','賣價','賣量']].iterrows():
#                     self.df.at[t,'買量']=str(ndict['買量'][t])
#                     self.df.at[t,'買價']=str(ndict['買價'][t])
#                     self.df.at[t,'賣價']=str(ndict['賣價'][t])
#                     self.df.at[t,'賣量']=str(ndict['賣量'][t])
#                 bidQty = ndict['買量'].values()
#                 askQty = ndict['賣量'].values()
#                 self.df.at[5,'買量']=str(int(sum(bidQty)))
#                 self.df.at[5,'賣量']=str(int(sum(askQty)))
#                 self.__Domdf.Domdf = self.df
#                 if self.__Event.is_set() is False :
#                     self.__Event.set()

class DomTableUpdateThread(QThread):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self._parent = parent
        
    def run(self):
        while True:
            nlist=GlobalVar.DomDataQueue.get()
            if nlist is not None:
                n=0
                for key in self._parent.SKCommodity.Domdict:
                    for i in range(5):
                        self._parent.SKCommodity.Domdict[key][i].setText(str(nlist[n]))
                        n+=1
                self._parent.SKCommodity.Domdict[0][5].setText(str(int(sum(nlist[0:5]))))
                self._parent.SKCommodity.Domdict[3][5].setText(str(int(sum(nlist[15:20]))))

class MPTableBigSmallThread(QThread):
    def __init__(self, parent) -> None:
        super().__init__(parent=parent)
        self._parent = parent
    def run(self):
        while True:
            nlist = GlobalVar.MP_Event.get()
            if nlist is not None:
                MP_dict = {'ComCont':{0:nlist[1],1:nlist[2],2:int(nlist[2]-nlist[1])},
                            'ComQty':{0:nlist[3],1:nlist[4],2:int(nlist[3]-nlist[4])},
                            'DealCont':{0:nlist[5],1:nlist[6],2:int(nlist[6]-nlist[5])}}
                for key in MP_dict:
                    i = 0
                    for i in range(3):
                        self._parent.SKCommodity.MPower.at[i,key].setText(str(MP_dict[key][i]))
                        if i == 2:
                            if MP_dict[key][i] > 0:
                                self._parent.SKCommodity.MPower.at[i,key].setBackground(Qt.red)
                                self._parent.SKCommodity.MPower.at[i,key].setForeground(Qt.white)
                            else:
                                self._parent.SKCommodity.MPower.at[i,key].setBackground(Qt.green)
                                self._parent.SKCommodity.MPower.at[i,key].setForeground(Qt.black)
            

class MPTablePowerThread(QThread):
    def __init__(self, parent) -> None:
        super().__init__(parent=parent)
        self._parent = parent
    def run(self):
        while True:
            nlist = GlobalVar.PowerQueue.get()
            if nlist != None:
                self._parent.SKCommodity.MPower.at[0,'DealQty'].setText(str(nlist[0]))
                self._parent.SKCommodity.MPower.at[1,'DealQty'].setText(str(nlist[1]))
                self._parent.SKCommodity.MPower.at[2,'DealQty'].setText(str(nlist[0]+nlist[1]))
                self._parent.SKCommodity.MPower.at[3,'DealQty'].setText(str(nlist[0]-nlist[1]))
                if nlist[0]+nlist[1] >= 0:
                    self._parent.SKCommodity.MPower.at[2,'DealQty'].setBackground(Qt.red)
                    self._parent.SKCommodity.MPower.at[2,'DealQty'].setForeground(Qt.white)                    
                else:
                    self._parent.SKCommodity.MPower.at[2,'DealQty'].setBackground(Qt.green)
                    self._parent.SKCommodity.MPower.at[2,'DealQty'].setForeground(Qt.black)
