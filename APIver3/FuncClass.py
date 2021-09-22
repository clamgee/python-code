from PySide6.QtCore import QAbstractTableModel, QObject,Qt,QThread,Signal,Slot
import multiprocessing as mp
import time,os

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

# 建立存SKQuout 回傳Data的Queue
class DataQueue(object):
    def __init__(self,inputname,inputidx):
        self.queue = mp.Queue()
        self.name = inputname
        self.commodityIndex = inputidx

class TransformTiskQueue(QObject):
    list_signal = Signal(list)
    queue_signal = Signal(list)
    def __init__(self,inputname,inputidx):
        super(TransformTiskQueue,self).__init__()
        self.queue = mp.Queue()
        self.listqueue = mp.Queue()
        self.name = inputname
        self.commodityIndex = inputidx
        self.list_signal.connect(self.receivelist)
        self.queue_signal.connect(self.receivetick)
    @Slot(list)
    def receivelist(self,nlist):
        self.listqueue.put(nlist)
    @Slot(list)
    def receivetick(self,nlist):
        self.queue.put(nlist)

class MyProcess(mp.Process):  # 定義一個Class，繼承Process類
    def __init__(self, func,*args):
        super(MyProcess, self).__init__()  # 實踐父類初始化方法
        self.target = func
        self.args = (args[0],args[1],args[2])

    def run(self):  # 必須的，啟動進程方法
        self.target(self.args[0],self.args[1],self.args[2])
        print('子進程:', os.getpid(), os.getppid())

class Testthread(QThread):
    def __init__(self,inputname,inputindex,inputTuple):
        QThread.__init__(self)
        self.name = inputname
        self.idx = inputindex
        self.msgtuple = inputTuple

    def func(self):
        self.Func = self.idx + self.msgtuple[0] + self.msgtuple[1]

    def run(self):
        while True:
            self.func()
            print(self.Func,os.getppid(),os.getpid())
            time.sleep(2) 
