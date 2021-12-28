
import numpy as np
import pandas as pd
import os
import datetime
import APIver3.Config_dict as Config_dict

print(Config_dict['BuySell'])

# Candledf=pd.read_csv('../result.dat',low_memory=False)
# Candledf['ndatetime']=pd.to_datetime(Candledf['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
# laxtidx = Candledf.last_valid_index()
# print(Candledf.at[laxtidx,'ndatetime'].time().strftime('%H:%M:%S.%f'))
# print(type(Candledf.at[laxtidx,'ndatetime'].time().strftime('%H:%M:%S.%f')))

# direct=os.path.abspath('../data')
# filelist = os.listdir('../data')
# file = filelist[-1]
# print(file)
# dayticks = pd.read_csv(direct+'\\'+file,header=None,names=['ndatetime','nbid','nask','close','volume','deal'])
# dayticks['ndatetime'] = pd.to_datetime(dayticks['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
# dayticks.sort_values(by=['ndatetime'],ascending=True)
# # print(dayticks.at[300,'ndatetime'].time().strftime('%H:%M'))
# # dayticks=dayticks[(dayticks.ndatetime.dt.hour>=8) & (dayticks.ndatetime.dt.hour<15)]
# dayticks=dayticks[(dayticks.ndatetime.dt.hour>14) | (dayticks.ndatetime.dt.hour<8)]
# dayticks.index = dayticks.ndatetime
# Candledf=dayticks['close'].resample('1min',closed='right').ohlc()
# tmpdf=dayticks['volume'].resample('1min').sum()
# Candledf=pd.concat([Candledf,tmpdf],axis=1)
# del tmpdf
# tmpdf=dayticks['deal'].resample('1min').sum()
# Candledf=pd.concat([Candledf,tmpdf],axis=1)
# del tmpdf
# Candledf['dealcumsum']=Candledf['deal'].cumsum()
# del Candledf['deal']
# Candledf.rename(columns={'dealcumsum':'deal'},inplace=True)
# Candledf=Candledf.rename_axis('ndatetime').reset_index()
# Candledf['ndatetime'] = pd.to_datetime(Candledf['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
# Candledf.sort_values(by=['ndatetime'],ascending=True)
# state = Candledf.loc[295,:]
# print(state['ndatetime'].time().strftime('%H:%M:%S'))