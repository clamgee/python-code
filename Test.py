import pandas as pd
import os
df=None
# print(os.path.abspath('data'))
for info in os.listdir('data'):
    domain=os.path.abspath(r'data')
    info=os.path.join(domain,info)
    print(info)
    if df is None:
        df=pd.read_csv(info,header=None)
        print(1)
    else:        
        df=df.append(pd.read_csv(info,header=None))
        print(2)

# df = pd.read_csv('data/Ticks2019319.txt',header=None)
df[0]=df[0]+' '+df[1]
del df[1]
df[0]=pd.to_datetime(df[0],format='%Y/%m/%d %H:%M:%S.%f')
print(df.head())
print(df.shape)