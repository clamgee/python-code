import pandas as pd
import numpy as np
import datetime
import time
import gc

start=time.time() 
#成交日期,商品代號,到期月份(週別),成交時間,成交價格,成交數量(B+S),近月價格,遠月價格,開盤集合競價 
title=['date','product','mon','time','close','volume','unuse1','unuse2','unuse3']
#以DataFrame資料型態讀取CSV
data=pd.read_csv('data.txt',low_memory=False)
#設定DataFrame欄位名稱
data.columns=title
#先行去掉無用欄位
data=data.drop(columns=['unuse1','unuse2','unuse3'])
#欄位資料型態轉換
data['product']=data['product'].map(str.strip)
data['date']=data['date'].astype(str)
data['close']=data['close'].astype(np.int64)
data['mon']=data['mon'].astype(str).map(str.strip)
data['time']=data['time'].astype(str).map(str.strip)
#比對欄位資料並選取所需資料
data=data[data['product']=='TX']
data=data[data['mon']=='201809']
#再將無用欄位去除
data=data.drop(columns=['product','mon'])
#重新設定DataFrame的索引
data.reset_index(drop=True, inplace=True)
#增加微秒全域變數
global microsec
microsec=0.0000
#修改每筆日期與時間資料
for index,row in data.iterrows():
    #修改日期格式YYYY/MM/DD
    data.loc[index,'date']=datetime.datetime.strptime(row['date'],'%Y%m%d').strftime('%Y/%m/%d').strip()
    #補足時間長度，修改時間格式(字串)HH:MM:SS
    while len(row['time'])<6:
        row['time']='0'+row['time']
    data.loc[index,'time']=datetime.datetime.strptime(row['time'],'%H%M%S').strftime('%H:%M:%S')
    #比對相同時間，增加微秒
    if index != 0 and data.loc[index-1,'time'][0:8]==data.loc[index,'time'][0:8]:
        microsec+=0.0001
        data.loc[index,'time']=data.loc[index,'time']+str(microsec)[1:]
    else:
        microsec=0.0000
    #秒數字串過長，取到小數點4位數
    if len(data.loc[index,'time'])>13:
        data.loc[index,'time']=data.loc[index,'time'][:13]
    print(index)

#print(data.head())
#寫入檔案
data.to_csv('newcvs.csv',index=False)
#清除使用記憶體
gc.set_threshold(700, 10, 5) 
end=time.time()
elapsed = end - start
print('運行時間: ',elapsed)