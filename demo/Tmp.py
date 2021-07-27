from multiprocessing import Process, Queue, current_process
# from PyQt5 import QThread,pyqtSignal,QMainWindow
from PyQt5.QtCore import pyqtSlot, QDate, QTime, QDateTime, QTimer, Qt, QThread, pyqtSignal, \
    QAbstractTableModel  # 插入資訊模組
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMainWindow, QGraphicsScene, QHeaderView, \
    QTableWidgetItem, QMessageBox  # PyQt5介面與繪圖模組
from PyQt5 import QtCore, QtGui, QtWidgets
import time

class communicate_Thread(QThread):

    communicate_singal = pyqtSignal(int)
    exit_signal = pyqtSignal()

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
    def setData(self,q):
        self.q = q

    def run(self):
       while self.q.qsize()>0:
           res=self.q.get()
           print('Thread',res)

class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.q = Queue()
        self.xxx=communicate_Thread()
        yyyprocess(self.xxx,self.q)


    def dosomething(self,res):
        self.count+=res
        print(self.count,res)

def yyyprocess(*args):
    print(args)
    # Process(target=args[0].setData,args=(args[1],)).start()

            

if __name__ == '__main__':
    import sys
    A = QApplication(sys.argv)
    QMain = App()
    QMain.show()
    # QMain.yyy.start()
    # QMain.yyy.join()
    sys.exit(A.exec_())
