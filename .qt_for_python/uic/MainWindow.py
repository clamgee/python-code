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
        CapitalAPI.resize(1024, 635)
        self.actionLogin = QAction(CapitalAPI)
        self.actionLogin.setObjectName(u"actionLogin")
        font = QFont()
        font.setPointSize(12)
        self.actionLogin.setFont(font)
        self.SysDetail = QAction(CapitalAPI)
        self.SysDetail.setObjectName(u"SysDetail")
        self.SysDetail.setFont(font)
        self.Connectbtn = QAction(CapitalAPI)
        self.Connectbtn.setObjectName(u"Connectbtn")
        self.Connectbtn.setFont(font)
        self.Disconnectbtn = QAction(CapitalAPI)
        self.Disconnectbtn.setObjectName(u"Disconnectbtn")
        self.Disconnectbtn.setFont(font)
        self.centralwidget = QWidget(CapitalAPI)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setFont(font)
        self.tabWidget.setTabPosition(QTabWidget.South)
        self.tab_TicksK = QWidget()
        self.tab_TicksK.setObjectName(u"tab_TicksK")
        self.tabWidget.addTab(self.tab_TicksK, "")
        self.tab_DayTrading = QWidget()
        self.tab_DayTrading.setObjectName(u"tab_DayTrading")
        self.tabWidget.addTab(self.tab_DayTrading, "")
        self.tab_Reply = QWidget()
        self.tab_Reply.setObjectName(u"tab_Reply")
        self.gridLayout_3 = QGridLayout(self.tab_Reply)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.Reply_TBW = QTableView(self.tab_Reply)
        self.Reply_TBW.setObjectName(u"Reply_TBW")

        self.verticalLayout.addWidget(self.Reply_TBW)

        self.Open_TBW = QTableView(self.tab_Reply)
        self.Open_TBW.setObjectName(u"Open_TBW")

        self.verticalLayout.addWidget(self.Open_TBW)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.tab_Reply)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.label.setFont(font1)
        self.label.setStyleSheet(u"background-color: rgb(0, 255, 0);")
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.Future_Acc_CBox = QComboBox(self.tab_Reply)
        self.Future_Acc_CBox.setObjectName(u"Future_Acc_CBox")
        self.Future_Acc_CBox.setMaxVisibleItems(16)
        self.Future_Acc_CBox.setMaxCount(16)

        self.horizontalLayout.addWidget(self.Future_Acc_CBox)

        self.Right_Update_btn = QPushButton(self.tab_Reply)
        self.Right_Update_btn.setObjectName(u"Right_Update_btn")

        self.horizontalLayout.addWidget(self.Right_Update_btn)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.Right_TB = QTableWidget(self.tab_Reply)
        if (self.Right_TB.columnCount() < 3):
            self.Right_TB.setColumnCount(3)
        if (self.Right_TB.rowCount() < 28):
            self.Right_TB.setRowCount(28)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(0, 0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(0, 1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(0, 2, __qtablewidgetitem2)
        brush = QBrush(QColor(0, 255, 0, 255))
        brush.setStyle(Qt.Dense4Pattern)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setBackground(brush);
        self.Right_TB.setItem(1, 0, __qtablewidgetitem3)
        brush1 = QBrush(QColor(0, 255, 0, 255))
        brush1.setStyle(Qt.Dense4Pattern)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setBackground(brush1);
        self.Right_TB.setItem(1, 1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(2, 0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(2, 1, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(2, 2, __qtablewidgetitem7)
        brush2 = QBrush(QColor(0, 255, 0, 255))
        brush2.setStyle(Qt.NoBrush)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem8.setBackground(brush2);
        self.Right_TB.setItem(4, 0, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(4, 1, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(4, 2, __qtablewidgetitem10)
        brush3 = QBrush(QColor(0, 0, 0, 255))
        brush3.setStyle(Qt.Dense4Pattern)
        brush4 = QBrush(QColor(0, 255, 0, 255))
        brush4.setStyle(Qt.Dense4Pattern)
        __qtablewidgetitem11 = QTableWidgetItem()
        __qtablewidgetitem11.setBackground(brush4);
        __qtablewidgetitem11.setForeground(brush3);
        self.Right_TB.setItem(5, 0, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        __qtablewidgetitem12.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(6, 0, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        __qtablewidgetitem13.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(6, 1, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        __qtablewidgetitem14.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(6, 2, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        __qtablewidgetitem15.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(8, 0, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        __qtablewidgetitem16.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(8, 1, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        __qtablewidgetitem17.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(8, 2, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        __qtablewidgetitem18.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(10, 0, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        __qtablewidgetitem19.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(10, 1, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        __qtablewidgetitem20.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(10, 2, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        __qtablewidgetitem21.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(12, 0, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        __qtablewidgetitem22.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(12, 1, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        __qtablewidgetitem23.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(12, 2, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        __qtablewidgetitem24.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(14, 0, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        __qtablewidgetitem25.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(14, 1, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        __qtablewidgetitem26.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(14, 2, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        __qtablewidgetitem27.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(16, 0, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        __qtablewidgetitem28.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(16, 1, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        __qtablewidgetitem29.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(16, 2, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        __qtablewidgetitem30.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(18, 0, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        __qtablewidgetitem31.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(18, 1, __qtablewidgetitem31)
        __qtablewidgetitem32 = QTableWidgetItem()
        __qtablewidgetitem32.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(18, 2, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        __qtablewidgetitem33.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(20, 0, __qtablewidgetitem33)
        __qtablewidgetitem34 = QTableWidgetItem()
        __qtablewidgetitem34.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(20, 1, __qtablewidgetitem34)
        __qtablewidgetitem35 = QTableWidgetItem()
        __qtablewidgetitem35.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(20, 2, __qtablewidgetitem35)
        __qtablewidgetitem36 = QTableWidgetItem()
        self.Right_TB.setItem(21, 1, __qtablewidgetitem36)
        __qtablewidgetitem37 = QTableWidgetItem()
        __qtablewidgetitem37.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(22, 0, __qtablewidgetitem37)
        __qtablewidgetitem38 = QTableWidgetItem()
        __qtablewidgetitem38.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(22, 1, __qtablewidgetitem38)
        __qtablewidgetitem39 = QTableWidgetItem()
        __qtablewidgetitem39.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(22, 2, __qtablewidgetitem39)
        __qtablewidgetitem40 = QTableWidgetItem()
        __qtablewidgetitem40.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(24, 0, __qtablewidgetitem40)
        __qtablewidgetitem41 = QTableWidgetItem()
        __qtablewidgetitem41.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(24, 1, __qtablewidgetitem41)
        __qtablewidgetitem42 = QTableWidgetItem()
        __qtablewidgetitem42.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(24, 2, __qtablewidgetitem42)
        __qtablewidgetitem43 = QTableWidgetItem()
        __qtablewidgetitem43.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(26, 0, __qtablewidgetitem43)
        __qtablewidgetitem44 = QTableWidgetItem()
        __qtablewidgetitem44.setTextAlignment(Qt.AlignCenter);
        self.Right_TB.setItem(26, 1, __qtablewidgetitem44)
        self.Right_TB.setObjectName(u"Right_TB")
        self.Right_TB.setLayoutDirection(Qt.LeftToRight)
        self.Right_TB.setAutoFillBackground(False)
        self.Right_TB.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.Right_TB.setAlternatingRowColors(True)
        self.Right_TB.setTextElideMode(Qt.ElideLeft)
        self.Right_TB.setSortingEnabled(False)
        self.Right_TB.setRowCount(28)
        self.Right_TB.setColumnCount(3)
        self.Right_TB.horizontalHeader().setVisible(False)
        self.Right_TB.verticalHeader().setVisible(False)

        self.verticalLayout_2.addWidget(self.Right_TB)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 29)

        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 1, 1, 1)

        self.gridLayout_2.setColumnStretch(0, 3)
        self.gridLayout_2.setColumnStretch(1, 2)

        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_Reply, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 1, 1, 1)

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
        self.menu_3.setGeometry(QRect(465, 196, 140, 78))
        self.menu_3.setFont(font)
        self.menu_4 = QMenu(self.menubar)
        self.menu_4.setObjectName(u"menu_4")
        self.menu_4.setFont(font)
        CapitalAPI.setMenuBar(self.menubar)
        self.statusBar = QStatusBar(CapitalAPI)
        self.statusBar.setObjectName(u"statusBar")
        CapitalAPI.setStatusBar(self.statusBar)
        self.toolBar = QToolBar(CapitalAPI)
        self.toolBar.setObjectName(u"toolBar")
        CapitalAPI.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menu_3.addAction(self.actionLogin)
        self.toolBar.addAction(self.SysDetail)
        self.toolBar.addAction(self.Connectbtn)
        self.toolBar.addAction(self.Disconnectbtn)

        self.retranslateUi(CapitalAPI)

        self.tabWidget.setCurrentIndex(2)


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
        self.Connectbtn.setText(QCoreApplication.translate("CapitalAPI", u"\u5831\u50f9\u9023\u7dda", None))
#if QT_CONFIG(tooltip)
        self.Connectbtn.setToolTip(QCoreApplication.translate("CapitalAPI", u"\u5efa\u7acb\u5831\u50f9\u9023\u7dda\u56de\u5831\u6a5f\u5236", None))
#endif // QT_CONFIG(tooltip)
        self.Disconnectbtn.setText(QCoreApplication.translate("CapitalAPI", u"\u505c\u6b62\u5831\u50f9", None))
        self.Disconnectbtn.setIconText(QCoreApplication.translate("CapitalAPI", u"\u505c\u6b62\u5831\u50f9", None))
#if QT_CONFIG(tooltip)
        self.Disconnectbtn.setToolTip(QCoreApplication.translate("CapitalAPI", u"\u65b7\u958b\u6216\u60c5\u9664\u5831\u50f9\u9023\u7dda\u72c0\u614b", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_TicksK), QCoreApplication.translate("CapitalAPI", u"TicksK\u7dda", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_DayTrading), QCoreApplication.translate("CapitalAPI", u"\u7576\u6c96", None))
        self.label.setText(QCoreApplication.translate("CapitalAPI", u"\u671f\u6b0a\u6b0a\u76ca\u6578", None))
        self.Right_Update_btn.setText(QCoreApplication.translate("CapitalAPI", u"\u66f4\u65b0", None))

        __sortingEnabled = self.Right_TB.isSortingEnabled()
        self.Right_TB.setSortingEnabled(False)
        ___qtablewidgetitem = self.Right_TB.item(0, 0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("CapitalAPI", u"\u5e33\u6236\u9918\u984d", None));
        ___qtablewidgetitem1 = self.Right_TB.item(0, 1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("CapitalAPI", u"\u6d6e\u52d5\u640d\u76ca", None));
        ___qtablewidgetitem2 = self.Right_TB.item(0, 2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("CapitalAPI", u"\u5df2\u5be6\u73fe\u8cbb\u7528", None));
        ___qtablewidgetitem3 = self.Right_TB.item(2, 0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("CapitalAPI", u"\u4ea4\u6613\u7a05", None));
        ___qtablewidgetitem4 = self.Right_TB.item(2, 1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("CapitalAPI", u"\u9810\u6263\u6b0a\u5229\u91d1", None));
        ___qtablewidgetitem5 = self.Right_TB.item(2, 2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("CapitalAPI", u"\u6b0a\u5229\u91d1\u6536\u4ed8", None));
        ___qtablewidgetitem6 = self.Right_TB.item(4, 0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("CapitalAPI", u"\u6b0a\u76ca\u6578", None));
        ___qtablewidgetitem7 = self.Right_TB.item(4, 1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("CapitalAPI", u"\u8d85\u984d\u4fdd\u8b49\u91d1", None));
        ___qtablewidgetitem8 = self.Right_TB.item(4, 2)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("CapitalAPI", u"\u5b58\u63d0\u6b3e", None));
        ___qtablewidgetitem9 = self.Right_TB.item(6, 0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("CapitalAPI", u"\u8cb7\u65b9\u5e02\u503c", None));
        ___qtablewidgetitem10 = self.Right_TB.item(6, 1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("CapitalAPI", u"\u8ce3\u65b9\u5e02\u503c", None));
        ___qtablewidgetitem11 = self.Right_TB.item(6, 2)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("CapitalAPI", u"\u671f\u8ca8\u5e73\u5009\u640d\u76ca", None));
        ___qtablewidgetitem12 = self.Right_TB.item(8, 0)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("CapitalAPI", u"\u76e4\u4e2d\u672a\u5be6\u73fe", None));
        ___qtablewidgetitem13 = self.Right_TB.item(8, 1)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("CapitalAPI", u"\u539f\u59cb\u4fdd\u8b49\u91d1", None));
        ___qtablewidgetitem14 = self.Right_TB.item(8, 2)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("CapitalAPI", u"\u7dad\u6301\u4fdd\u8b49\u91d1", None));
        ___qtablewidgetitem15 = self.Right_TB.item(10, 0)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("CapitalAPI", u"\u90e8\u4f4d\u539f\u59cb\u4fdd\u8b49\u91d1", None));
        ___qtablewidgetitem16 = self.Right_TB.item(10, 1)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("CapitalAPI", u"\u90e8\u4f4d\u7dad\u6301\u4fdd\u8b49\u91d1", None));
        ___qtablewidgetitem17 = self.Right_TB.item(10, 2)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("CapitalAPI", u"\u59d4\u8a17\u4fdd\u8b49\u91d1", None));
        ___qtablewidgetitem18 = self.Right_TB.item(12, 0)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("CapitalAPI", u"\u8d85\u984d\u6700\u4f73\u4fdd\u8b49\u91d1", None));
        ___qtablewidgetitem19 = self.Right_TB.item(12, 1)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("CapitalAPI", u"\u6b0a\u5229\u7e3d\u503c", None));
        ___qtablewidgetitem20 = self.Right_TB.item(12, 2)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("CapitalAPI", u"\u9810\u6263\u8cbb\u7528", None));
        ___qtablewidgetitem21 = self.Right_TB.item(14, 0)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("CapitalAPI", u"\u539f\u59cb\u4fdd\u8b49\u91d1", None));
        ___qtablewidgetitem22 = self.Right_TB.item(14, 1)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("CapitalAPI", u"\u6628\u65e5\u9918\u984d", None));
        ___qtablewidgetitem23 = self.Right_TB.item(14, 2)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("CapitalAPI", u"\u9078\u64c7\u6b0a\u7d44\u5408\u55ae\u52a0\u4e0d\u52a0\u6536\u4fdd\u8b49\u91d1", None));
        ___qtablewidgetitem24 = self.Right_TB.item(16, 0)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("CapitalAPI", u"\u7dad\u6301\u7387", None));
        ___qtablewidgetitem25 = self.Right_TB.item(16, 1)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("CapitalAPI", u"\u5e63\u5225", None));
        ___qtablewidgetitem26 = self.Right_TB.item(16, 2)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("CapitalAPI", u"\u8db3\u984d\u539f\u59cb\u4fdd\u8b49\u91d1", None));
        ___qtablewidgetitem27 = self.Right_TB.item(18, 0)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("CapitalAPI", u"\u8db3\u984d\u7dad\u6301\u4fdd\u8b49\u91d1", None));
        ___qtablewidgetitem28 = self.Right_TB.item(18, 1)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("CapitalAPI", u"\u8db3\u984d\u53ef\u7528", None));
        ___qtablewidgetitem29 = self.Right_TB.item(18, 2)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("CapitalAPI", u"\u62b5\u7e73\u91d1\u984d", None));
        ___qtablewidgetitem30 = self.Right_TB.item(20, 0)
        ___qtablewidgetitem30.setText(QCoreApplication.translate("CapitalAPI", u"\u6709\u50f9\u53ef\u7528", None));
        ___qtablewidgetitem31 = self.Right_TB.item(20, 1)
        ___qtablewidgetitem31.setText(QCoreApplication.translate("CapitalAPI", u"\u8d85\u984d\u4fdd\u8b49\u91d1", None));
        ___qtablewidgetitem32 = self.Right_TB.item(20, 2)
        ___qtablewidgetitem32.setText(QCoreApplication.translate("CapitalAPI", u"\u8db3\u984d\u73fe\u91d1\u53ef\u7528", None));
        ___qtablewidgetitem33 = self.Right_TB.item(22, 0)
        ___qtablewidgetitem33.setText(QCoreApplication.translate("CapitalAPI", u"\u6709\u50f9\u50f9\u503c", None));
        ___qtablewidgetitem34 = self.Right_TB.item(22, 1)
        ___qtablewidgetitem34.setText(QCoreApplication.translate("CapitalAPI", u"\u98a8\u96aa\u6307\u6a19", None));
        ___qtablewidgetitem35 = self.Right_TB.item(22, 2)
        ___qtablewidgetitem35.setText(QCoreApplication.translate("CapitalAPI", u"\u9078\u64c7\u6b0a\u5230\u671f\u5dee\u7570", None));
        ___qtablewidgetitem36 = self.Right_TB.item(24, 0)
        ___qtablewidgetitem36.setText(QCoreApplication.translate("CapitalAPI", u"\u9078\u64c7\u6b0a\u5230\u671f\u5dee\u640d", None));
        ___qtablewidgetitem37 = self.Right_TB.item(24, 1)
        ___qtablewidgetitem37.setText(QCoreApplication.translate("CapitalAPI", u"\u671f\u8ca8\u5230\u671f\u640d\u76ca", None));
        ___qtablewidgetitem38 = self.Right_TB.item(24, 2)
        ___qtablewidgetitem38.setText(QCoreApplication.translate("CapitalAPI", u"\u52a0\u6536\u4fdd\u8b49\u91d1", None));
        ___qtablewidgetitem39 = self.Right_TB.item(26, 0)
        ___qtablewidgetitem39.setText(QCoreApplication.translate("CapitalAPI", u"\u767b\u5165\u5e33\u865f", None));
        ___qtablewidgetitem40 = self.Right_TB.item(26, 1)
        ___qtablewidgetitem40.setText(QCoreApplication.translate("CapitalAPI", u"\u671f\u8ca8\u5e33\u865f", None));
        self.Right_TB.setSortingEnabled(__sortingEnabled)

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Reply), QCoreApplication.translate("CapitalAPI", u"\u671f\u6b0a\u5e33\u52d9", None))
        self.menu.setTitle(QCoreApplication.translate("CapitalAPI", u"\u6a94\u6848", None))
        self.menu_2.setTitle(QCoreApplication.translate("CapitalAPI", u"\u6aa2\u8996", None))
        self.menu_3.setTitle(QCoreApplication.translate("CapitalAPI", u"\u529f\u80fd", None))
        self.menu_4.setTitle(QCoreApplication.translate("CapitalAPI", u"\u8aaa\u660e", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("CapitalAPI", u"toolBar", None))
    # retranslateUi

