from PySide6.QtCore import QAbstractTableModel, QObject,Qt,QThread,Signal,Slot
import multiprocessing as mp
import time,os
import typing
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
    def __init__(self,inputQueue,inputdf,parent: typing.Optional[QObject] = ...) -> None:
        super().__init__(parent=parent)
        self.df = None
        self.__CandleItem12K_Queue = inputQueue
        self.__Candledf12K = inputdf
        print('in Thread id: ',id(self.__CandleItem12K_Queue),id(self.__Candledf12K))

    def run(self):
        while True:
            if self.__CandleItem12K_Queue.qsize() != 0:
                a = self.__CandleItem12K_Queue.get()
                print('nPtr: ',a)
                self.df = self.__Candledf12K.df12K
                if self.df.shape[0]>0: 
                    print(self.df.tail(1))
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
        print('子進程:', os.getpid(), os.getppid())

