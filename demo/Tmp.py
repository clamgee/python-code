
from sys import platform

import winreg
from winreg import HKEY_LOCAL_MACHINE
import platform
print(platform.machine())

def open_key(key):
    """Open the register key.
    Args:
        key (str): The key of register.
    Returns:
        str: The handle to the specified key.
    """
    machine_type = platform.machine()
    mappings = {"AMD64": winreg.KEY_WOW64_64KEY}
    return winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE,
        key,
        access=winreg.KEY_READ | mappings.get(machine_type, winreg.KEY_WOW64_32KEY),
    )

# import os
# import PySide2
# dirname = os.path.dirname(PySide2.__file__)
# plugin_path = os.path.join(dirname, 'plugins', 'platforms')
# os.environ['PYSIDE_DESIGNER_PLUGINS'] = plugin_path
# print(plugin_path)


# import sys
# import os
# import PySide6
# from PySide6.QtWidgets import QApplication, QMainWindow
# from PySide6.QtCore import QFile
# from PySide6.QtUiTools import QUiLoader
# # from MainWindows import Ui_CapitalAPI
# # os.environ['PYSIDE_DESIGNER_PLUGINS'] = "C:\\Users\\Gary\\anaconda3\\Lib\\site-packages\\PySide6\\plugins"
# # dirname = os.path.dirname(PySide6.__file__)
# # plugin_path = os.path.join(dirname, 'plugins')
# # os.environ['PYSIDE_DESIGNER_PLUGINS'] = plugin_path
# # print(plugin_path)


# class MyMainWindow(QMainWindow):
#     def __init__(self):
#         super(MyMainWindow, self).__init__()
#         self.load_ui()
    
#     # def load_ui(self):
#     #     self.ui = Ui_CapitalAPI()
#     #     self.ui.setupUI(self)

#     def load_ui(self):
#         loader = QUiLoader()
#         path = os.path.join(os.path.dirname(__file__), "../APIver3/UI/MainWindow.ui")
#         ui_file = QFile(path)
#         ui_file.open(QFile.ReadOnly)
#         loader.load(ui_file, self)
#         ui_file.close()

# if __name__ == "__main__":
#     app = QApplication([])
#     widget = MyMainWindow()
#     widget.show()
#     sys.exit(app.exec())


