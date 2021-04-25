import pandas as pd
import os
import time

df=None
start = time.time()
df1=pd.read_csv('filename.txt')

def func2(df):
    df[0]=pd.to_datetime(df[0],format='%Y-%m-%d %H:%M:%S.%f')
    df.columns=['ndatetime','nbid','nask','close','volume']
    df[['nbid','nask','close','volume']]=df[['nbid','nask','close','volume']].astype(int)
    df.sort_values(by=['ndatetime'],ascending=True)
    df.reset_index(drop=True)
    contractkpd = pd.DataFrame(columns=['ndatetime','open','high','low','close','volume'])
    contractkpd['ndatetime'] = pd.to_datetime(contractkpd['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
    contractkpd[['open','high','low','close','volume']] = contractkpd[['open','high','low','close','volume']].astype(int)
    rowindex=0
    tmpcontract=0
    CheckHour=None
    dfshape=df.shape[0]
    for index ,row in df.iterrows():
        tmphour=row.ndatetime.hour
        if tmpcontract==0 or (tmphour==15 and (CheckHour is None or CheckHour==13)):
            tmplist=[[row.ndatetime,row.close,row.close,row.close,row.close,row.volume]]
            contractkpd=contractkpd.append(pd.DataFrame(tmplist,columns=['ndatetime','open','high','low','close','volume']),ignore_index=True)
            # contractkpd.loc[row.ndatetime]=[row.ndatetime,row.close,row.close,row.close,row.close,row.volume]
            print(contractkpd.tail(1),', 條件1 Index: ',index,' ,rowindex: ',rowindex)
            tmpcontract=row.volume
            rowindex=index
        elif (tmpcontract+row.volume)==12000 or (dfshape==index+1 and (tmpcontract+row.volume)<12000) :
            contractkpd.iloc[-1,2]=df.iloc[rowindex+1:index,3].max()
            contractkpd.iloc[-1,3]=df.iloc[rowindex+1:index,3].min()
            contractkpd.iloc[-1,4]=row.close
            contractkpd.iloc[-1,5]=tmpcontract+row.volume
            print(contractkpd.tail(1),', 條件2 Index: ',index,' ,rowindex: ',rowindex)
            rowindex=index
            tmpcontract=0
        
        elif (tmphour==8 and CheckHour==4) :
            contractkpd.iloc[-1,2]=df.iloc[rowindex+1:(index-1),3].max()
            contractkpd.iloc[-1,3]=df.iloc[rowindex+1:(index-1),3].min()
            contractkpd.iloc[-1,4]=df.iloc[(index-1),3]
            contractkpd.iloc[-1,5]=tmpcontract
            rowindex=index
            tmpcontract=row.volume
            tmplist=[[row.ndatetime,row.close,row.close,row.close,row.close,tmpcontract]]
            contractkpd=contractkpd.append(pd.DataFrame(tmplist,columns=['ndatetime','open','high','low','close','volume']),ignore_index=True)
            print(contractkpd.tail(1),', 條件3 Index: ',index,' ,rowindex: ',rowindex)

        elif (tmpcontract+row.volume)>12000:
            contractkpd.iloc[-1,2]=df.iloc[rowindex:index,3].max()
            contractkpd.iloc[-1,3]=df.iloc[rowindex:index,3].min()
            contractkpd.iloc[-1,4]=row.close
            contractkpd.iloc[-1,5]=12000
            tmpcontract=tmpcontract+row.volume-12000
            rowindex=index
            # contractkpd.loc[row.ndatetime]=[row.ndatetime,row.close,row.close,row.close,row.close,tmpcontract]
            tmplist=[[row.ndatetime,row.close,row.close,row.close,row.close,tmpcontract]]
            contractkpd=contractkpd.append(pd.DataFrame(tmplist,columns=['ndatetime','open','high','low','close','volume']),ignore_index=True)
            print(contractkpd.tail(1),',條件4 Index: ',index,', rowindex: ',rowindex)
        else:
            tmpcontract=tmpcontract+row.volume
        CheckHour=tmphour
    contractkpd.sort_values(by=['ndatetime'],ascending=True)
    contractkpd.reset_index(drop=True)
    return contractkpd

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
            df=pd.read_csv(info,header=None)
            print(2)
        contractkpd=func2(df)
        contractkpd.to_csv('../result.dat',header=False,index=False,mode='a')

print(df1)
df1.to_csv('filename.txt',index=False)
if df is not None:
    print('done!!')
else:
    print('No Data UpDate!!')

print(time.time()-start,'秒')