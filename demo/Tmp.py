import pandas as pd
import os
import time
domain=os.listdir('../data/')
print(domain[-1])
df=pd.read_csv('../data/'+domain[-1])
df.rename(columns={
    df.columns[0]: 'ndate',
    df.columns[1]: 'ntime',
    df.columns[2]: 'nBid',
    df.columns[3]: 'nAsk',
    df.columns[4]: 'nClose',
    df.columns[5]: 'nQty',
}, inplace=True)
df['ndate'] = df['ndate']+' '+df['ntime']
del df['ntime']
df.columns=['ndatetime','nBid','nAsk','nClose','nQty']
df['ndatetime'] = pd.to_datetime(df['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
df.sort_values(by=['ndatetime'],ascending=True)
# df.set_index('ndatetime',drop=False,inplace=True)
# df[0]=pd.to_datetime(df[0],format='%Y-%m-%d %H:%M:%S.%f')
tmpcontract=0
CheckHour=0
start = time.time()
contractkpd = pd.DataFrame(columns=['ndatetime','open','high','low','close','volume'])
    # return contractkpd.iloc[-1:].values
print('1:',df.nQty.tail(2)[-1:])
print('2:',df.nQty.tail(2)[-2:-1])
def func():
    if df.nQty[-2:-1] is True:
        if   < 120000:
            return 

df['2vol']=df.volume.apply(func)
print(str(time.time()-start)+'秒')
print(contractkpd.head())

# for index ,row in df.iterrows():
#     tmphour=row.ndatetime.hour
#     if contractkpd.shape[0]==0 or tmpcontract==0 or tmpcontract==12000 or (tmphour==8 and CheckHour==4) or (tmphour==15 and CheckHour==13):
#         # contractkpd.loc[ndatetime]=[ndatetime,nClose,nClose,nClose,nClose,nQty]
#         tmplist=[[row.ndatetime,row.nClose,row.nClose,row.nClose,row.nClose,row.nQty]]
#         contractkpd=contractkpd.append(pd.DataFrame(tmplist,columns=['ndatetime','open','high','low','close','volume']),ignore_index=True)
#         print(contractkpd.tail(1))
#         tmpcontract=row.nQty
#     elif (tmpcontract+row.nQty)>12000:
#         contractkpd.iloc[-1,2]=max(contractkpd.iloc[-1,2],row.nClose)
#         contractkpd.iloc[-1,3]=min(contractkpd.iloc[-1,3],row.nClose)
#         contractkpd.iloc[-1,4]=row.nClose
#         contractkpd.iloc[-1,5]=12000
#         tmpcontract=tmpcontract+row.nQty-12000
#         contractkpd.loc[row.ndatetime]=[row.ndatetime,row.nClose,row.nClose,row.nClose,row.nClose,tmpcontract]
#     else:
#         contractkpd.iloc[-1,2]=max(contractkpd.iloc[-1,2],row.nClose)
#         contractkpd.iloc[-1,3]=min(contractkpd.iloc[-1,3],row.nClose)
#         contractkpd.iloc[-1,4]=row.nClose
#         tmpcontract=tmpcontract+row.nQty
#         contractkpd.iloc[-1,5]=tmpcontract
#     # contractkpd.reset_index(drop=True)
#     CheckHour=tmphour