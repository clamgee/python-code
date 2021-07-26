from multiprocessing import Process, Queue, current_process
# from PyQt5 import QThread,pyqtSignal,QMainWindow
from PyQt5.QtCore import pyqtSlot, QDate, QTime, QDateTime, QTimer, Qt, QThread, pyqtSignal, \
    QAbstractTableModel  # 插入資訊模組
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMainWindow, QGraphicsScene, QHeaderView, \
    QTableWidgetItem, QMessageBox  # PyQt5介面與繪圖模組
from PyQt5 import QtCore, QtGui, QtWidgets


class communicate_Thread(QThread):

    communicate_singal = pyqtSignal(str)
    exit_signal = pyqtSignal()

    def __init__(self, q, parent=None,):
        QThread.__init__(self, parent)
        self.q = q

    def run(self):
        # global running
        while True:
            text = self.q.get(True)
            self.communicate_singal.emit(text)

        self.exit_signal.emit()

class App(QMainWindow):
    def __init__(self):
        self.q = Queue()
        self.xxx = communicate_Thread(self.q)
        self.xxx.communicate_singal.connect(self.do_something)
        self.xxx.start()
        
        self.yyy_process = Process(target=self.yyyprocess, args=(self.q,))
        self.yyy_process.start()
        
    def yyyprocess(self,q):
        res = []
        i = 0
        a = current_process().name
        for i in range(10):
            res.append([i,a])
            q.put(res)

if __name__ == '__main__':
    QMain = App()