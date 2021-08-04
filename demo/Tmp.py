import sys
from PySide6 import QtCore,QtWidgets,QtGui
from PySide6.QtUiTools import QUiLoader

from wigglywidget import WigglyWidget

import QtDesigner


TOOLTIP = "A cool wiggly widget (Python)"
DOM_XML = """
<ui language='c++'>
    <widget class='WigglyWidget' name='wigglyWidget'>
        <property name='geometry'>
            <rect>
                <x>0</x>
                <y>0</y>
                <width>400</width>
                <height>200</height>
            </rect>
        </property>
        <property name='text'>
            <string>Hello, world</string>
        </property>
    </widget>
</ui>
"""

QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(WigglyWidget, module="wigglywidget",tool_tip=TOOLTIP, xml=DOM_XML)

class SKMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(SKMainWindow, self).__init__()
        self.loadUi = QUiLoader()
        self.loadUi.load(r'../APIver3/UI/MainWindow.ui')



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    SKMain = SKMainWindow()
    # SKMain.showMaximized()
    SKMain.show()


    sys.exit(app.exec())