import pandas as pd
import os
import time
# -----------宣告multiprocess
import multiprocessing as mp


def func1(row):
    if 'contractkpd' in globals() :
        pass
    else :
        global contractkpd,tmpcontract,CheckHour 
        contractkpd = pd.DataFrame(columns=['ndatetime','open','high','low','close','volume'])
        tmpcontract=0
        CheckHour=0

    # contractkpd = pd.DataFrame(columns=['ndatetime','open','high','low','close','volume'])
    tmphour=row.ndatetime.hour
    if contractkpd.shape[0]==0 or tmpcontract==0 or tmpcontract==12000 or (tmphour==8 and CheckHour==4) or (tmphour==15 and CheckHour==13):
        # contractkpd.loc[ndatetime]=[ndatetime,nClose,nClose,nClose,nClose,nQty]
        tmplist=[[row.ndatetime,row.nClose,row.nClose,row.nClose,row.nClose,row.nQty]]
        contractkpd=contractkpd.append(pd.DataFrame(tmplist,columns=['ndatetime','open','high','low','close','volume']),ignore_index=True)
        print(contractkpd.tail(1))
        tmpcontract=row.nQty
    elif (tmpcontract+row.nQty)>12000:
        contractkpd.iloc[-1,2]=max(contractkpd.iloc[-1,2],row.nClose)
        contractkpd.iloc[-1,3]=min(contractkpd.iloc[-1,3],row.nClose)
        contractkpd.iloc[-1,4]=row.nClose
        contractkpd.iloc[-1,5]=12000
        tmpcontract=tmpcontract+row.nQty-12000
        contractkpd.loc[row.ndatetime]=[row.ndatetime,row.nClose,row.nClose,row.nClose,row.nClose,tmpcontract]
    else:
        contractkpd.iloc[-1,2]=max(contractkpd.iloc[-1,2],row.nClose)
        contractkpd.iloc[-1,3]=min(contractkpd.iloc[-1,3],row.nClose)
        contractkpd.iloc[-1,4]=row.nClose
        tmpcontract=tmpcontract+row.nQty
        contractkpd.iloc[-1,5]=tmpcontract
    # contractkpd.reset_index(drop=True)
    CheckHour=tmphour
    return contractkpd

def func(df,lock):
    contractkpd = pd.DataFrame(columns=['ndatetime','open','high','low','close','volume'])
    for index ,row in df.iterrows():
        lock.acquire()
        tmphour=row.ndatetime.hour
        if contractkpd.shape[0]==0 or tmpcontract==0 or tmpcontract==12000 or (tmphour==8 and CheckHour==4) or (tmphour==15 and CheckHour==13):
            # contractkpd.loc[ndatetime]=[ndatetime,nClose,nClose,nClose,nClose,nQty]
            tmplist=[[row.ndatetime,row.nClose,row.nClose,row.nClose,row.nClose,row.nQty]]
            contractkpd=contractkpd.append(pd.DataFrame(tmplist,columns=['ndatetime','open','high','low','close','volume']),ignore_index=True)
            print(contractkpd.tail(1),'Index: ',index)
            tmpcontract=row.nQty
        elif (tmpcontract+row.nQty)>12000:
            contractkpd.iloc[-1,2]=max(contractkpd.iloc[-1,2],row.nClose)
            contractkpd.iloc[-1,3]=min(contractkpd.iloc[-1,3],row.nClose)
            contractkpd.iloc[-1,4]=row.nClose
            contractkpd.iloc[-1,5]=12000
            tmpcontract=tmpcontract+row.nQty-12000
            contractkpd.loc[row.ndatetime]=[row.ndatetime,row.nClose,row.nClose,row.nClose,row.nClose,tmpcontract]
        else:
            contractkpd.iloc[-1,2]=max(contractkpd.iloc[-1,2],row.nClose)
            contractkpd.iloc[-1,3]=min(contractkpd.iloc[-1,3],row.nClose)
            contractkpd.iloc[-1,4]=row.nClose
            tmpcontract=tmpcontract+row.nQty
            contractkpd.iloc[-1,5]=tmpcontract
        # contractkpd.reset_index(drop=True)
        CheckHour=tmphour
        lock.release()
    return contractkpd

