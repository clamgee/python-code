import sys
import os
from PySide6.QtCore import Signal,Slot,QTime,Qt,QThread,QAbstractTableModel,QFile
from PySide6.QtWidgets import QMainWindow,QApplication,QTableWidgetItem,QMessageBox,QHeaderView
from PySide6.QtGui import QAction
import pyqtgraph as pg
from UI.Uiload import UiLoader
from UI.ui_MainWindow import Ui_CapitalAPI
# 程式路徑
SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
# print(os.path.join(SCRIPT_DIRECTORY, 'UI\MainWindow.ui'))

class SKMainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.MainUi=Ui_CapitalAPI()
        self.MainUi.setupUi(self)
        # self.MainWindowUiFile = QFile(os.path.join(SCRIPT_DIRECTORY, 'UI\MainWindow.ui'))
        # # self.MainWindowUiFile.open(QFile.ReadOnly)
        # UiLoader(self.MainWindowUiFile, self)
        # # self.MainWindowUiFile.close()


if __name__=='__main__':
    SKApp = QApplication(sys.argv)
    SKMain = SKMainWindow()
    SKMain.show()
    sys.exit(SKApp.exec_())
