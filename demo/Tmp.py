import pandas as pd
import time

dfMon = pd.read_csv('MonKline.dat')

<<<<<<< HEAD
tmp['ndatetime'] = pd.to_datetime(tmp['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
# print(tmp.head(5))
# print(tmp.tail(5),tmp.last_valid_index())
A = tmp.head(5)
# A.pop(1)
# A=A.append(tmp.tail(1))
# A.loc[A.last_valid_index()]=tmp.loc[tmp.last_valid_index()].values.tolist()
A.iloc[-1:]=tmp.tail(1).values.tolist()
# [-1:,0:6] = tmp.iloc[-1:,0:6]
print(A)
# print(A.loc[A.last_valid_index()])
# print(tmp.tail(1).values.tolist())
# print(np.datetime64('2019-04-16 13:44:59.765'))
=======
dfMon['ndatetime']=pd.to_datetime(dfMon['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
dfMon[['open','high','low','close','volume']]=dfMon[['open','high','low','close','volume']].astype(int)
>>>>>>> 17d936e248d146aa77d1813c48dfd208ce8fbf3b


A = dfMon.head(5)
# tmp = dfMon.iloc[25,1:6].tolist()
# A.iloc[4,5].replace(tmp[0],tmp[1],tmp[2],tmp[3],tmp[4],tmp[5])
# A.iloc[4,1:5].replace(value=tmp,inplace=True)
# for i in range(1,5):    
#     A.iloc[4,i]=dfMon.iloc[25,i]
B=dfMon.tail(2)
start = time.time()
A.drop(index=A.last_valid_index(),inplace=True)
A=A.append(dfMon.tail(1),ignore_index=True)
A.iloc[4]=dfMon.iloc[25]
print(A,time.time()-start)

start = time.time()
print(B.iloc[0])
for i in range(1,5):    
    A.iloc[4,i]=B.iloc[0,i]
start = time.time()
print(A,time.time()-start)

