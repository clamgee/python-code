import pandas as pd
import numpy as np
import datetime
import time
import csv
import gc
start=time.time()
csvpd=pd.DataFrame(columns=['date','time','close','volume'])
global microsec
microsec=0.0000
global lasttime
lasttime=''
with open('Daily_2018_10_08.csv',mode='r',newline='') as file:
    rows=csv.reader(file)
    for row in rows:
        if row[1].strip()=='TX' and row[2].strip()=='201810':
            #成交日期,商品代號,到期月份(週別),成交時間,成交價格,成交數量(B+S),近月價格,遠月價格,開盤集合競價 
            row[0]=datetime.datetime.strptime(str(row[0]).strip(),'%Y%m%d').strftime('%Y/%m/%d')
            if row[3].strip() != lasttime :
                lasttime=row[3].strip()
                microsec=0.0000
                row[3]=datetime.datetime.strptime(row[3].strip(),'%H%M%S').strftime('%H:%M:%S')+'.0000'
            else:
                microsec+=0.0001
                row[3]=datetime.datetime.strptime(row[3].strip(),'%H%M%S').strftime('%H:%M:%S')+str(microsec)[1:6]
            #print(type(row[0]),type(row[3]),type(row[4]),type(row[5]))
            newlist=[[row[0],row[3],row[4].strip(),row[5].strip()]]
            csvpd=csvpd.append(pd.DataFrame(newlist,columns=['date','time','close','volume']),ignore_index=True)

print(csvpd.head())
csvpd.to_csv('output.csv',index=False)
gc.set_threshold(700, 10, 5)
end=time.time()
elapsed = end - start
print('運行時間: ',elapsed)