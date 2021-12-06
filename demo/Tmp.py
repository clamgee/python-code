
import numpy as np
import pandas as pd
import os
import datetime

# Candledf=pd.read_csv('../result.dat',low_memory=False)
# Candledf['ndatetime']=pd.to_datetime(Candledf['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
# laxtidx = Candledf.last_valid_index()
# print(Candledf.at[laxtidx,'ndatetime'].time().strftime('%H:%M:%S.%f'))
# print(type(Candledf.at[laxtidx,'ndatetime'].time().strftime('%H:%M:%S.%f')))
direct=os.path.abspath('../data')
filelist = os.listdir('../data')
file = filelist[-1]
print(file)
dayticks = pd.read_csv(direct+'\\'+file,header=None,names=['ndatetime','nbid','nask','close','volume','deal'])
dayticks['ndatetime'] = pd.to_datetime(dayticks['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
dayticks.sort_values(by=['ndatetime'],ascending=True)
print(dayticks.at[73196,'ndatetime'].time().strftime('%H:%M:%S'))