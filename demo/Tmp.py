import pandas as pd
import time

dfMon = pd.read_csv('MonKline.dat')

dfMon['ndatetime'] = pd.to_datetime(dfMon['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
# print(dfMon.head(5))
# print(dfMon.tail(5),dfMon.last_valid_index())
A = dfMon.head(5)
# A.pop(1)
# A=A.append(dfMon.tail(1))
# A.loc[A.last_valid_index()]=dfMon.loc[dfMon.last_valid_index()].values.tolist()
A.iloc[-1:]=dfMon.tail(1).values.tolist()
# [-1:,0:6] = dfMon.iloc[-1:,0:6]
print(A)
# print(A.loc[A.last_valid_index()])
# print(dfMon.tail(1).values.tolist())
# print(np.datetime64('2019-04-16 13:44:59.765'))



A = dfMon.tail(2)
# print(A.iloc[A.index==24,0].shape[1])
print(A.shape[1])
# tmp = dfMon.iloc[25,1:6].tolist()
# A.iloc[4,5].replace(tmp[0],tmp[1],tmp[2],tmp[3],tmp[4],tmp[5])
# A.iloc[4,1:5].replace(value=tmp,inplace=True)
# for i in range(1,5):    
#     A.iloc[1,i]=dfMon.iloc[25,i]
# B=dfMon.tail(2)
# start = time.time()
# A.drop(index=A.last_valid_index(),inplace=True)
# A=A.append(dfMon.tail(1),ignore_index=True)
# A.iloc[4]=dfMon.iloc[25]
# print(A,time.time()-start)

start = time.time()
col = dfMon.columns.tolist()
# A.at[A.index==24]=dfMon[dfMon.index==25]
for row in col:
    A.at[24,row]=dfMon.at[0,row]

print(A,col,time.time()-start)

