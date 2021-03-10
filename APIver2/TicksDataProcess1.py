import pandas as pd
import os
import time

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
print(df1)
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

class Klineprocess:
    def __init__(self):
        self.contractkpd=pd.DataFrame(columns=['ndatetime','open','high','low','close','volume'])
        print('DataFrame大小: ',self.contractkpd.shape[0])
        self.contractkpd[['open','high','low','close','volume']]=self.contractkpd[['open','high','low','close','volume']].astype(int)
        self.tmpcontract=0
        self.CheckHour=0

    def contractk(self,ndatetime,nClose,nQty):
        tmphour=ndatetime.hour
        if self.contractkpd.shape[0]==0 or self.tmpcontract==0 or self.tmpcontract==12000 or (tmphour==8 and self.CheckHour==4) or (tmphour==15 and self.CheckHour==13):
            # self.contractkpd.loc[ndatetime]=[ndatetime,nClose,nClose,nClose,nClose,nQty]
            tmplist=[[ndatetime,nClose,nClose,nClose,nClose,nQty]]
            self.contractkpd=self.contractkpd.append(pd.DataFrame(tmplist,columns=['ndatetime','open','high','low','close','volume']),ignore_index=True)
            print(self.contractkpd.tail(1))
            self.tmpcontract=nQty
        elif (self.tmpcontract+nQty)>12000:
            self.contractkpd.iloc[-1,2]=max(self.contractkpd.iloc[-1,2],nClose)
            self.contractkpd.iloc[-1,3]=min(self.contractkpd.iloc[-1,3],nClose)
            self.contractkpd.iloc[-1,4]=nClose
            self.contractkpd.iloc[-1,5]=12000
            self.tmpcontract=self.tmpcontract+nQty-12000
            self.contractkpd.loc[ndatetime]=[ndatetime,nClose,nClose,nClose,nClose,self.tmpcontract]
        else:
            self.contractkpd.iloc[-1,2]=max(self.contractkpd.iloc[-1,2],nClose)
            self.contractkpd.iloc[-1,3]=min(self.contractkpd.iloc[-1,3],nClose)
            self.contractkpd.iloc[-1,4]=nClose
            self.tmpcontract=self.tmpcontract+nQty
            self.contractkpd.iloc[-1,5]=self.tmpcontract
        # self.contractkpd.reset_index(drop=True)
        self.CheckHour=tmphour
        return self.contractkpd.iloc[-1:].values

if df is not None:
    kline=Klineprocess()
    start = time.time()
    for (t,x) in df.loc[:,['ndatetime','close','volume']].iterrows():
        kline.contractk(x.ndatetime,x.close,x.volume)
    print(time.time()-start)
    kline.contractkpd.to_csv('../result.dat',header=False,index=False,mode='a')