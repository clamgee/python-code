import pandas as pd
import numpy as np
import datetime
import time
import csv
import gc

df=pd.read_csv('Daily_2019_04_03.csv',encoding='big5',error_bad_lines=False,warn_bad_lines=True)
df.rename(columns={
    df.columns[0]:'ndate',
    df.columns[1]:'product',
    df.columns[2]:'Month',
    df.columns[3]:'ntime',
    df.columns[4]:'price',
    df.columns[5]:'volumn',
    df.columns[6]:'lastmon',
    df.columns[7]:'farmon',
    df.columns[8]:'open'
},inplace=True)
df.drop(['lastmon','farmon','open'],axis=1,inplace=True)
df=df[df['product'].str.strip()=='TX']
df=df[df['Month'].str.strip()=='201904']
# df['ndate']=df['ndate'].str.strip()+' '+df['ntime'].str.strip()
print(df.columns.values)
print(df.shape)
print(df.head(5))

# start=time.time()
# csvpd=pd.DataFrame(columns=['date','time','close','volume'])
# global microsec
# microsec=0.0000
# global lasttime
# lasttime=''
# with open('Daily_2019_03_21.csv',mode='r',newline='') as file:
#     rows=csv.reader(file)
#     for row in rows:
#         if row[1].strip()=='TX' and row[2].strip()=='201904':
#             #成交日期,商品代號,到期月份(週別),成交時間,成交價格,成交數量(B+S),近月價格,遠月價格,開盤集合競價 
#             row[0]=datetime.datetime.strptime(str(row[0]).strip(),'%Y%m%d').strftime('%Y/%m/%d')
#             if row[3].strip() != lasttime :
#                 lasttime=row[3].strip()
#                 microsec=0.0000
#                 row[3]=datetime.datetime.strptime(row[3].strip(),'%H%M%S').strftime('%H:%M:%S')+'.0000'
#             else:
#                 microsec+=0.0001
#                 row[3]=datetime.datetime.strptime(row[3].strip(),'%H%M%S').strftime('%H:%M:%S')+str(microsec)[1:6]
#             #print(type(row[0]),type(row[3]),type(row[4]),type(row[5]))
#             newlist=[[row[0],row[3],row[4].strip(),row[5].strip()]]
#             csvpd=csvpd.append(pd.DataFrame(newlist,columns=['date','time','close','volume']),ignore_index=True)

# print(csvpd.head())
# csvpd.to_csv('output.csv',index=False)
# gc.set_threshold(700, 10, 5)
# end=time.time()
# elapsed = end - start
# print('運行時間: ',elapsed)