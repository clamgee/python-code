import pandas as pd
# import modin.pandas as pd
import numpy as np
import datetime
import time
import csv
import gc

start = time.time()
# 修改要抓期交所資料的檔案，手動修改檔案名稱
df = pd.read_csv('Daily_2025_01_21.csv', encoding='big5',low_memory=False)# error_bad_lines=False, warn_bad_lines=True)
df.rename(columns={
    df.columns[0]: 'ndate',
    df.columns[1]: 'product',
    df.columns[2]: 'Month',
    df.columns[3]: 'ntime',
    df.columns[4]: 'price',
    df.columns[5]: 'volume',
    df.columns[6]: 'lastmon',
    df.columns[7]: 'farmon',
    df.columns[8]: 'open'
}, inplace=True)
df.drop(['lastmon', 'farmon', 'open'], axis=1, inplace=True)
df = df[df['product'].str.strip() == 'TX']  # 目標商品
df = df[df['Month'].str.strip() == '202502']  # 手動修改目標月份
df[['ndate', 'ntime']] = df[['ndate', 'ntime']].astype(str)
df.drop(['product', 'Month'], axis=1, inplace=True)

def fx(x):
    return x.zfill(6) + '.001'

df.ntime = df.ntime.apply(fx)

df.price = df.price.astype(int)
df['nbid'] = df['price']
df['nask'] = df['price']
df = df[['ndate', 'ntime', 'nbid', 'nask', 'price', 'volume']]
df['ndate']=df['ndate']+' '+df['ntime']
del df['ntime']
df['ndate']=pd.to_datetime(df['ndate'],format='%Y%m%d %H%M%S.%f')
# df['ndate']=pd.to_datetime(df['ndate'],format='%Y-%m-%d %H:%M:%S.%f')

df.sort_values(by=['ndate'],ascending=True)
df = df.reset_index(drop=True)
# -----處理多空力道
df['diff_close']=df.price - df.price.shift(1).fillna(df.price)

def dealfunc(arrLike,nQty,diff_close):
    if arrLike[diff_close] > 0 :
        deal = arrLike[nQty]
    elif arrLike[diff_close] < 0:
        deal = 0-arrLike[nQty]
    else:
        deal=0
    return deal
start = time.time()
df['deal']=df.apply(dealfunc,axis=1,args=('volume','diff_close'))
del df['diff_close']
print(df.columns.values)
print(df.shape)
print(df.info())
print(df.head(5))
filename = 'data/Ticks' + str(df.iloc[-1, 0].date()) + '.txt'
print(filename)
df.to_csv(filename, header=False, index=False)
end = time.time()
print('耗時: ', round((end - start), 3), ' 秒')
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
