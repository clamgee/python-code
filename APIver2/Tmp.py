import pandas as pd
import os
import time
import multiprocessing as mp

df=None
df1=pd.read_csv('filename.txt')
if 'filename.txt' not in df1['filename'].values:
    print('yes')
else :
    print('no')
print(os.path.abspath('../data'))
for info in os.listdir('../data'):
    domain=os.path.abspath(r'../data')
    if info not in df1['filename'].values:
        df1=df1.append(pd.DataFrame([[info]],columns=['filename']),ignore_index=True)
        info=os.path.join(domain,info)
        print(info)
        if df is None:
            df=pd.read_csv(info,header=None)
            print(1)        
        else:        
            df=df.append(pd.read_csv(info,header=None))
            print(2)
print(df1.tail(5))
df1.to_csv('filename.txt',index=False)
if df is not None:
    df[0]=df[0]+' '+df[1]
    del df[1]
    df[0]=pd.to_datetime(df[0],format='%Y-%m-%d %H:%M:%S.%f')
    df.columns=['ndatetime','nbid','nask','close','volume']
    print(df.head())
    print(df.shape)
    df.sort_values(by=['ndatetime'],ascending=True)
else:
    # df=pd.read_csv('result.dat')
    # print(df['ndatetime'].tail(5))
    # df['ndatetime']=pd.to_datetime(df['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
    # print(df.tail(5))
    # df.sort_values(by=['ndatetime'],ascending=True)
    print('No Data UpDate!!')

if df is not None:
    print(df['volume'].)