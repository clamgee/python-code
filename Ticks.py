# # 
import matplotlib.pyplot as plt
import numpy as np
import time
plt.ion()
images = np.random.uniform(0, 255, size=(40, 50, 50))
fig, ax = plt.subplots()

fig.canvas.draw()
for image in images:
    start=time.time()
    ax.imshow(image)
    fig.canvas.flush_events()
    ax.cla()
    end=time.time()
    ep=end-start
    print('執行時間: ',ep)



# plt.ion()
# fig, ax = plt.subplots()
# line, = ax.plot(np.random.randn(100))
# fig.canvas.draw()

# tstart = time.time()
# num_plots = 0
# while time.time()-tstart < 5:
#     start=time.time()
#     line.set_ydata(np.random.randn(100))
#     ax.draw_artist(ax.patch)
#     ax.draw_artist(line)
#     # fig.canvas.update()
#     fig.canvas.flush_events()
#     num_plots += 1
#     end=time.time()
#     ep=round((end-start),6)
#     print('單一繪圖: ',ep)
# print(num_plots/5)