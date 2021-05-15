import pandas as pd
import os
import time
# -----------宣告multiprocess
import multiprocessing as mp


def func2(df):
    contractkpd = pd.DataFrame(columns=['ndatetime','open','high','low','close','volume'])
    contractkpd['ndatetime'] = pd.to_datetime(contractkpd['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
    contractkpd[['open','high','low','close','volume']] = contractkpd[['open','high','low','close','volume']].astype(int)
    rowindex=0
    CheckHour=None
    tmpcontract=0
    dfshape=df.shape[0]
    for index ,row in df.iterrows():
        tmphour=row.ndatetime.hour
        if tmpcontract==0 or (tmphour==15 and (CheckHour is None or CheckHour==13)):
            tmplist=[[row.ndatetime,row.nClose,row.nClose,row.nClose,row.nClose,row.nQty]]
            contractkpd=contractkpd.append(pd.DataFrame(tmplist,columns=['ndatetime','open','high','low','close','volume']),ignore_index=True)
            # contractkpd.loc[row.ndatetime]=[row.ndatetime,row.nClose,row.nClose,row.nClose,row.nClose,row.nQty]
            print(contractkpd.tail(1),', 條件1 Index: ',index,' ,rowindex: ',rowindex)
            tmpcontract=row.nQty
            rowindex=index
        elif (tmpcontract+row.nQty)==12000 or (dfshape==index+1 and (tmpcontract+row.nQty)<12000) :
            contractkpd.iloc[-1,2]=df.iloc[rowindex:index,3].max()
            contractkpd.iloc[-1,3]=df.iloc[rowindex:index,3].min()
            contractkpd.iloc[-1,4]=row.nClose
            contractkpd.iloc[-1,5]=tmpcontract+row.nQty
            print(contractkpd.tail(1),', 條件2 Index: ',index,' ,rowindex: ',rowindex)
            rowindex=index
            tmpcontract=0

        elif (tmphour==8 and CheckHour==4) :
            contractkpd.iloc[-1,2]=df.iloc[rowindex+1:(index-1),3].max()
            contractkpd.iloc[-1,3]=df.iloc[rowindex+1:(index-1),3].min()
            contractkpd.iloc[-1,4]=df.iloc[(index-1),3]
            contractkpd.iloc[-1,5]=tmpcontract
            tmplist=[[row.ndatetime,row.nClose,row.nClose,row.nClose,row.nClose,tmpcontract]]
            contractkpd=contractkpd.append(pd.DataFrame(tmplist,columns=['ndatetime','open','high','low','close','volume']),ignore_index=True)
            print(contractkpd.tail(1),', 條件3 Index: ',index,' ,rowindex: ',rowindex)
            rowindex=index
            tmpcontract=row.nQty

        elif (tmpcontract+row.nQty)>12000:
            contractkpd.iloc[-1,2]=df.iloc[rowindex:index,3].max()
            contractkpd.iloc[-1,3]=df.iloc[rowindex:index,3].min()
            contractkpd.iloc[-1,4]=row.nClose
            contractkpd.iloc[-1,5]=12000
            tmpcontract=tmpcontract+row.nQty-12000
            # contractkpd.loc[row.ndatetime]=[row.ndatetime,row.nClose,row.nClose,row.nClose,row.nClose,tmpcontract]
            tmplist=[[row.ndatetime,row.nClose,row.nClose,row.nClose,row.nClose,tmpcontract]]
            contractkpd=contractkpd.append(pd.DataFrame(tmplist,columns=['ndatetime','open','high','low','close','volume']),ignore_index=True)
            print(contractkpd.tail(1),',條件4 Index: ',index,', rowindex: ',rowindex)
            rowindex=index
        else:
            tmpcontract=tmpcontract+row.nQty
        CheckHour=tmphour
    contractkpd.sort_values(by=['ndatetime'],ascending=True)
    contractkpd.reset_index(drop=True)
    return contractkpd

if __name__ == '__main__':
    # domain=os.listdir('../data/')
    # print(domain[-1])
    df=pd.read_csv('../data/Ticks2021-05-12.txt',header=None)
    df.columns=['ndatetime','nBid','nAsk','nClose','nQty']
    df['ndatetime'] = pd.to_datetime(df['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
    df.sort_values(by=['ndatetime'],ascending=True)
    df.reset_index(drop=True)
    print(df.head(5))
    print(df.info())
    print(df.nQty.sum())
    # df=df.drop(index=df.index)
    # print(df.info())
    # df.set_index('ndatetime',drop=False,inplace=True)
    # df[0]=pd.to_datetime(df[0],format='%Y-%m-%d %H:%M:%S.%f')

    start = time.time()
    # print(df.iloc[0:10,3])
    newdf=func2(df)
    newdf.sort_values(by=['ndatetime'],ascending=True)

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
    # newdf.reset_index(d)
    # print(newdf.info())
    print(newdf)
    print(newdf.volume.sum())
    # newdf.drop(newdf.index,inplace=True)
    # print(newdf.info())
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
