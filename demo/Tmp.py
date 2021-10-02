import PySide6
import pandas as pd
from PySide6 import QtCore
from PySide6.QtCore import QObject
from valkka.multiprocess import MessageProcess
import typing

class PassSignal(MessageProcess):
    class Signals(QObject):
        def __init__(self, parent: typing.Optional[PySide6.QtCore.QObject] = ...) -> None:
            super().__init__(parent=parent)
            
PassSignalA = PassSignal()