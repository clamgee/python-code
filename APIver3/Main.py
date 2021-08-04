import sys
from PySide6.QtCore import Signal,Slot,QTime,Qt,QThread,QAbstractTableModel
from PySide6.QtWidgets import QMainWindow,QApplication,QTableWidgetItem,QMessageBox,QHeaderView
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QAction
import pyqtgraph as pg
from UI.ui_MainWindow import Ui_CapitalAPI
class SKMainWindow(QMainWindow):  # 主視窗
    def __init__(self):
        super(SKMainWindow, self).__init__()
        self.ui=Ui_CapitalAPI()
        self.ui.setupUi(self)

if __name__=='__main__':
    SKApp = QApplication(sys.argv)
    SKMain = SKMainWindow()
    SKMain.show()
    sys.exit(SKApp.exec())
