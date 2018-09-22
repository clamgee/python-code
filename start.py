# import mathmethod
# result1=mathmethod.square(2,2)
# result2=mathmethod.rate(1,1,7,28)
# print(result1,",",result2)
# import datetime
# import time
# newdate=datetime.datetime.strptime('20180905','%Y%m%d').strftime('%Y/%m/%d')
# newtime=datetime.datetime.strptime('084500','%H%M%S').strftime('%H:%M:%S')
# print(newdate,newtime,type(newtime))
#from numba import jit
import csv
import time
start=time.time()
# jit decorator tells Numba to compile this function.
# The argument types will be inferred by Numba when function is called.
with open('Daily_2018_09_06.csv',mode='r',newline='') as newfile:
    rows=csv.reader(newfile)
    for row in rows:
        print(row[0].strip())

end=time.time()
elapsed = end - start
print('運行時間: ',elapsed)