def func2(df):
    contractkpd = pd.DataFrame(columns=['ndatetime','open','high','low','close','volume'])
    rowindex=0
    df1=df
    for index ,row in df.iterrows():
        tmphour=row.ndatetime.hour
        if contractkpd.shape[0]==0 or tmpcontract==0 or (tmphour==15 and CheckHour is None):
            # contractkpd.loc[ndatetime]=[ndatetime,nClose,nClose,nClose,nClose,nQty]
            # tmplist=[[row.ndatetime,row.nClose,row.nClose,row.nClose,row.nClose,row.nQty]]
            # contractkpd=contractkpd.append(pd.DataFrame(tmplist,columns=['ndatetime','open','high','low','close','volume']),ignore_index=True)
            contractkpd.loc[row.ndatetime]=[row.ndatetime,row.nClose,row.nClose,row.nClose,row.nClose,row.nQty]
            # print(contractkpd.tail(1),'條件1Index: ',index,'rowindex',rowindex)
            tmpcontract=row.nQty
            rowindex=index
        elif (tmpcontract+row.nQty)==12000 or (tmphour==8 and CheckHour==4) or df1.shape[0]==index+1:
            contractkpd.iloc[-1,2]=df1.iloc[rowindex:index,3].max()
            contractkpd.iloc[-1,3]=df1.iloc[rowindex:index,3].min()
            contractkpd.iloc[-1,4]=row.nClose
            contractkpd.iloc[-1,5]=tmpcontract+row.nQty
            print(contractkpd.tail(1),'條件2Index: ',index,'rowindex',rowindex)
            rowindex=index
            tmpcontract=0

        elif (tmpcontract+row.nQty)>12000:
            contractkpd.iloc[-1,2]=df1.iloc[rowindex:index,3].max()
            contractkpd.iloc[-1,3]=df1.iloc[rowindex:index,3].min()
            contractkpd.iloc[-1,4]=row.nClose
            contractkpd.iloc[-1,5]=12000
            tmpcontract=tmpcontract+row.nQty-12000
            print(contractkpd.tail(1),'條件3Index: ',index,'rowindex',rowindex)
            rowindex=index
            contractkpd.loc[row.ndatetime]=[row.ndatetime,row.nClose,row.nClose,row.nClose,row.nClose,tmpcontract]
        else:
            tmpcontract=tmpcontract+row.nQty
        CheckHour=tmphour
    contractkpd.sort_values(by=['ndatetime'],ascending=True)
    contractkpd.reset_index(inplace=True)
    return contractkpd

if __name__ == '__main__':
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

    start = time.time()
    # print(df.iloc[0:10,3])
    newdf=func2(df)
    # newdf.sort_values(by=['ndatetime'],ascending=True)

    # P = mp.Pool()
    # mg = mp.Manager()
    # ns = mg.Namespace()
    # lock = mp.Lock()
    # ns.df=df
    # tart = time.time()
    # newdf = P.starmap(func,(ns.df,lock))
    # # newdf = P.map(func1,[row for index ,row in df.iterrows()])
    # P.close()
    # P.join()
    print(newdf)
    print('執行時間: ',time.time()-start)



#-------------------------------------------------------------
# def func():
#     if df.loc[df['ndatetime']==df.ndatetime[-1:].values[0]].index[0]!=0:
#         df.tmp_nQty = df.tmp_nQty[-2:-1]+df.nQty[-1:]
#     else:
#         df.tmp_nQty = df.nQty
#     # return df.tmp_nQty

# # df['tmp_nQty']=df.apply(func)
# print('index:',df.loc[df['ndatetime']==df.ndatetime.values[0]].index[0])
