import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QAction

class GUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(800,600)
        self.setWindowTitle('Clam 視窗')
        self.statusBar().showMessage('內文狀態')
        #建立一個Menu欄
        self.menu = self.menuBar()
        #建立一個Menu
        self.file_menu=self.menu.addMenu('文件')
        #建立一個行為
        self.new_action = QAction('新文件',self)
        #添加一個行為到Menu
        self.file_menu.addAction(self.new_action)
        #更新狀態欄位
        self.new_action.setStatusTip('新的文件')



if __name__=='__main__':
    app=QApplication(sys.argv)
    gui=GUi()
    gui.show()
    sys.exit(app.exec_())