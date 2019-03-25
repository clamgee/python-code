# import pyqtgraph as pg
# from pyqtgraph import QtCore, QtGui
# import numpy as np
# x = np.arange(1000)
# y = np.random.normal(size=(3, 1000))
# plotWidget = pg.plot(title="Three plot curves")
# for i in range(3):
#     plotWidget.plot(x, y[i], pen=(i,3)) 
# if __name__ == '__main__':
#     import sys
#     if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#          QtGui.QApplication.instance().exec_()

# if __name__=='__main__':
#     app=QApplication(sys.argv)
#     sys.exit(app.exec_())
import pyqtgraph.examples
pyqtgraph.examples.run()

# import keyword
# print(keyword.kwlist)

# # list all built-in keywords
# print(vars(__builtin__).keys())