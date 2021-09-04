from PySide6.QtCore import QAbstractTableModel,Qt
import multiprocessing as mp
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

# 將QThread建立後放置Func內然後傳到SKprocess
def SKThreadmovetoprocess(func):
    func.start()
# 收到QThread後建立MultiProcessing 執行
def SKProcess(func):
    p1 = mp.Process(target=func)
    p1.start()
    p1.join()
