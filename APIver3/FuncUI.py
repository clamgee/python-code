import sys,os,gc
sys.path.append("..")
# # 使用PySide6套件
from PySide6.QtUiTools import QUiLoader #使用 .LoginUI介面模組
from PySide6.QtWidgets import QApplication,QHeaderView,QTableWidgetItem #PySide6介面控制模組
from PySide6 import QtCore, QtGui, QtWidgets
import json
import re
import GlobalVar
import pandas as pd
import numpy as np

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
    Message_signal = QtCore.Signal(str)
    def __init__(self,gname):
        super(MessageDialog, self).__init__()
        UiFile = QtCore.QFile('UI/Message.ui')
        Loader = QUiLoader()
        UiFile.open(QtCore.QFile.ReadOnly)
        self.ui = Loader.load(UiFile)
        UiFile.close()
        self.ui.setWindowTitle(gname)
        self.ui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 設定最上層
        # 顯示最大最小化關閉按鍵
        self.ui.setWindowFlags(QtCore.Qt.WindowMinMaxButtonsHint|QtCore.Qt.WindowCloseButtonHint)
        #訊號連結
        self.Message_signal.connect(self.inserttextfunc)
    @QtCore.Slot(str)
    def inserttextfunc(self,strMsg):
        self.ui.textBrowser.append(strMsg)

class CommodityForm(QtCore.QObject):
    Commodity_comboBox_signal = QtCore.Signal(int,str)
    def __init__(self,parent):
        super(CommodityForm, self).__init__(parent)
        self.parent = parent
        self.count = 0
        UiFile = QtCore.QFile('UI/Commodity.ui')
        Loader = QUiLoader()
        UiFile.open(QtCore.QFile.ReadOnly)
        self.ui = Loader.load(UiFile)
        UiFile.close()
        # self.ui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 設定最上層
        # 顯示最大最小化關閉按鍵
        self.ui.setWindowFlags(QtCore.Qt.WindowMinMaxButtonsHint|QtCore.Qt.WindowCloseButtonHint)
        self.ui.DomTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.DomTable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.Commodity_comboBox_signal.connect(self.Commodity_comboBox_recive)
        self.MPowerTalbeUI()
        self.DomTalbeUI()
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
        
        if len(ListCommodity)==0:
            pass
        else:
            self.ui.Commodity_comboBox.addItems(ListCommodity)
            if 'TX00,台指近' in ListCommodity:
                self.ui.Commodity_comboBox.setCurrentText('TX00,台指近')
            elif gc.is_tracked(self.parent) and self.ui.Commodity_comboBox.currentText()!='TX00,台指近':
                print('找不到 TX00')
                self.parent.Message_signal.emit('找不到 TX00')
            else:
                try:
                    pass
                except AttributeError as e:
                    raise AttributeError("商品清單功能Bug 市場編號為: %d" %(sMarketNo),e)

    def MPowerTalbeUI(self):
        self.ui.MPTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.MPTable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.MPower = pd.DataFrame(np.arange(16).reshape(4,4), columns=['ComQty','ComCont','DealCont','DealQty'])
        font = QtGui.QFont()
        font.setBold(True)
        i=0
        while i < 4 :
            j=0
            while j < 4:
                self.MPower.at[i,self.MPower.columns[j]] = QTableWidgetItem('')
                self.MPower.at[i,self.MPower.columns[j]].setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                if i == 2:
                    self.MPower.at[i,self.MPower.columns[j]].setFont(font)
                self.ui.MPTable.setItem(i, j, self.MPower.at[i,self.MPower.columns[j]])
                j+=1
            i+=1

    def DomTalbeUI(self):
        self.ui.DomTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.DomTable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.Domdf = pd.DataFrame(np.arange(24).reshape(6,4), columns=['買量','買價','賣價','賣量'])
        self.Domdict = {}
        
        for i in range(4):
            self.Domdict.setdefault(i,{})
            for j in range(6):
                self.Domdict[i][j]=QTableWidgetItem('')
                self.Domdict[i][j].setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                # self.Domdf.at[i,self.Domdf.columns[j]] = QTableWidgetItem('')
                # self.Domdf.at[i,self.Domdf.columns[j]].setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                # self.ui.DomTable.setItem(i, j, self.Domdf.at[i,self.Domdf.columns[j]])
                self.ui.DomTable.setItem(j, i, self.Domdict[i][j])

# if __name__ == "__main__":
#     FuncUIApp = QApplication(sys.argv)
#     SKLogin = LoginDialog()
#     SKLogin.ui.show()
#     SKMessage = MessageDialog()
#     SKMessage.ui.show()
#     sys.exit(FuncUIApp.exec_())