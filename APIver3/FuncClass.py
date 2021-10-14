from PySide6.QtCore import QAbstractTableModel, QObject,Qt,QThread,Signal,Slot
import multiprocessing as mp
import time,os
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
                return str(self._data.at[index.row(), self._data.columns[index.column()]])
            elif role == Qt.TextAlignmentRole:
                return int(Qt.AlignCenter | Qt.AlignVCenter)
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

class Candle12KDrawThread(QThread):
    def __init__(self,inputEvent,inputdf,inputSignal):
        super().__init__()
        self.__CandleItem12K_Event = inputEvent
        self.__Candledf12K = inputdf
        self.Candle12KItem_signal = inputSignal
        self.creatItembool_None = True
    def run(self):
        while True:
            nlist = self.__CandleItem12K_Event.get()
            if nlist is not None: 
                if self.creatItembool_None:
                    while self.__Candledf12K.df12K.shape[0]==0:
                        time.sleep(0.02)
                    self.CandleItem12K = KlineItem.CandleItem(self.__Candledf12K.df12K)
                    self.Candle12KItem_signal.emit(self.CandleItem12K)
                    self.creatItembool_None = False
                else:
                    if GlobalVar.NS.list12K[0] != self.CandleItem12K.lastidx or GlobalVar.NS.list12K[1] != self.CandleItem12K.close:
                        self.CandleItem12K.set_data(self.__Candledf12K.df12K,GlobalVar.NS.list12K)
                        self.Candle12KItem_signal.emit(self.CandleItem12K)
                    else:
                        pass

class CandleMinKDrawThread(QThread):
    def __init__(self,inputEvent,inputdf,inputSignal):
        super().__init__()
        self.__CandleItemMinK_Event = inputEvent
        self.__CandledfMinK = inputdf
        self.CandleMinKItem_signal = inputSignal
        self.creatItembool_None = True
    def run(self):
        while True:
            nlist = self.__CandleItemMinK_Event.get()
            if nlist is not None:
                if self.creatItembool_None:
                    while self.__CandledfMinK.dfMinK.shape[0]==0:
                        time.sleep(0.02)
                    self.CandleItemMinK = KlineItem.CandleItem(self.__CandledfMinK.dfMinK)
                    self.CandleMinKItem_signal.emit(self.CandleItemMinK)
                    self.creatItembool_None = False
                else:
                    if self.__CandledfMinK.listMinK[0] != self.CandleItemMinK.lastidx or self.__CandledfMinK.listMinK[1] != self.CandleItemMinK.close:
                        self.CandleItemMinK.set_data(self.__CandledfMinK.dfMinK,self.__CandledfMinK.listMinK)
                        self.CandleMinKItem_signal.emit(self.CandleItemMinK)
                    else:
                        pass

class CandleMinKDealMinusDrawThread(QThread):
    def __init__(self,inputSignal):
        super().__init__()
        self.CandleMinuteDealMinusItem_signal = inputSignal
        self.setItembool_None = True
    def run(self):
        while True:
            nlist = GlobalVar.CandleMinuteDealMinus_Event.get()
            if nlist is not None:
                if self.setItembool_None:
                    while GlobalVar.NS.dfMinK.shape[0]==0:
                        time.sleep(0.02)
                    self.CandleItemMinuteDealMinus = KlineItem.BarItem()
                    self.CandleItemMinuteDealMinus.set_data(GlobalVar.NS.dfMinK[['ndatetime','dealminus']],GlobalVar.NS.listMinDealMinus)
                    self.CandleMinuteDealMinusItem_signal.emit(self.CandleItemMinuteDealMinus)
                    self.setItembool_None = False
                else:
                    if GlobalVar.NS.listMinDealMinus[0] != self.CandleItemMinuteDealMinus.lastidx or GlobalVar.NS.listMinDealMinus[1] != self.CandleItemMinuteDealMinus.close:
                        self.CandleItemMinuteDealMinus.set_data(GlobalVar.NS.dfMinK[['ndatetime','dealminus']],GlobalVar.NS.listMinDealMinus)
                        self.CandleMinuteDealMinusItem_signal.emit(self.CandleItemMinuteDealMinus)
                    else:
                        pass

class MyProcess(mp.Process):  # 定義一個Class，繼承Process類
    def __init__(self, func,*args):
        super(MyProcess, self).__init__()  # 實踐父類初始化方法
        self.target = func
        self.args = (args[0],args[1],args[2])

    def run(self):  # 必須的，啟動進程方法
        self.Thd = self.target(self.args[0],self.args[1],self.args[2])
        self.Thd.run()

