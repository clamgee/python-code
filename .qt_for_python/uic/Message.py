# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Message.ui'
##
## Created by: Qt User Interface Compiler version 6.0.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_MessageUI(object):
    def setupUi(self, MessageUI):
        if not MessageUI.objectName():
            MessageUI.setObjectName(u"MessageUI")
        MessageUI.setWindowModality(Qt.WindowModal)
        MessageUI.resize(640, 360)
        MessageUI.setSizeGripEnabled(True)
        self.gridLayout = QGridLayout(MessageUI)
        self.gridLayout.setObjectName(u"gridLayout")
        self.textBrowser = QTextBrowser(MessageUI)
        self.textBrowser.setObjectName(u"textBrowser")

        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)


        self.retranslateUi(MessageUI)

        QMetaObject.connectSlotsByName(MessageUI)
    # setupUi

    def retranslateUi(self, MessageUI):
        MessageUI.setWindowTitle(QCoreApplication.translate("MessageUI", u"\u8a0a\u606f", None))
    # retranslateUi

