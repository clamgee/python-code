<<<<<<< HEAD
# import numpy as np
# import pandas as pd
# import datetime
# import time
# import matplotlib
# import matplotlib.dates as mdates
# import matplotlib.pyplot as plt
# from mpl_finance import candlestick_ohlc
# import csv
=======
import numpy as np
import pandas as pd
import datetime
import time
import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ohlc
import csv
plt.ion()
fig, ax = plt.subplots()
ax.set_autoscaley_on(True)

def drawbar(ndatetime,nopen,nhigh,nlow,nclose):
    candlestick2_ohlc(
        ax,
        nopen,
        nhigh,
        nlow,
        nclose,
        width=0.6,colorup='r',colordown='g',alpha=1
    )
    ax.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()
>>>>>>> 0ed7220e2a203f3cdf2905ee9a0637e33b8cd84b

<<<<<<< HEAD
# csvpf=pd.DataFrame(columns=['ndatetime','open','high','low','close','volume'])
# print('DataFrame大小: ',csvpf.shape[0])
# csvpf[['open','high','low','close','volume']]=csvpf[['open','high','low','close','volume']].astype(int)
# with open('data.csv',mode='r',newline='') as file:
#     rows=csv.reader(file)
#     for row in rows:
#         ndatetime=datetime.datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S.%f')
#         newlist=[ndatetime,int(row[1]),int(row[2]),int(row[3]),int(row[4]),int(row[5])]
#         csvpf.loc[ndatetime]=newlist

# # print(csvpf)
# csvpf= csvpf.reset_index(drop=True)
# # print(csvpf)
# csvpf['ndatetime']=csvpf['ndatetime'].map(mdates.date2num)
# # print(csvpf)
# ohlc=csvpf[['ndatetime','open','high','low','close']]
# print(ohlc)
# # fig = plt.figure()
# ax1 = plt.subplot2grid((6,1),(0,0),rowspan=5,colspan=1)
# ax1.xaxis_date()
# candlestick_ohlc(ax1,ohlc.values,width=0.02,colorup='r',colordown='g')
# plt.show()

import comtypes.client as cc
cc.GetModule(r'C:\Users\Clam\Documents\CapitalAPI\元件\x64\SKCOM.dll')
=======
csvpf=pd.DataFrame(columns=['ndatetime','open','high','low','close','volume'])
print('DataFrame大小: ',csvpf.shape[0])
csvpf[['open','high','low','close','volume']]=csvpf[['open','high','low','close','volume']].astype(int)
with open('data.csv',mode='r',newline='') as file:
    rows=csv.reader(file)
    for row in rows:
        ndatetime=datetime.datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S.%f')
        newlist=[ndatetime,int(row[1]),int(row[2]),int(row[3]),int(row[4]),int(row[5])]
        csvpf.loc[ndatetime]=newlist
        # print(csvpf)
        csvpf= csvpf.reset_index(drop=True)
        # print(csvpf)
        # csvpf['ndatetime']=csvpf['ndatetime'].map(mdates.date2num)
        # print(csvpf)
        ohlc=csvpf[['ndatetime','open','high','low','close']]
        print(ohlc)
        drawbar(ohlc['ndatetime'],ohlc['open'],ohlc['high'],ohlc['low'],ohlc['close'])
        time.sleep(1)
        # fig = plt.figure()


    




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
>>>>>>> 7b7afc3003c37eb0fb582318e9583ded57e8f2cb
