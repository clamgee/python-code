import pandas as pd
import numpy as np
import time
df = pd.DataFrame(columns=['close','volume'])
df1 = pd.DataFrame(columns=['close','volume'])
start = time.time()
for i in range(0,1000,1):
    df.at[i,'close']= i
    df.at[i,'volume']= i+5
print(df.tail(),df.shape[0])
print(time.time()-start)

start = time.time()
for i in range(0,1000,1):
    df1=df1.append(pd.DataFrame([[i,i+5]],columns=['close','volume']),ignore_index=True)
print(df1.tail(),df1.shape[0])
print(time.time()-start)
print(df.at[1:50,'close'])