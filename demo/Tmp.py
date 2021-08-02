import sys
import random
from PySide6 import QtCore,QtWidgets,QtGui
from PySide6.QtUiTools import QUiLoader

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)


class SKMainWindow(QtWidgets.QMainWindow):  # 主視窗
    def __init__(self):
        super(SKMainWindow, self).__init__()
        self.loadUi = QUiLoader()
        self.loadUi.load(r'../APIver2/UI/MainWindow.ui', self)
        self.showMaximized()



    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = SKMainWindow()
    # widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())