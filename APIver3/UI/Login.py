# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Login.ui'
##
## Created by: Qt User Interface Compiler version 6.0.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_LoginUI(object):
    def setupUi(self, LoginUI):
        if not LoginUI.objectName():
            LoginUI.setObjectName(u"LoginUI")
        LoginUI.resize(274, 196)
        self.LoginConfirmbtn = QDialogButtonBox(LoginUI)
        self.LoginConfirmbtn.setObjectName(u"LoginConfirmbtn")
        self.LoginConfirmbtn.setGeometry(QRect(70, 110, 191, 32))
        font = QFont()
        font.setPointSize(12)
        self.LoginConfirmbtn.setFont(font)
        self.LoginConfirmbtn.setOrientation(Qt.Horizontal)
        self.LoginConfirmbtn.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.LoginConfirmbtn.setCenterButtons(True)
        self.IDPWCheck = QCheckBox(LoginUI)
        self.IDPWCheck.setObjectName(u"IDPWCheck")
        self.IDPWCheck.setGeometry(QRect(80, 150, 161, 31))
        self.IDPWCheck.setFont(font)
        self.IDPWCheck.setLayoutDirection(Qt.RightToLeft)
        self.IDPWCheck.setChecked(True)
        self.layoutWidget = QWidget(LoginUI)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 20, 221, 28))
        self.layoutWidget.setFont(font)
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.label.setFont(font1)

        self.horizontalLayout.addWidget(self.label)

        self.LoginID = QLineEdit(self.layoutWidget)
        self.LoginID.setObjectName(u"LoginID")
        self.LoginID.setFont(font)
        self.LoginID.setMaxLength(16)

        self.horizontalLayout.addWidget(self.LoginID)

        self.layoutWidget1 = QWidget(LoginUI)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(20, 60, 221, 28))
        self.layoutWidget1.setFont(font)
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.layoutWidget1)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.LoginPW = QLineEdit(self.layoutWidget1)
        self.LoginPW.setObjectName(u"LoginPW")
        self.LoginPW.setFont(font)
        self.LoginPW.setMaxLength(16)
        self.LoginPW.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_2.addWidget(self.LoginPW)


        self.retranslateUi(LoginUI)
        self.LoginConfirmbtn.rejected.connect(self.LoginID.clear)
        self.LoginConfirmbtn.rejected.connect(self.LoginPW.clear)

        QMetaObject.connectSlotsByName(LoginUI)
    # setupUi

    def retranslateUi(self, LoginUI):
        LoginUI.setWindowTitle(QCoreApplication.translate("LoginUI", u"\u767b\u5165", None))
        self.IDPWCheck.setText(QCoreApplication.translate("LoginUI", u"\u662f\u5426\u5132\u5b58\u5e33\u865f\u5bc6\u78bc", None))
        self.label.setText(QCoreApplication.translate("LoginUI", u"  \u5e33\u865f  ", None))
        self.label_2.setText(QCoreApplication.translate("LoginUI", u"  \u5bc6\u78bc  ", None))
    # retranslateUi

