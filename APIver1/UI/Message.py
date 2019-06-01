# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Message.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MessageUI(object):
    def setupUi(self, MessageUI):
        MessageUI.setObjectName("MessageUI")
        MessageUI.resize(640, 480)
        self.textBrowser = QtWidgets.QTextBrowser(MessageUI)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 640, 480))
        self.textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.append('test')

        self.retranslateUi(MessageUI)
        QtCore.QMetaObject.connectSlotsByName(MessageUI)

    def retranslateUi(self, MessageUI):
        _translate = QtCore.QCoreApplication.translate
        MessageUI.setWindowTitle(_translate("MessageUI", "SK訊息"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MessageUI = QtWidgets.QDialog()
    ui = Ui_MessageUI()
    ui.setupUi(MessageUI)
    MessageUI.show()
    sys.exit(app.exec_())

