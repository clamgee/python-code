from PySide6.QtCore import QAbstractTableModel, QObject,Qt,QThread,Signal,Slot
import multiprocessing as mp
import time

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
class DataQueue(QObject):
    def __init__(self,inputname,inputidx):
        self.queue = mp.Queue()
        self.name = inputname
        self.commodityIndex = inputidx

class TickQueue(QObject):
    list_signal = Signal(list)
    queue_signal = Signal(list)
    def __init__(self,inputname,inputidx):
        self.queue = mp.Queue()
        self.nlist = []
        self.name = inputname
        self.commodityIndex = inputidx
        self.list_signal.connect(self.receivelist)
        self.queue_signal.connect(self.receivetick)
    @Slot(list)
    def receivelist(self,nlist):
        self.nlist = nlist
    @Slot(list)
    def receivetick(self,nlist):
        self.queue.put(nlist)

# 將QThread建立後放置Func內然後傳到SKprocess
class SubFunc(QObject):
    def __init__(self, parent=None):
        super(SubFunc,self).__init__(parent=parent)
        self.Main = parent
        
    def SKThreadmovetoprocess(self,func,*args):
        print('Thread: ',*args)
        self.Main.FutrueTickto12kThread = func(args[0],args[1],self)
        self.Main.FutrueTickto12kThread.start()
        i=1
        while self.Main.FutrueTickto12kThread.isRunning() != True :
            print('等待執行續建立!!',i)
            time.sleep(0.2)
            i+=1
        print('執行續:',self.Main.FutrueTickto12kThread.idealThreadCount())

    # 收到QThread後建立MultiProcessing 執行
    def SKProcess(self,*args):
        print('Process:',*args)
        self.p1 = mp.Process(target=self.SKThreadmovetoprocess,args=(args[0],args[1],args[2],))
        self.p1.start()
        # while p1.is_alive() != True:
        #     time.sleep(0.2)
        #     print('等待建立進程!!')
        # print('mp: ',p1.pid)
        self.p1.join()
    
