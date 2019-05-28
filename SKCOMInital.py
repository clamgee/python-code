import sys
import os
import shutil
import comtypes.client as cc
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QDialog,QFileDialog

class UpdateSKCOM(QDialog):
    def __init__(self):
        super(UpdateSKCOM,self).__init__()
        loadUi(r'APIver1/UI/SKCOMupdate.ui',self)
        self.path=None
        self.found=False
        self.dllpath=None
        try:
            import comtypes.gen.SKCOMLib as sk
            self.found=True
            self.path=sk.__file__
            a=self.path.index('_')-1
            self.path=self.path[:a]
            self.label3.setText(self.path)
            # print(self.path)
        except ImportError:
            self.found=False
            self.label2.setText('未安裝')
            self.label3.setText('')
        self.openSKCOMfilebtn.clicked.connect(self.openSKCOMfile_click)
        self.UpdateComfirm.accepted.connect(self.ok_click)
        self.UpdateComfirm.rejected.connect(self.close)

    def openSKCOMfile_click(self):
        self.dllpath=QFileDialog.getOpenFileName(self,'選擇SKCOM.dll檔案')
        self.dllpath=(str(self.dllpath[0]).replace('/','\\'))
        self.SKCOMfilepath.setText(self.dllpath)

    def ok_click(self):
        if self.found:
            shutil.rmtree(self.path)
            os.mkdir(self.path)
        try:
            cc.GetModule(self.dllpath)
            self.label2.setText('已更新!!')    
        except Exception as e:
            self.label2.setText(e)
            pass

if __name__ == '__main__':
    App=QApplication(sys.argv)
    Widget=UpdateSKCOM()
    Widget.show()
    sys.exit(App.exec_())

