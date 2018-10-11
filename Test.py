import numpy as np
import pandas as pd
import datetime
import time
import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import csv

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
csvpf['ndatetime']=csvpf['ndatetime'].map(mdates.date2num)
# print(csvpf)
ohlc=csvpf[['ndatetime','open','high','low','close']]
print(ohlc)
# fig = plt.figure()
ax1 = plt.subplot2grid((6,1),(0,0),rowspan=5,colspan=1)
ax1.xaxis_date()
candlestick_ohlc(ax1,ohlc.values,width=0.02,colorup='r',colordown='g')
plt.show()