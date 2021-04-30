import os
import pandas as pd
import datetime

dfMon=pd.DataFrame(columns=['ndatetime','open','high','low','close','volume'])
dfMon['ndatetime']=pd.to_datetime(dfMon['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
dfMon[['open','high','low','close','volume']]=dfMon[['open','high','low','close','volume']].astype(int)
# print(dfMon.shape)

domain=os.listdir('../data/')
checkyear=False
# print(domain[-1].strip('Ticks').strip('.txt'))
# print(ndate,type(ndate))
for info in domain:
    if info != 'filename.txt':
        ndate=datetime.datetime.strptime(info.strip('Ticks').strip('.txt'),'%Y-%m-%d').date()
        if (ndate.month==1 or ndate.month==2) and (ndate.day >= 15 and ndate.day <= 21) and ndate.weekday()>2 and checkyear == False:
            is_third_thurs = True
            checkyear = True
        else:
            is_third_thurs = (ndate.weekday() == 2 and (ndate.day >= 15 and ndate.day <= 21)) 
            if is_third_thurs and ndate.month == 1 or ndate.month == 2 :
                checkyear = True
        df1=pd.read_csv('../data/'+info,header=None)
        df1[0]=pd.to_datetime(df1[0],format='%Y-%m-%d %H:%M:%S.%f')

        if dfMon.shape[0]==0 or is_third_thurs:
            tmplist=[[df1.iloc[-1,0],df1.iloc[0,3],df1[3].max(),df1[3].min(),df1.iloc[-1,3],df1[4].sum()]]
            dfMon=dfMon.append(pd.DataFrame(tmplist,columns=['ndatetime','open','high','low','close','volume']),ignore_index=True)
            if ndate.month > 2:
                checkyear = False
        else:
            dfMon.iloc[-1,0]=df1.iloc[-1,0]
            dfMon.iloc[-1,2]=max(dfMon.iloc[-1,2],df1[3].max())
            dfMon.iloc[-1,3]=min(dfMon.iloc[-1,3],df1[3].min())
            dfMon.iloc[-1,4]=df1.iloc[-1,3]
            dfMon.iloc[-1,5]=dfMon.iloc[-1,5]+df1[4].sum()

print(dfMon.tail())
dfMon.to_csv('MonKline.dat',header=True,index=False,mode='w')
        # if is_third_thurs :
        #     print(is_third_thurs,ndate)
    


# df=pd.read_csv('../data/'+domain[-1],header=None)
# df.columns=['ndatetime','nBid','nAsk','nClose','nQty']
# df['ndatetime'] = pd.to_datetime(df['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
# df.sort_values(by=['ndatetime'],ascending=True)
# df.reset_index(drop=True)
# print(df.nClose.max(),df.nClose.min())
# print(df.iloc[-1,0].date().weekday(),datetime.datetime.today().weekday())
