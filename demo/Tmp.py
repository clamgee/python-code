import os
import pandas as pd
import numpy as np
import time

direct=os.path.abspath('../data')
file = os.listdir('../data')
print(direct+'\\'+file[-1])
df = pd.read_csv(direct+'\\'+file[-1],header=None,names=['ndatetime','nbid','nask','close','volume'])
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
    if arrLike[lClose]!=0 and arrLike[nClose]>arrLike[lClose]:
        deal = arrLike[nQty]
    elif arrLike[lClose]!=0 and arrLike[nClose]<arrLike[lClose]:
        deal = 0-arrLike[nQty]
    else:
        deal=arrLike[nQty]
    # if arrLike[nClose] >= arrLike[nAsk]:
    #     deal = arrLike[nQty]        
    # elif arrLike[nClose] <= arrLike[nBid]:
    #     deal = 0-arrLike[nQty]        
    # else:
    #     if nClose >=nAsk:
    #         deal = nQty
    #     else:
    #         deal = 0 - nQty
    return deal
start = time.time()
df['deal']=df.apply(dealfunc,axis=1,args=('nbid','nask','close','volume','lclose'))
print(time.time()-start)
print(df.head())



