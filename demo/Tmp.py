from datetime import time
import numpy as np
import pandas as pd
import os
import sys
import datetime
import time
from pandas.core.frame import DataFrame

from pandas.tseries.offsets import Minute

direct=os.path.abspath('../data')
file = os.listdir('../data')
print(direct+'\\'+file[-1])
line=[]
with open(direct+'\\'+file[-1]) as file :
    lines = file.read().splitlines()
    for rows in lines:
        row=rows.split(',')
        line.append([row[0],row[1],row[2],row[3],row[4]])


# print(len(line))
# print(line[0:10])
tick2min=pd.DataFrame(line,columns=['ndatetime','nbid','nask','close','volume'])
tick2min['ndatetime']= pd.to_datetime(tick2min['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
tick2min=tick2min.sort_values(by=['ndatetime'],ascending=True)
tick2min=tick2min.reset_index(drop=True)
tick2min[['nbid','nask','close','volume']]=tick2min[['nbid','nask','close','volume']].astype(int)

df1min=pd.DataFrame(columns=['ndatetime','open','high','low','close','volume'])
df1min['ndatetime']= pd.to_datetime(df1min['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
df1min[['open','high','low','close','volume']]=df1min[['open','high','low','close','volume']].astype(int)

mm=0
mm1=0
high=0
low=0
lastidx=0
# mm=tick2min.at[0,'ndatetime'].replace(second=0,microsecond=0)+datetime.timedelta(minutes=1)
start=time.time()
for idx,row in tick2min.iterrows():
    if (idx==0 or mm==0) or row.ndatetime>=mm1:
        mm=row.ndatetime.replace(second=0,microsecond=0)
        mm1=mm+datetime.timedelta(minutes=1)
        df1min=df1min.append(pd.DataFrame([[mm,row[3],row[3],row[3],row[3],row[4]]],columns=['ndatetime','open','high','low','close','volume']),ignore_index=True,sort=False)
        high = low = row[3]
        lastidx=df1min.last_valid_index()
        # print(mm,'+','開頭')
    elif row.ndatetime < mm1 :
        df1min.at[lastidx,'close']=row[3]
        df1min.at[lastidx,'volume']+=row[4]
        if high < row[3] or low > row[3]:
            df1min.at[lastidx,'high']=high=max(high,row[3])
            df1min.at[lastidx,'low']=low=min(low,row[3])
    else:
        print('有錯誤:',mm,',',mm1,',',idx,row.ndatetime)
print('消耗: ',time.time()-start)
df1min=df1min.dropna()
data=df1min[(df1min.ndatetime.dt.hour>8) & (df1min.ndatetime.dt.hour<15)]
data=data.reset_index(drop=True)
print(data.head())
print(data.tail())
print(data.info())

