import pandas as pd
import datetime
A=list('abcdefg')
print(A.pop(0))
print(A)

# tmp = pd.read_csv('../result.dat')
# tmp['ndatetime'] = pd.to_datetime(tmp['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
# # tmp['high_avg'] =0
# # tmp[['high_avg']]=tmp[['high_avg']].astype(int)
# tmp['high_avg'] = tmp.high.rolling(20).mean().round(0).astype(int)
# # print(tmp.loc[tmp['volume']!=12000 & tmp['ndatetime'].values.hour()>8])
# print(tmp.tail())
# print(tmp.info())