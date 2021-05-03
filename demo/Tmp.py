import numpy as np
import pandas as pd

tmp = pd.read_csv('MonKline.dat')

tmp['ndatetime'] = pd.to_datetime(tmp['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
print(tmp.head(5))
tmp=tmp.drop(columns=['open','high','low'])
print(tmp.tail(5),tmp.last_valid_index())
# print(np.datetime64('2019-04-16 13:44:59.765'))

# def strtodate(x):
#     print(x)
#     return np.datetime64(x)

# np1 = np.genfromtxt('MonKline.dat', delimiter=',',usecols=(0,1),skip_header=1,converters={0:strtodate},dtype='M8,f8')
# print(np1)