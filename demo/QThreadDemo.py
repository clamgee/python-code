# from PyQt5.QtWidgets import QApplication,QGraphicsScene,QGraphicsView
# import pyqtgraph as pg
# import numpy as np
# if __name__ == '__main__':
#     import sys
#     apps = QApplication(sys.argv)
#     scene = QGraphicsScene()
#     plt = pg.PlotItem()
#     x = np.arange(1000)
#     y1 = np.random.randint(0,50 + 1)
#     bar1 = pg.BarGraphItem(x=x, height=y1, width=1, brush='r')
#     plt.addItem(bar1)
#     scene.addItem(plt)
#     view = QGraphicsView(scene)
#     view.show()
#     sys.exit(apps.exec_())
import pyqtgraph.examples
pyqtgraph.examples.run()