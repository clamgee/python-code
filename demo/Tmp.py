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


# A = dfMon.head(5)
# dfMon = dfMon.iloc[25,1:6].tolist()
# A.iloc[4,5].replace(dfMon[0],dfMon[1],dfMon[2],dfMon[3],dfMon[4],dfMon[5])
# A.iloc[4,1:5].replace(value=dfMon,inplace=True)
# for i in range(1,5):    
#     A.iloc[4,i]=dfMon.iloc[25,i]

A=dfMon[-10:].reset_index(drop=True)
start = time.time()
# A.iloc[4,5] = dfMon.iloc[25,5]
# print(A.head(5))

# A.drop(index=A.last_valid_index(),inplace=True)
A=A.append(dfMon.tail(1),ignore_index=True)
# A.iloc[4]=dfMon.iloc[25]

print(A.head(5),time.time()-start)




start = time.time()
B = dfMon[-2:]
print(B.iloc[0])
for i in range(1,5):    
    A.iloc[4,i]=B.iloc[0,i]
start = time.time()
print(A.head(5),time.time()-start)

