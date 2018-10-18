# import numpy as np
# import pandas as pd
# import datetime
# import time
# import matplotlib
# import matplotlib.dates as mdates
# import matplotlib.pyplot as plt
# from mpl_finance import candlestick2_ohlc
# import csv
# plt.ion()
# fig, ax = plt.subplots()
# ax.set_autoscaley_on(True)

# def drawbar(ndatetime,nopen,nhigh,nlow,nclose):
#     candlestick2_ohlc(
#         ax,
#         nopen,
#         nhigh,
#         nlow,
#         nclose,
#         width=0.6,colorup='r',colordown='g',alpha=1
#     )
#     ax.autoscale_view()
#     fig.canvas.draw()
#     fig.canvas.flush_events()

# csvpf=pd.DataFrame(columns=['ndatetime','open','high','low','close','volume'])
# print('DataFrame大小: ',csvpf.shape[0])
# csvpf[['open','high','low','close','volume']]=csvpf[['open','high','low','close','volume']].astype(int)
# with open('data.csv',mode='r',newline='') as file:
#     rows=csv.reader(file)
#     for row in rows:
#         ndatetime=datetime.datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S.%f')
#         newlist=[ndatetime,int(row[1]),int(row[2]),int(row[3]),int(row[4]),int(row[5])]
#         csvpf.loc[ndatetime]=newlist
#         # print(csvpf)
#         csvpf= csvpf.reset_index(drop=True)
#         # print(csvpf)
#         # csvpf['ndatetime']=csvpf['ndatetime'].map(mdates.date2num)
#         # print(csvpf)
#         ohlc=csvpf[['ndatetime','open','high','low','close']]
#         print(ohlc)
#         drawbar(ohlc['ndatetime'],ohlc['open'],ohlc['high'],ohlc['low'],ohlc['close'])
#         time.sleep(1)
#         # fig = plt.figure()

# print(csvpf.shape[0])

# candlestick2_ohlc(ax,
#                   ohlc['open'].values,
#                   ohlc['high'].values,
#                   ohlc['low'].values,
#                   ohlc['close'].values,
#                   width=0.6,colorup='r',colordown='g',alpha=1)

# plt.xticks(ohlc.index.values,ohlc['ndatetime'].values, size='small')
# ax.set_autoscaley_on(True)
# plt.show()
        # time.sleep(2)

import matplotlib.pyplot as plt
import numpy as np
import time
images = np.random.uniform(0, 255, size=(40, 50, 50))

fig, ax = plt.subplots()

im = ax.imshow(images[0])
fig.show()
for image in images[1:]:
    start=time.time()
    im.set_data(image)
    fig.canvas.draw()
    end=time.time()
    ep=end-start
    print('執行時間: ',ep)