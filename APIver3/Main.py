import sys
import os
from PySide6.QtCore import QObject, Signal,Slot,QTime,Qt,QThread,QAbstractTableModel,QFile
from PySide6.QtWidgets import QMainWindow,QApplication,QTableWidgetItem,QMessageBox,QHeaderView
from PySide6.QtGui import QAction
import pyqtgraph as pg
from PySide6.QtUiTools import QUiLoader
# from UI.Uiload import UiLoader
# from UI.ui_MainWindow import Ui_CapitalAPI
# 程式路徑
SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
# print(os.path.join(SCRIPT_DIRECTORY, 'UI\MainWindow.ui'))

class SKMainWindow(QObject):
    def __init__(self,MainUIFile,parent=None):
        super(SKMainWindow, self).__init__(parent)
        # QMainWindow.__init__(self, parent)
        self.MainWindowUiFile = QFile(os.path.join(SCRIPT_DIRECTORY, MainUIFile))
        self.MainWindowUiFile.open(QFile.ReadOnly)
        self.Loader=QUiLoader()
        self.MainUi=self.Loader.load(self.MainWindowUiFile)
        # self.Loader.load('UI\MainWindow.ui')
        self.MainWindowUiFile.close()
        self.MainUi.show()
        self.MainUi.showMaximized()


if __name__=='__main__':
    SKApp = QApplication(sys.argv)
    SKMain = SKMainWindow('UI\MainWindow.ui')
    sys.exit(SKApp.exec_())
