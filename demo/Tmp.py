import pandas as pd
import os

domain=os.listdir('../data/')
print(domain[-1])
df=pd.read_csv('../data/'+domain[-1])
df.rename(columns={
    df.columns[0]: 'ndate',
    df.columns[1]: 'ntime',
    df.columns[2]: 'nbid',
    df.columns[3]: 'nask',
    df.columns[4]: 'close',
    df.columns[5]: 'volume',
}, inplace=True)
df['ndate'] = df['ndate']+' '+df['ntime']
del df['ntime']
df.columns=['ndatetime','nbid','nask','close','volume']
df['ndatetime'] = pd.to_datetime(df['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
df.sort_values(by=['ndatetime'],ascending=True)
# df.set_index('ndatetime',drop=False,inplace=True)
# df[0]=pd.to_datetime(df[0],format='%Y-%m-%d %H:%M:%S.%f')
A=0
for index ,row in df.iterrows():
    A += row.volume
    if A >= 12000:
        print(row.ndatetime)
        A = 0
    
print(df.head())