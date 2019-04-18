# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         pyqtgraph逐点画波形图
# Description:
# Author:       lgk
# Date:         2018/6/2
#-------------------------------------------------------------------------------

import pyqtgraph as pg
import numpy as np
import array

app = pg.mkQApp()

win = pg.GraphicsWindow()
win.setWindowTitle(u'pyqtgraph逐点画波形图')
win.resize(800, 500)

data = array.array('d') #可动态改变数组的大小,double型数组
historyLength = 200

p = win.addPlot()
p.showGrid(x=True, y=True)

p.setRange(xRange=[200,400], yRange=[-1.2, 1.2], padding=0)
p.setLabel(axis='left', text='y / V')
p.setLabel(axis='bottom', text='x / point')
p.setTitle('y = sin(x)')

curve = p.plot()
idx = 0

def plotData():
    global idx
    tmp = np.sin(np.pi / 50 * idx)

    if len(data)<historyLength:
        data.append(tmp)
    else:
        data[:-1] = data[1:]
        data[-1] = tmp
        # curve.setPos(idx-historyLength, 0)
        # p.enableAutoRange('x', True)

    curve.setData(np.frombuffer(data, dtype=np.double))
    # curve.setData(data) #也可以
    idx += 1

timer = pg.QtCore.QTimer()
timer.timeout.connect(plotData)
timer.start(50)

app.exec_()