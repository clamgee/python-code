import pandas as pd
import os

domain=os.listdir('../data/')
print(domain[-1])
tmp=pd.read_csv('../data/'+domain[-1])
tmp.rename(columns={
    tmp.columns[0]: 'ndate',
    tmp.columns[1]: 'ntime',
    tmp.columns[2]: 'nbid',
    tmp.columns[3]: 'nask',
    tmp.columns[4]: 'close',
    tmp.columns[5]: 'volume',
}, inplace=True)
# print(tmp.tail(5))

print(tmp.volume.cumsum())