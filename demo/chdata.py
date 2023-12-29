import os
import pandas as pd
import time
start = time.time()
for info in os.listdir('../data'):
    # domain=os.path.abspath(r'../data')
    # info=os.path.join(domain,info)
    if info != 'filename.txt':
        info='../data/'+info
        print(info)
        df=pd.read_csv(info,header=None)
        df[0] = df[0]+' '+df[1]
        del df[1]
        df[0] = pd.to_datetime(df[0], format='%Y-%m-%d %H:%M:%S.%f')
        df.to_csv(info, header=False, index=False,mode='w')

print('time passed: ',time.time()-start)

# print(df.head())
# df.to_csv('../data/'+domain[-1], header=False, index=False,mode='w')

# domain=os.listdir('../data/')
# print(domain[-1])
# df=pd.read_csv('../data/'+domain[-1],header=None)
# print(df.head())
# df[0] = df[0]+' '+df[1]
# del df[1]
# df.columns=['ndatetime','nBid','nAsk','nClose','nQty']
# df['ndatetime'] = pd.to_datetime(df['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')

# print(df.head())
# df.to_csv('../data/'+domain[-1], header=False, index=False,mode='w')