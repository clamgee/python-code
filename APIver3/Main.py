import sys
import os
from PySide6.QtCore import QObject, Signal,Slot,QTime,Qt,QThread,QAbstractTableModel,QFile
from PySide6.QtWidgets import QMainWindow,QApplication,QTableWidgetItem,QMessageBox,QHeaderView
from PySide6.QtGui import QAction
from PySide6 import QtCore
import pyqtgraph as pg
# from PySide6.QtUiTools import QUiLoader
# from UI.Uiload import UiLoader
from UI.ui_MainWindow import Ui_CapitalAPI
import FuncUI

class SKMainWindow(QMainWindow):
    def __init__(self,parent=None):
        super(SKMainWindow, self).__init__(parent)
        self.MainUi = Ui_CapitalAPI()
        self.MainUi.setupUi(self)
        self.showMaximized()
        # 介面導入
        self.SKLoginUI()  # 登入介面
        # ManuBar連結
        self.MainUi.actionLogin.triggered.connect(self.Login.ui.show)  # 登入介面連結
    
    def SKLoginUI(self):
        self.Login = FuncUI.LoginDialog()
        self.Login.ui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 設定最上層
        self.Login.ui.setWindowModality(QtCore.Qt.ApplicationModal)  # 設定須先完成對話框，GUI設定無效
        self.Login.ui.show()
        self.Login.ui.LoginConfirmbtn.accepted.connect(self.LoginFuncAccept)
        self.Login.ui.LoginConfirmbtn.rejected.connect(self.LoginFuncReject)
    
    def LoginFuncAccept(self):
        print('登入')
    def LoginFuncReject(self):
        print('清除')



if __name__=='__main__':
    SKApp = QApplication(sys.argv)
    SKMain = SKMainWindow()
    SKMain.show()
    sys.exit(SKApp.exec_())
