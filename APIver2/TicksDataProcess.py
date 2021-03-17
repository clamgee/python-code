import pandas as pd
import os
import time
import multiprocessing as mp


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

def transformK(ndatetime,nClose,nQty):
    if kline.df is not None:
        print('有傳入值嗎: ',kline.df.tail(1),kline.df.shape[0])
    else:
        print('kline.df不存在')
    tmpcontract=0
    CheckHour=0
    tmphour=ndatetime.hour
    if kline.df.shape[0]==0 or tmpcontract==0 or tmpcontract==12000 or (tmphour==8 and CheckHour==4) or (tmphour==15 and CheckHour==13):
        # kline.df.loc[ndatetime]=[ndatetime,nClose,nClose,nClose,nClose,nQty]
        tmplist=[[ndatetime,nClose,nClose,nClose,nClose,nQty]]
        kline.df=kline.df.append(pd.DataFrame(tmplist,columns=['ndatetime','open','high','low','close','volume']),ignore_index=True)
        print(kline.df.tail(1))
        tmpcontract=nQty
    elif (tmpcontract+nQty)>12000:
        kline.df.iloc[-1,2]=max(kline.df.iloc[-1,2],nClose)
        kline.df.iloc[-1,3]=min(kline.df.iloc[-1,3],nClose)
        kline.df.iloc[-1,4]=nClose
        kline.df.iloc[-1,5]=12000
        tmpcontract=tmpcontract+nQty-12000
        kline.df.loc[ndatetime]=[ndatetime,nClose,nClose,nClose,nClose,tmpcontract]
    else:
        kline.df.iloc[-1,2]=max(kline.df.iloc[-1,2],nClose)
        kline.df.iloc[-1,3]=min(kline.df.iloc[-1,3],nClose)
        kline.df.iloc[-1,4]=nClose
        tmpcontract=tmpcontract+nQty
        kline.df.iloc[-1,5]=tmpcontract
    # kline.df.reset_index(drop=True)
    CheckHour=tmphour
    return kline.df.iloc[-1:].values


def job(x):
    print('kline.df不存在',x.ndatetime,x.close,x.volume)
    # for (t,x) in df.loc[:,['ndatetime','close','volume']].iterrows():
    res = transformK(x.ndatetime,x.close,x.volume)
        # print(t)
    return res

# def multicore(df):
#     pool = mp.Pool()
#     print('core有傳入值嗎: ',type(df),df.shape[0])
#     # pool.map(job,df)
#     # res=pool.map(job,[x for (t,x) in df.loc[:,['ndatetime','close','volume']].iterrows()
#     multi_res = [pool.apply_async(job,(x,)) for (t,x) in df.loc[:,['ndatetime','close','volume']].iterrows()]
#     print([res.get() for res in multi_res])
#     pool.close()
#     pool.join()



if __name__=='__main__':
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

    pool = mp.Pool()
    lock = mp.Lock()
    mgr = mp.Manager()
    kline = mgr.Namespace()
    dataframe = pd.DataFrame(columns=['ndatetime','open','high','low','close','volume'])
    kline.df = dataframe



    start = time.time()
    if df is not None:
        print('進入Multiprocessing',kline.df.head())
        # pool.map(job,df)
        multi_res = [pool.apply_async(job,(x,)) for (t,x) in df.loc[:,['ndatetime','close','volume']].iterrows()]
        # multicore(df)
        # print(multi_res)
        pool.close()
        pool.join()
        # print(df.tail(3))
        # p1=mp.Process(target=job,args=(df,))
        # p1.start()
        # p1.join()
    print(time.time()-start)
    if kline.df is not None:
        print(kline.df.tail(5))
    # MyFile=open('output.txt','w')
    # for element in res:
    #     MyFile.write(str(element))
    #     MyFile.write('\n')
    # MyFile.close()
    # kline.contractkpd.to_csv('../result.dat',header=False,index=False,mode='a')