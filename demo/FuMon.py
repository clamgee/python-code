import os
import pandas as pd
import datetime



domain=os.listdir('../data/')
print(domain[-2:-1][0])
df=pd.read_csv('../data/'+domain[-2:-1][0],header=None)
df.columns=['ndatetime','nBid','nAsk','nClose','nQty']
df['ndatetime'] = pd.to_datetime(df['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
df.sort_values(by=['ndatetime'],ascending=True)
df.reset_index(drop=True)
print(df.nClose.max(),df.nClose.min())
print(df.iloc[-1,0].date().weekday(),datetime.datetime.today().weekday())

is_third_thurs = df.iloc[-1,0].date().weekday() == 2 and df.iloc[-1,0].date().day >= 15 and df.iloc[-1,0].date().day <= 21 
print(is_third_thurs)