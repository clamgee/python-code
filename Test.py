import datetime
import time
import numpy as np
import pandas as pd

# newlist=['2018/09/26','15:00:00.0005',10966,2]
# contractkpd=pd.DataFrame(columns=['ndatetime','open','high','low','close','volume'])
# contractkpd['ndatetime']=pd.to_datetime(contractkpd['ndatetime'])
# contractkpd=contractkpd.set_index(contractkpd['ndatetime'])
# contractkpd[['open','high','low','close','volume']]=contractkpd[['open','high','low','close','volume']].astype(int)
# a=datetime.datetime.strptime(newlist[0]+' '+newlist[1],'%Y/%m/%d %H:%M:%S.%f')
# nlist=[a,newlist[2],newlist[2],newlist[2],newlist[2],newlist[3]]
# contractkpd.loc['ndatetime']=nlist
# # csvpd=csvpd.append(pd.DataFrame(newlist,columns=['date','time','close','volume']),ignore_index=True)
# print(contractkpd)
# print(type(nlist[0]),type(nlist[1]),type(nlist[2]),type(nlist[3]),type(nlist[4]),type(nlist[5]))
# print(a)
df=pd.read_csv('data.csv')
df.iloc[-1,2]=df.iloc[-1,2]+2
print(df.iloc[-1:].values)