# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CapitalAPI(object):
    def setupUi(self, CapitalAPI):
        CapitalAPI.setObjectName("CapitalAPI")
        CapitalAPI.setWindowModality(QtCore.Qt.WindowModal)
        CapitalAPI.resize(1024, 576)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        CapitalAPI.setFont(font)
        self.centralwidget = QtWidgets.QWidget(CapitalAPI)
        self.centralwidget.setObjectName("centralwidget")
        CapitalAPI.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(CapitalAPI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        CapitalAPI.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(CapitalAPI)
        self.statusbar.setObjectName("statusbar")
        CapitalAPI.setStatusBar(self.statusbar)
        self.actionLogin = QtWidgets.QAction(CapitalAPI)
        self.actionLogin.setObjectName("actionLogin")
        self.actionLogin.triggered
        self.menu_3.addAction(self.actionLogin)
        self.menu_3.addSeparator()
        self.menu_4.addSeparator()
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())

        self.retranslateUi(CapitalAPI)
        QtCore.QMetaObject.connectSlotsByName(CapitalAPI)

    def retranslateUi(self, CapitalAPI):
        _translate = QtCore.QCoreApplication.translate
        CapitalAPI.setWindowTitle(_translate("CapitalAPI", "群益API"))
        self.menu.setTitle(_translate("CapitalAPI", "檔案"))
        self.menu_2.setTitle(_translate("CapitalAPI", "檢視"))
        self.menu_3.setTitle(_translate("CapitalAPI", "功能"))
        self.menu_4.setTitle(_translate("CapitalAPI", "說明"))
        self.actionLogin.setText(_translate("CapitalAPI", "登入"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CapitalAPI = QtWidgets.QMainWindow()
    ui = Ui_CapitalAPI()
    ui.setupUi(CapitalAPI)
    CapitalAPI.show()
    sys.exit(app.exec_())

