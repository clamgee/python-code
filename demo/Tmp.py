
import pandas as pd
import numpy as np
import datetime
import time
a = np.empty(shape=[0,5])
ndatetime=datetime.datetime.strptime('2021-05-14 15:00:00.054','%Y-%m-%d %H:%M:%S.%f')
lista=[]
x=0
start = time.time()
for i in range(1,10,1):
    lista.append([ndatetime,x,15750,15747,187])
    x=i+1

for row in lista:
    print(row[0])
print(type(lista[-1][0]),time.time()-start)