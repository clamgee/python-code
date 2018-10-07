import datetime
import time
import numpy as np
import pandas as pd

newlist=['2018/09/26','15:00:00.0005',10966,2]
contractkpd=pd.DataFrame(columns=['ndatetime','open','high','low','close','volume'])
# contractkpd=pd.DataFrame(columns=['ndatetime','open','high','low','close'])
contractkpd['ndatetime']=pd.to_datetime(contractkpd['ndatetime'])
contractkpd=contractkpd.set_index(contractkpd['ndatetime'])
# contractkpd[['open','high','low','close','volume']]=contractkpd[['open','high','low','close','volume']].astype(int)
a=datetime.datetime.strptime(newlist[0]+' '+newlist[1],'%Y/%m/%d %H:%M:%S.%f')
nlist=[a,newlist[2],newlist[2],newlist[2],newlist[2],newlist[3]]
contractkpd.loc[nlist[0]]=nlist
# contractkpd=contractkpd.append(pd.DataFrame(nlist,columns=['ndatetime','open','high','low','close','volume']),ignore_index=False)
print(contractkpd)
print(type(nlist[0]),type(nlist[1]),type(nlist[2]),type(nlist[3]),type(nlist[4]),type(nlist[5]))
print(a)


ndatetime=datetime.datetime.strptime('2018/10/06 15:00:00.053345','%Y/%m/%d %H:%M:%S.%f')
newlist=[ndatetime,10507,10507,10405,10412,50]
contractkpd.loc[newlist[0]]=newlist
# contractkpd=contractkpd.append(pd.DataFrame(newlist,columns=['ndatetime','open','high','low','close']),ignore_index=True)
ndatetime=datetime.datetime.strptime('2018/10/07 01:24:20.133','%Y/%m/%d %H:%M:%S.%f')
newlist=[ndatetime,10411,10448,10407,10443,112]
contractkpd.loc[newlist[0]]=newlist
# contractkpd=contractkpd.append(pd.DataFrame(newlist,columns=['ndatetime','open','high','low','close']),ignore_index=True)
ndatetime=datetime.datetime.strptime('2018/10/07 03:44:37.656487','%Y/%m/%d %H:%M:%S.%f')
newlist=[ndatetime,10443,10513,10436,10506,33]
contractkpd.loc[newlist[0]]=newlist
# contractkpd=contractkpd.append(pd.DataFrame(newlist,columns=['ndatetime','open','high','low','close']),ignore_index=True)
print(contractkpd.info())