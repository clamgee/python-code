#using: utf-8

from ui_graphArea import Ui_GraphArea
import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QWidget
import pyqtgraph as pg
import numpy as np
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget
import matplotlib.pyplot as plt

#被提升后的GraphView类定义方式
class GraphArea(QWidget, Ui_GraphArea):
    def __init__(self):
        super(GraphArea, self).__init__()
        self.setupUi(self)

    def plot_set_color(self):
        #设置对象颜色
        pass

    def plot_get_coordinate(self):
        #动态获取曲线坐标信息
        pass

    def plot_by_GraphicsLayout(self):
        gl = pg.GraphicsLayout()
        self.graphicsView.setCentralItem(gl)
        self.graphicsView.show()
        p1 = gl.addPlot(title="通过GraphicsLayout绘图")
        p1.plot([1, 3, 2, 4, 3, 5], pen='r')
        print(p1)

    def plot_by_PlotItem(self):
        x = np.arange(1000)
        y = np.random.normal(size=(1000,))
        plot1 = pg.PlotItem(title='PlotItem形式绘图')
        plot1.plot(x, y)  # 颜色变更方法一： plot1.plot(x, y, pen='r')
        print(plot1) #返回PlotItem对象,如下两种添加方式均无问题
        # self.graphicsView.setCentralWidget(plot1)
        self.graphicsView.setCentralItem(plot1)

    def plot_by_Plot(self):
        x = np.arange(1000)
        y = np.random.normal(size=(1000,))
        plot1 = pg.plot(x, y, pen='r')
        print(plot1)  #返回的是plotWindow对象，没法加到grahicsView中去，只是独立窗口
        # self.graphicsView.setCentralWidget(plot1) 错误用法

    def plot_by_PlotWidget(self):
        x = np.arange(1000)
        y = np.random.normal(size=(1000,))
        # plotItem1 = pg.PlotItem(title='通过PlotWidget方式绘图')
        # plotWidget1 = pg.PlotWidget(parent=None,background='r')
        # # plotWidget1.addItem(plotItem1)
        # self.graphicsView.setCentralWidget(plotWidget1)
        pass

    def plot_by_matplotlib(self):
        # MatplotLib绘图测试
        x = np.arange(1000)
        y = np.random.normal(size=(1000,))
        mw = MatplotlibWidget()
        # subplot = mw.getFigure()
        # subplot.plot(x, y)
        mw.draw() #嵌入graphicsView遇到问题
        #self.graphicsView.setCentralWidget(mw)
        pass

    def plot_MatplotLib(self):
        x = np.linspace(0, 10, 500)
        dashes = [10, 5, 100, 5]  # 10 points on, 5 off, 100 on, 5 off

        fig, ax = plt.subplots()
        line1, = ax.plot(x, np.sin(x), '--', linewidth=2,
                         label='Dashes set retroactively')
        line1.set_dashes(dashes)

        line2, = ax.plot(x, -1 * np.sin(x), dashes=[30, 5, 10, 5],
                         label='Dashes set proactively')

        ax.legend(loc='lower right')
        plt.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    graph1 = GraphArea()
    graph1.resize(400, 400)
    graph1.setWindowTitle('pyqtgraphGraphicsLayout')
    # graph1.plot_by_GraphicsLayout() #通过graphicsLayout布局绘图
    # graph1.plot_by_PlotItem() #通过PlotItem方式绘图
    # graph1.plot_by_Plot() #通过Plot方式绘图
    # graph1.plot_by_PlotWidget() #通过PlotWidget方式绘图
    graph1.plot_by_matplotlib() #与MatPlotlib交互
    # graph1.plot_MatplotLib()

    graph1.show()

    sys.exit(app.exec_())