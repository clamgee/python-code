# 系統套件
import sys
# import os
# # 使用PySide6套件
from PySide6.QtUiTools import QUiLoader #使用 .LoginUI介面模組
from PySide6.QtWidgets import QApplication,QDialog #PySide6介面控制模組
from PySide6 import QtCore, QtGui, QtWidgets
import json
import re

class LoginDialog(QtCore.QObject):
    def __init__(self):
        UiFile = QtCore.QFile('UI/Login.ui')
        Loader = QUiLoader()
        UiFile.open(QtCore.QFile.ReadOnly)
        self.ui=Loader.load(UiFile)
        UiFile.close()
        self.ui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 設定最上層
        self.ui.setWindowModality(QtCore.Qt.ApplicationModal)  # 設定須先完成對話框，其他介面設定無效
        if self.ui.IDPWCheck.checkState()==2:
            with open("IDPW.json",mode="r",encoding="utf-8") as file:
                data = json.load(file)
            self.ui.LoginID.setText(data["ID"])
            self.ui.LoginPW.setText(data["PW"])

class MessageDialog(QtCore.QObject):
    def __init__(self,gname):
        UiFile = QtCore.QFile('UI/Message.ui')
        Loader = QUiLoader()
        UiFile.open(QtCore.QFile.ReadOnly)
        self.ui = Loader.load(UiFile)
        UiFile.close()
        self.ui.setWindowTitle(gname)
        self.ui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 設定最上層
        # 顯示最大最小化關閉按鍵
        self.ui.setWindowFlags(QtCore.Qt.WindowMinMaxButtonsHint|QtCore.Qt.WindowCloseButtonHint)

class CommodityForm(QtCore.QObject):
    Commodity_comboBox_signal = QtCore.Signal(int,str)
    def __init__(self):
        super(CommodityForm, self).__init__()
        self.count = 0
        UiFile = QtCore.QFile('UI/Commodity.ui')
        Loader = QUiLoader()
        UiFile.open(QtCore.QFile.ReadOnly)
        self.ui = Loader.load(UiFile)
        UiFile.close()
        self.ui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 設定最上層
        # 顯示最大最小化關閉按鍵
        self.ui.setWindowFlags(QtCore.Qt.WindowMinMaxButtonsHint|QtCore.Qt.WindowCloseButtonHint)
        self.Commodity_comboBox_signal.connect(self.Commodity_comboBox_recive)
    @QtCore.Slot(int,str)
    def Commodity_comboBox_recive(self,sMarketNo,bstrStockData):
        Line = bstrStockData.split(';')
        self.count+=1
        ListCommodity=[]
        p = re.compile('TX\w+|TF\w+|TE\w+')
        c = re.compile('##\w+')
        for row in Line:
            rowstuff = row.split(',')
            for row in rowstuff:
                row.replace(' ','')
            if c.findall(rowstuff[0]):
                break
            elif p.match(rowstuff[0]):
                ListCommodity.append(rowstuff[0]+','+rowstuff[1])
        
        print('sMarketNo: %s',sMarketNo)
        # print(ListCommodity)
        self.ui.Commodity_comboBox.addItems(ListCommodity)
        if len(ListCommodity)==0:
            pass
        elif 'TX00,台指近' in ListCommodity:
            self.ui.Commodity_comboBox.setCurrentText('TX00,台指近')
        else:
            print('找不到 TX00')
        print(self.count,'次')
        # self.SKMessage.ui.textBrowser.append('找不到 TX00')





# if __name__ == "__main__":
#     FuncUIApp = QApplication(sys.argv)
#     SKLogin = LoginDialog()
#     SKLogin.ui.show()
#     SKMessage = MessageDialog()
#     SKMessage.ui.show()
#     sys.exit(FuncUIApp.exec_())