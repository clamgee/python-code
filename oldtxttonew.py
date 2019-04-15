import pandas as pd
import os
df=None
df1=pd.read_csv('tmp/filename.txt')
if 'filename1.txt' not in df1['filename'].values:
    print('yes')
else :
    print('no')
print(os.path.abspath('tmp'))
domain=os.path.abspath(r'tmp')
domain1=os.path.abspath(r'data')
for info in os.listdir('tmp'):
    if info not in df1['filename'].values:
        df1=df1.append(pd.DataFrame([[info]],columns=['filename']),ignore_index=True)
        info=os.path.join(domain,info)
        print(info)
        df=pd.read_csv(info,header=None)
        df[0]=pd.to_datetime(df[0],format='%Y-%m-%d').dt.date
        if len(str(df.iloc[1,1]))==8:
            df[1]=pd.to_datetime(df[1],format='%H:%M:%S').dt.time
        else:
            df[1]=pd.to_datetime(df[1],format='%H:%M:%S.%f').dt.time
        df.columns=['date','time','close','volume']
        df['nbid']=df['close']
        df['nask']=df['close']
        df=df[['date','time','nbid','nask','close','volume']]
        filename='Ticks'+str(df.iloc[-1,0])+'.txt'
        filename=os.path.join(domain1,filename)
        df.to_csv(filename,header=False,index=False)
        df.drop(df.index,inplace=True)
        df1.to_csv('tmp/filename.txt',index=False)     
print(df1)
