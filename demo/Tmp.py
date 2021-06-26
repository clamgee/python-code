import os
import pandas as pd
import numpy as np
import time

direct=os.path.abspath('../data')
# file = os.listdir('../data')
file = 'Ticks2021-06-25.txt'
print(direct+'\\'+file)
df = pd.read_csv(direct+'\\'+file,header=None,low_memory=False)
tmpdf = df['close'].drop(index=df.index)
tmpdf.columns='close'
tmpdf.loc[0]=0
tmpdf = tmpdf.append(df.close,ignore_index=True)
tmpdf = tmpdf.reset_index(drop=True)
# tmpdf=tmpdf.drop(index=df.last_valid_index())
print(tmpdf.head(),len(tmpdf))
df['lclose']=0
df['lclose']=tmpdf.map(lambda x:x)
# testdata.map(lambda x: x if (x < 30 or x > 60) else 0) 
def dealfunc(arrLike,nBid,nAsk,nClose,nQty,lClose):
    if arrLike[nBid]==arrLike[nAsk]:
        if arrLike[lClose]!=0 and arrLike[nClose]>arrLike[lClose]:
            deal = arrLike[nQty]
        elif arrLike[lClose]!=0 and arrLike[nClose]<arrLike[lClose]:
            deal = 0-arrLike[nQty]
        else:
            deal=arrLike[nQty]
    else:
        if arrLike[lClose]!=0 and (arrLike[nClose]>arrLike[lClose] or arrLike[nClose]>=arrLike[nAsk]):
            deal = arrLike[nQty]
        elif arrLike[lClose]!=0 and (arrLike[nClose]<arrLike[lClose] or arrLike[nClose]<=arrLike[nBid]):
            deal = 0-arrLike[nQty]
        else:
            if arrLike[nClose]>=arrLike[nAsk]:
                deal=arrLike[nQty]
            else:
                deal = 0-arrLike[nQty]
    return deal
start = time.time()
df['deal']=df.apply(dealfunc,axis=1,args=('nbid','nask','close','volume','lclose'))
del df['lclose']
df.to_csv(direct+'\\'+file, header=False, index=False)
print(time.time()-start)
print(df.head())



