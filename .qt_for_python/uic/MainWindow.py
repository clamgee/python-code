# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.0.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_CapitalAPI(object):
    def setupUi(self, CapitalAPI):
        if not CapitalAPI.objectName():
            CapitalAPI.setObjectName(u"CapitalAPI")
        CapitalAPI.resize(1024, 640)
        self.actionLogin = QAction(CapitalAPI)
        self.actionLogin.setObjectName(u"actionLogin")
        font = QFont()
        font.setPointSize(12)
        self.actionLogin.setFont(font)
        self.SysDetail = QAction(CapitalAPI)
        self.SysDetail.setObjectName(u"SysDetail")
        self.SysDetail.setFont(font)
        self.centralwidget = QWidget(CapitalAPI)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        CapitalAPI.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(CapitalAPI)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1024, 27))
        self.menubar.setFont(font)
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu.setFont(font)
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        self.menu_2.setFont(font)
        self.menu_3 = QMenu(self.menubar)
        self.menu_3.setObjectName(u"menu_3")
        self.menu_3.setGeometry(QRect(365, 132, 140, 78))
        self.menu_3.setFont(font)
        self.menu_4 = QMenu(self.menubar)
        self.menu_4.setObjectName(u"menu_4")
        self.menu_4.setFont(font)
        CapitalAPI.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(CapitalAPI)
        self.statusbar.setObjectName(u"statusbar")
        CapitalAPI.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menu_2.addAction(self.SysDetail)
        self.menu_3.addAction(self.actionLogin)

        self.retranslateUi(CapitalAPI)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(CapitalAPI)
    # setupUi

    def retranslateUi(self, CapitalAPI):
        CapitalAPI.setWindowTitle(QCoreApplication.translate("CapitalAPI", u"\u7a0b\u5f0f\u4ea4\u6613Ver.3.0.0", None))
        self.actionLogin.setText(QCoreApplication.translate("CapitalAPI", u"\u767b\u5165", None))
#if QT_CONFIG(tooltip)
        self.actionLogin.setToolTip(QCoreApplication.translate("CapitalAPI", u"\u5e33\u865f\u767b\u5165", None))
#endif // QT_CONFIG(tooltip)
        self.SysDetail.setText(QCoreApplication.translate("CapitalAPI", u"\u7cfb\u7d71\u8cc7\u8a0a", None))
#if QT_CONFIG(tooltip)
        self.SysDetail.setToolTip(QCoreApplication.translate("CapitalAPI", u"\u7cfb\u7d71\u8a73\u7d30\u8cc7\u8a0a", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("CapitalAPI", u"Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("CapitalAPI", u"Tab 2", None))
        self.menu.setTitle(QCoreApplication.translate("CapitalAPI", u"\u6a94\u6848", None))
        self.menu_2.setTitle(QCoreApplication.translate("CapitalAPI", u"\u6aa2\u8996", None))
        self.menu_3.setTitle(QCoreApplication.translate("CapitalAPI", u"\u529f\u80fd", None))
        self.menu_4.setTitle(QCoreApplication.translate("CapitalAPI", u"\u8aaa\u660e", None))
    # retranslateUi

