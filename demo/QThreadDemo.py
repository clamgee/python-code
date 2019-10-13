import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QFormLayout, QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal


class TutorialThread(QThread):
    set_max = pyqtSignal(int)
    update = pyqtSignal(int)
    
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        self.update.emit(100)
        for index in range(1, 101):
            self.update.emit(index)
            time.sleep(0.1)


class MainWindow(QWidget):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi()
        self._tutorial_thread = TutorialThread()
        self._tutorial_thread.set_max.connect(self.set_max)
        self._tutorial_thread.update.connect(self.set_value)
        self.show()

    def setupUi(self):
        self.setWindowTitle("執行緒的使用")

        self.button_start = QPushButton()
        self.button_start.setText("開始")
        self.button_stop = QPushButton()
        self.button_stop.setText("結束")

        self.progress_bar = QProgressBar()

        self.line = QLineEdit()

        form_layout = QFormLayout()
        form_layout.addRow(self.button_start, self.line)
        form_layout.addRow(self.button_stop)
        form_layout.addRow(self.progress_bar)

        h_layout = QVBoxLayout()
        h_layout.addLayout(form_layout)

        self.setLayout(h_layout)

        self.button_start.clicked.connect(self.start)
        self.button_stop.clicked.connect(self.stop)

    def start(self):
        self.line.setText("觸發後可以修改")
        self._tutorial_thread.start()

    def stop(self):
        self._tutorial_thread.terminate()

    def set_max(self, data):
        self.progress_bar.setMaximum(data)

    def set_value(self, data):
        self.progress_bar.setValue(data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    sys.exit(app.exec_())