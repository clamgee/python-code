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
        CommodityForm.resize(448, 663)
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
        self.Market_comboBox.setObjectName(u"Market_comboBox")

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

        self.horizontalLayout_7.addWidget(self.Commodity_comboBox)

        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 2)

        self.verticalLayout.addLayout(self.horizontalLayout_7)


        self.horizontalLayout_8.addLayout(self.verticalLayout)

        self.commoditybtn_pawn = QPushButton(CommodityForm)
        self.commoditybtn_pawn.setObjectName(u"commoditybtn_pawn")

        self.horizontalLayout_8.addWidget(self.commoditybtn_pawn)

        self.TDetailbtn_pawn = QPushButton(CommodityForm)
        self.TDetailbtn_pawn.setObjectName(u"TDetailbtn_pawn")

        self.horizontalLayout_8.addWidget(self.TDetailbtn_pawn)


        self.gridLayout.addLayout(self.horizontalLayout_8, 0, 0, 1, 1)

        self.DomTable_pawn = QTableView(CommodityForm)
        self.DomTable_pawn.setObjectName(u"DomTable_pawn")

        self.gridLayout.addWidget(self.DomTable_pawn, 1, 0, 1, 1)

        self.MPTableView_pawn = QTableView(CommodityForm)
        self.MPTableView_pawn.setObjectName(u"MPTableView_pawn")

        self.gridLayout.addWidget(self.MPTableView_pawn, 2, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(CommodityForm)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.contract_pawn = QLabel(CommodityForm)
        self.contract_pawn.setObjectName(u"contract_pawn")
        self.contract_pawn.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.contract_pawn)

        self.label_5 = QLabel(CommodityForm)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_2.addWidget(self.label_5)

        self.profit_pawn = QLabel(CommodityForm)
        self.profit_pawn.setObjectName(u"profit_pawn")
        self.profit_pawn.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.profit_pawn)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 2)
        self.horizontalLayout_2.setStretch(2, 1)
        self.horizontalLayout_2.setStretch(3, 2)

        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.BidAct_btn_pawn = QPushButton(CommodityForm)
        self.BidAct_btn_pawn.setObjectName(u"BidAct_btn_pawn")

        self.horizontalLayout_3.addWidget(self.BidAct_btn_pawn)

        self.AskAct_btn_pawn = QPushButton(CommodityForm)
        self.AskAct_btn_pawn.setObjectName(u"AskAct_btn_pawn")

        self.horizontalLayout_3.addWidget(self.AskAct_btn_pawn)

        self.InterestType_box_pawn = QComboBox(CommodityForm)
        self.InterestType_box_pawn.addItem("")
        self.InterestType_box_pawn.addItem("")
        self.InterestType_box_pawn.addItem("")
        self.InterestType_box_pawn.setObjectName(u"InterestType_box_pawn")

        self.horizontalLayout_3.addWidget(self.InterestType_box_pawn)

        self.OrderType_box_pawn = QComboBox(CommodityForm)
        self.OrderType_box_pawn.addItem("")
        self.OrderType_box_pawn.addItem("")
        self.OrderType_box_pawn.addItem("")
        self.OrderType_box_pawn.setObjectName(u"OrderType_box_pawn")

        self.horizontalLayout_3.addWidget(self.OrderType_box_pawn)


        self.gridLayout.addLayout(self.horizontalLayout_3, 4, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_7 = QLabel(CommodityForm)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_4.addWidget(self.label_7)

        self.PriceSpin_pawn = QDoubleSpinBox(CommodityForm)
        self.PriceSpin_pawn.setObjectName(u"PriceSpin_pawn")
        self.PriceSpin_pawn.setAlignment(Qt.AlignCenter)
        self.PriceSpin_pawn.setMaximum(30000.000000000000000)
        self.PriceSpin_pawn.setValue(10000.000000000000000)

        self.horizontalLayout_4.addWidget(self.PriceSpin_pawn)

        self.LastPrice_btn_pawn = QPushButton(CommodityForm)
        self.LastPrice_btn_pawn.setObjectName(u"LastPrice_btn_pawn")

        self.horizontalLayout_4.addWidget(self.LastPrice_btn_pawn)

        self.MarketPrice_btn_pawn = QPushButton(CommodityForm)
        self.MarketPrice_btn_pawn.setObjectName(u"MarketPrice_btn_pawn")

        self.horizontalLayout_4.addWidget(self.MarketPrice_btn_pawn)

        self.LimitMarketPrice_btn_pawn = QPushButton(CommodityForm)
        self.LimitMarketPrice_btn_pawn.setObjectName(u"LimitMarketPrice_btn_pawn")

        self.horizontalLayout_4.addWidget(self.LimitMarketPrice_btn_pawn)


        self.gridLayout.addLayout(self.horizontalLayout_4, 5, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_8 = QLabel(CommodityForm)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_5.addWidget(self.label_8)

        self.Contract_SpinBox = QSpinBox(CommodityForm)
        self.Contract_SpinBox.setObjectName(u"Contract_SpinBox")
        self.Contract_SpinBox.setAlignment(Qt.AlignCenter)
        self.Contract_SpinBox.setReadOnly(False)

        self.horizontalLayout_5.addWidget(self.Contract_SpinBox)

        self.dealbox_pawn = QCheckBox(CommodityForm)
        self.dealbox_pawn.setObjectName(u"dealbox_pawn")
        self.dealbox_pawn.setLayoutDirection(Qt.RightToLeft)
        self.dealbox_pawn.setChecked(True)

        self.horizontalLayout_5.addWidget(self.dealbox_pawn)

        self.Order_btn_pawn = QDialogButtonBox(CommodityForm)
        self.Order_btn_pawn.setObjectName(u"Order_btn_pawn")
        self.Order_btn_pawn.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.horizontalLayout_5.addWidget(self.Order_btn_pawn)

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
        self.Order_btn_pawn.rejected.connect(self.AskAct_btn_pawn.toggle)
        self.Order_btn_pawn.rejected.connect(self.BidAct_btn_pawn.toggle)

        QMetaObject.connectSlotsByName(CommodityForm)
    # setupUi

    def retranslateUi(self, CommodityForm):
        CommodityForm.setWindowTitle(QCoreApplication.translate("CommodityForm", u"\u5546\u54c1\u4e94\u6a94&\u5927\u5c0f\u55ae&\u4e0b\u55ae", None))
        self.label.setText(QCoreApplication.translate("CommodityForm", u"\u5e02\u5834\u5225", None))
        self.Market_comboBox.setItemText(0, QCoreApplication.translate("CommodityForm", u"\u8acb\u9078\u64c7", None))
        self.Market_comboBox.setItemText(1, QCoreApplication.translate("CommodityForm", u"\u671f\u8ca8", None))
        self.Market_comboBox.setItemText(2, QCoreApplication.translate("CommodityForm", u"\u9078\u64c7\u6b0a", None))

        self.label_2.setText(QCoreApplication.translate("CommodityForm", u"\u5546\u54c1\u540d\u7a31", None))
        self.Commodity_comboBox.setItemText(0, QCoreApplication.translate("CommodityForm", u"\u8acb\u9078\u64c7", None))

        self.commoditybtn_pawn.setText(QCoreApplication.translate("CommodityForm", u"\u78ba\u5b9a", None))
        self.TDetailbtn_pawn.setText(QCoreApplication.translate("CommodityForm", u"\u4ea4\u6613\u660e\u7d30", None))
        self.label_3.setText(QCoreApplication.translate("CommodityForm", u"\u672a\u5e73\u5009:", None))
        self.contract_pawn.setText(QCoreApplication.translate("CommodityForm", u"0", None))
        self.label_5.setText(QCoreApplication.translate("CommodityForm", u"\u640d\u76ca", None))
        self.profit_pawn.setText(QCoreApplication.translate("CommodityForm", u"0", None))
        self.BidAct_btn_pawn.setText(QCoreApplication.translate("CommodityForm", u"\u8cb7", None))
        self.AskAct_btn_pawn.setText(QCoreApplication.translate("CommodityForm", u"\u8ce3", None))
        self.InterestType_box_pawn.setItemText(0, QCoreApplication.translate("CommodityForm", u"\u81ea\u52d5\u5009", None))
        self.InterestType_box_pawn.setItemText(1, QCoreApplication.translate("CommodityForm", u"\u65b0\u5009", None))
        self.InterestType_box_pawn.setItemText(2, QCoreApplication.translate("CommodityForm", u"\u5e73\u5009", None))

        self.OrderType_box_pawn.setItemText(0, QCoreApplication.translate("CommodityForm", u"ROD", None))
        self.OrderType_box_pawn.setItemText(1, QCoreApplication.translate("CommodityForm", u"IOC", None))
        self.OrderType_box_pawn.setItemText(2, QCoreApplication.translate("CommodityForm", u"FOK", None))

        self.label_7.setText(QCoreApplication.translate("CommodityForm", u"\u59d4\u8a17\u50f9:", None))
        self.LastPrice_btn_pawn.setText(QCoreApplication.translate("CommodityForm", u"\u73fe\u50f9", None))
        self.MarketPrice_btn_pawn.setText(QCoreApplication.translate("CommodityForm", u"\u5e02\u50f9", None))
        self.LimitMarketPrice_btn_pawn.setText(QCoreApplication.translate("CommodityForm", u"\u7bc4\u570d\u5e02\u50f9", None))
        self.label_8.setText(QCoreApplication.translate("CommodityForm", u"\u53e3\u6578:", None))
        self.dealbox_pawn.setText(QCoreApplication.translate("CommodityForm", u"\u76e4\u4e2d:", None))
        self.OrderCancel_btn_pawn.setText(QCoreApplication.translate("CommodityForm", u"\u4e00\u9375\u522a\u55ae", None))
        self.ClosePositionAll_btn_pawn.setText(QCoreApplication.translate("CommodityForm", u"\u4e00\u9375\u5e73\u5009", None))
    # retranslateUi

