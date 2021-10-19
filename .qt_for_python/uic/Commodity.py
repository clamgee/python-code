# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Commodity.ui'
##
## Created by: Qt User Interface Compiler version 6.0.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_CommodityForm(object):
    def setupUi(self, CommodityForm):
        if not CommodityForm.objectName():
            CommodityForm.setObjectName(u"CommodityForm")
        CommodityForm.setWindowModality(Qt.WindowModal)
        CommodityForm.resize(450, 800)
        CommodityForm.setMinimumSize(QSize(0, 0))
        CommodityForm.setBaseSize(QSize(450, 800))
        CommodityForm.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.gridLayout_2 = QGridLayout(CommodityForm)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(CommodityForm)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.Market_comboBox = QComboBox(CommodityForm)
        self.Market_comboBox.addItem("")
        self.Market_comboBox.addItem("")
        self.Market_comboBox.addItem("")
        self.Market_comboBox.addItem("")
        self.Market_comboBox.setObjectName(u"Market_comboBox")
        self.Market_comboBox.setMaxVisibleItems(4)
        self.Market_comboBox.setMaxCount(4)

        self.horizontalLayout.addWidget(self.Market_comboBox)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_2 = QLabel(CommodityForm)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_7.addWidget(self.label_2)

        self.Commodity_comboBox = QComboBox(CommodityForm)
        self.Commodity_comboBox.addItem("")
        self.Commodity_comboBox.setObjectName(u"Commodity_comboBox")
        self.Commodity_comboBox.setMaxVisibleItems(16)

        self.horizontalLayout_7.addWidget(self.Commodity_comboBox)

        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 2)

        self.verticalLayout.addLayout(self.horizontalLayout_7)


        self.horizontalLayout_8.addLayout(self.verticalLayout)

        self.commoditybtn = QPushButton(CommodityForm)
        self.commoditybtn.setObjectName(u"commoditybtn")

        self.horizontalLayout_8.addWidget(self.commoditybtn)

        self.TDetailbtn = QPushButton(CommodityForm)
        self.TDetailbtn.setObjectName(u"TDetailbtn")

        self.horizontalLayout_8.addWidget(self.TDetailbtn)


        self.gridLayout.addLayout(self.horizontalLayout_8, 0, 0, 1, 1)

        self.DomTable = QTableView(CommodityForm)
        self.DomTable.setObjectName(u"DomTable")

        self.gridLayout.addWidget(self.DomTable, 1, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(CommodityForm)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_3)

        self.contract = QLabel(CommodityForm)
        self.contract.setObjectName(u"contract")
        self.contract.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.contract)

        self.label_5 = QLabel(CommodityForm)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_5)

        self.profit = QLabel(CommodityForm)
        self.profit.setObjectName(u"profit")
        self.profit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.profit)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 2)
        self.horizontalLayout_2.setStretch(2, 1)
        self.horizontalLayout_2.setStretch(3, 2)

        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.BidAct_btn = QPushButton(CommodityForm)
        self.BidAct_btn.setObjectName(u"BidAct_btn")

        self.horizontalLayout_3.addWidget(self.BidAct_btn)

        self.AskAct_btn = QPushButton(CommodityForm)
        self.AskAct_btn.setObjectName(u"AskAct_btn")

        self.horizontalLayout_3.addWidget(self.AskAct_btn)

        self.InterestType_box = QComboBox(CommodityForm)
        self.InterestType_box.addItem("")
        self.InterestType_box.addItem("")
        self.InterestType_box.addItem("")
        self.InterestType_box.setObjectName(u"InterestType_box")

        self.horizontalLayout_3.addWidget(self.InterestType_box)

        self.OrderType_box = QComboBox(CommodityForm)
        self.OrderType_box.addItem("")
        self.OrderType_box.addItem("")
        self.OrderType_box.addItem("")
        self.OrderType_box.setObjectName(u"OrderType_box")

        self.horizontalLayout_3.addWidget(self.OrderType_box)


        self.gridLayout.addLayout(self.horizontalLayout_3, 4, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_7 = QLabel(CommodityForm)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_7)

        self.PriceSpin = QDoubleSpinBox(CommodityForm)
        self.PriceSpin.setObjectName(u"PriceSpin")
        self.PriceSpin.setAlignment(Qt.AlignCenter)
        self.PriceSpin.setMaximum(30000.000000000000000)
        self.PriceSpin.setValue(10000.000000000000000)

        self.horizontalLayout_4.addWidget(self.PriceSpin)

        self.LastPrice_btn = QPushButton(CommodityForm)
        self.LastPrice_btn.setObjectName(u"LastPrice_btn")

        self.horizontalLayout_4.addWidget(self.LastPrice_btn)

        self.MarketPrice_btn = QPushButton(CommodityForm)
        self.MarketPrice_btn.setObjectName(u"MarketPrice_btn")

        self.horizontalLayout_4.addWidget(self.MarketPrice_btn)

        self.LimitMarketPrice_btn = QPushButton(CommodityForm)
        self.LimitMarketPrice_btn.setObjectName(u"LimitMarketPrice_btn")

        self.horizontalLayout_4.addWidget(self.LimitMarketPrice_btn)


        self.gridLayout.addLayout(self.horizontalLayout_4, 5, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_8 = QLabel(CommodityForm)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.label_8)

        self.Contract_SpinBox = QSpinBox(CommodityForm)
        self.Contract_SpinBox.setObjectName(u"Contract_SpinBox")
        self.Contract_SpinBox.setAlignment(Qt.AlignCenter)
        self.Contract_SpinBox.setReadOnly(False)

        self.horizontalLayout_5.addWidget(self.Contract_SpinBox)

        self.dealbox = QCheckBox(CommodityForm)
        self.dealbox.setObjectName(u"dealbox")
        self.dealbox.setLayoutDirection(Qt.RightToLeft)
        self.dealbox.setChecked(True)

        self.horizontalLayout_5.addWidget(self.dealbox)

        self.Order_btn = QDialogButtonBox(CommodityForm)
        self.Order_btn.setObjectName(u"Order_btn")
        self.Order_btn.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.horizontalLayout_5.addWidget(self.Order_btn)

        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 1)
        self.horizontalLayout_5.setStretch(2, 1)
        self.horizontalLayout_5.setStretch(3, 3)

        self.gridLayout.addLayout(self.horizontalLayout_5, 6, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.OrderCancel_btn_pawn = QPushButton(CommodityForm)
        self.OrderCancel_btn_pawn.setObjectName(u"OrderCancel_btn_pawn")

        self.horizontalLayout_6.addWidget(self.OrderCancel_btn_pawn)

        self.ClosePositionAll_btn_pawn = QPushButton(CommodityForm)
        self.ClosePositionAll_btn_pawn.setObjectName(u"ClosePositionAll_btn_pawn")

        self.horizontalLayout_6.addWidget(self.ClosePositionAll_btn_pawn)


        self.gridLayout.addLayout(self.horizontalLayout_6, 7, 0, 1, 1)

        self.MPTable = QTableWidget(CommodityForm)
        if (self.MPTable.columnCount() < 4):
            self.MPTable.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignCenter);
        self.MPTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setTextAlignment(Qt.AlignCenter);
        self.MPTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setTextAlignment(Qt.AlignCenter);
        self.MPTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setTextAlignment(Qt.AlignCenter);
        self.MPTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        if (self.MPTable.rowCount() < 4):
            self.MPTable.setRowCount(4)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setTextAlignment(Qt.AlignCenter);
        self.MPTable.setVerticalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setTextAlignment(Qt.AlignCenter);
        self.MPTable.setVerticalHeaderItem(1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setTextAlignment(Qt.AlignCenter);
        self.MPTable.setVerticalHeaderItem(2, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setTextAlignment(Qt.AlignCenter);
        self.MPTable.setVerticalHeaderItem(3, __qtablewidgetitem7)
        self.MPTable.setObjectName(u"MPTable")
        self.MPTable.setRowCount(4)
        self.MPTable.setColumnCount(4)

        self.gridLayout.addWidget(self.MPTable, 2, 0, 1, 1)

        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 5)
        self.gridLayout.setRowStretch(2, 4)
        self.gridLayout.setRowStretch(3, 1)
        self.gridLayout.setRowStretch(4, 1)
        self.gridLayout.setRowStretch(5, 1)
        self.gridLayout.setRowStretch(6, 1)
        self.gridLayout.setRowStretch(7, 1)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(CommodityForm)
        self.Order_btn.rejected.connect(self.AskAct_btn.toggle)
        self.Order_btn.rejected.connect(self.BidAct_btn.toggle)

        self.Market_comboBox.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(CommodityForm)
    # setupUi

    def retranslateUi(self, CommodityForm):
        CommodityForm.setWindowTitle(QCoreApplication.translate("CommodityForm", u"\u5546\u54c1\u4e94\u6a94&\u5927\u5c0f\u55ae&\u4e0b\u55ae", None))
        self.label.setText(QCoreApplication.translate("CommodityForm", u"\u5e02\u5834\u5225", None))
        self.Market_comboBox.setItemText(0, QCoreApplication.translate("CommodityForm", u"\u4e0a\u5e02", None))
        self.Market_comboBox.setItemText(1, QCoreApplication.translate("CommodityForm", u"\u4e0a\u6ac3", None))
        self.Market_comboBox.setItemText(2, QCoreApplication.translate("CommodityForm", u"\u671f\u8ca8", None))
        self.Market_comboBox.setItemText(3, QCoreApplication.translate("CommodityForm", u"\u9078\u64c7\u6b0a", None))

        self.label_2.setText(QCoreApplication.translate("CommodityForm", u"\u5546\u54c1\u540d\u7a31", None))
        self.Commodity_comboBox.setItemText(0, QCoreApplication.translate("CommodityForm", u"\u8acb\u9078\u64c7", None))

        self.commoditybtn.setText(QCoreApplication.translate("CommodityForm", u"\u78ba\u5b9a", None))
        self.TDetailbtn.setText(QCoreApplication.translate("CommodityForm", u"\u4ea4\u6613\u660e\u7d30", None))
        self.label_3.setText(QCoreApplication.translate("CommodityForm", u"\u672a\u5e73\u5009:", None))
        self.contract.setText(QCoreApplication.translate("CommodityForm", u"0", None))
        self.label_5.setText(QCoreApplication.translate("CommodityForm", u"\u640d\u76ca", None))
        self.profit.setText(QCoreApplication.translate("CommodityForm", u"0", None))
        self.BidAct_btn.setText(QCoreApplication.translate("CommodityForm", u"\u8cb7", None))
        self.AskAct_btn.setText(QCoreApplication.translate("CommodityForm", u"\u8ce3", None))
        self.InterestType_box.setItemText(0, QCoreApplication.translate("CommodityForm", u"\u81ea\u52d5\u5009", None))
        self.InterestType_box.setItemText(1, QCoreApplication.translate("CommodityForm", u"\u65b0\u5009", None))
        self.InterestType_box.setItemText(2, QCoreApplication.translate("CommodityForm", u"\u5e73\u5009", None))

        self.OrderType_box.setItemText(0, QCoreApplication.translate("CommodityForm", u"ROD", None))
        self.OrderType_box.setItemText(1, QCoreApplication.translate("CommodityForm", u"IOC", None))
        self.OrderType_box.setItemText(2, QCoreApplication.translate("CommodityForm", u"FOK", None))

        self.label_7.setText(QCoreApplication.translate("CommodityForm", u"\u59d4\u8a17\u50f9:", None))
        self.LastPrice_btn.setText(QCoreApplication.translate("CommodityForm", u"\u73fe\u50f9", None))
        self.MarketPrice_btn.setText(QCoreApplication.translate("CommodityForm", u"\u5e02\u50f9", None))
        self.LimitMarketPrice_btn.setText(QCoreApplication.translate("CommodityForm", u"\u7bc4\u570d\u5e02\u50f9", None))
        self.label_8.setText(QCoreApplication.translate("CommodityForm", u"\u53e3\u6578:", None))
        self.dealbox.setText(QCoreApplication.translate("CommodityForm", u"\u76e4\u4e2d:", None))
        self.OrderCancel_btn_pawn.setText(QCoreApplication.translate("CommodityForm", u"\u4e00\u9375\u522a\u55ae", None))
        self.ClosePositionAll_btn_pawn.setText(QCoreApplication.translate("CommodityForm", u"\u4e00\u9375\u5e73\u5009", None))
        ___qtablewidgetitem = self.MPTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("CommodityForm", u"\u59d4\u8a17\u53e3\u6578", None));
        ___qtablewidgetitem1 = self.MPTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("CommodityForm", u"\u59d4\u8a17\u7b46\u6578", None));
        ___qtablewidgetitem2 = self.MPTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("CommodityForm", u"\u6210\u4ea4\u7b46\u6578", None));
        ___qtablewidgetitem3 = self.MPTable.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("CommodityForm", u"\u6210\u4ea4\u53e3\u6578", None));
        ___qtablewidgetitem4 = self.MPTable.verticalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("CommodityForm", u"\u8cb7\u9032", None));
        ___qtablewidgetitem5 = self.MPTable.verticalHeaderItem(1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("CommodityForm", u"\u8ce3\u51fa", None));
        ___qtablewidgetitem6 = self.MPTable.verticalHeaderItem(2)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("CommodityForm", u"\u5dee\u984d", None));
        ___qtablewidgetitem7 = self.MPTable.verticalHeaderItem(3)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("CommodityForm", u"\u7e3d\u53e3\u6578", None));
    # retranslateUi

