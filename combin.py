import pandas as pd
import os

df=None
df1=pd.read_csv('combinfile.txt')
if 'filename.txt' not in df1['filename'].values:
    print('yes')
else :
    print('no')
print(os.path.abspath('data'))
for info in os.listdir('data'):
    domain=os.path.abspath(r'data')
    if info != 'filename.txt' and info in df1['filename'].values:
        df1=df1.append(pd.DataFrame([[info]],columns=['filename']),ignore_index=True)
        info=os.path.join(domain,info)
        print(info)
        if df is None:
            df=pd.read_csv(info,header=None)
            print(1)        
        else:        
            df=df.append(pd.read_csv(info,header=None))
            print(2)
# print(df1)
df.columns=['Date','Time','Bid','Ask','Price','Volume']
df.drop(['Bid', 'Ask'], axis=1, inplace=True)
df.to_csv('allticks.txt',index=False)
