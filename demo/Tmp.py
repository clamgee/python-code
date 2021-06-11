# import pyqtgraph.examples
# pyqtgraph.examples.run()

import numpy as np
import pyqtgraph as pg

data = 1000
pg.plot(1000, fillLevel=0, brush=(50,50,200,100))

# data = np.random.normal(size=(500,500))
# pg.image(data, title="Simplest possible image example")


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()