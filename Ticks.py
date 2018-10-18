# 
import matplotlib.pyplot as plt
import numpy as np
import time
images = np.random.uniform(0, 255, size=(40, 50, 50))

fig, ax = plt.subplots()

fig.show()
for image in images:
    start=time.time()
    ax.imshow(image)
    fig.canvas.draw()
    ax.cla()
    end=time.time()
    ep=end-start
    print('執行時間: ',ep)