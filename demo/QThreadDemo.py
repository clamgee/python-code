import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

global sec
sec = 0

def setTime():
    global sec
    sec += 1
    # LED顯示數字+1
    lcdNumber.display(sec)

def work():
    # 計時器每秒計數
    timer.start(1000)

    # 開始一次非常耗時的計算
    # 這裡用一個2 000 000 000次的迴圈來模擬
    for i in range(200000000):
        pass

    timer.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    top = QWidget()
    top.resize(300, 120)

    # 垂直佈局類QVBoxLayout
    layout = QVBoxLayout(top)

    # 新增控制元件
    lcdNumber = QLCDNumber()
    layout.addWidget(lcdNumber)
    button = QPushButton("測試")
    layout.addWidget(button)
    timer = QTimer()

    # 每次計時結束，觸發setTime
    timer.timeout.connect(setTime)

    # 連線測試按鈕和槽函式work
    button.clicked.connect(work)

    top.show()
    sys.exit(app.exec_())