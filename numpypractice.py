# import datetime
# import pandas as pd
# tmplist=[]
# ticksdf=pd.DataFrame(columns=['ndate','ntime','nbid','nask','close','volume'])
# ticksdf['ndate']=pd.to_datetime(ticksdf['ndate'],format='%Y-%m-%d')
# ticksdf['ntime']=pd.to_datetime(ticksdf['ntime'],format='%H:%M:%S.%f')
# tmplist.append(datetime.datetime.now().date())
# tmplist.append(datetime.datetime.now().time())
# tmplist=[tmplist+[1,2,3,4]]
# print(len(tmplist))
# ticksdf=ticksdf.append(pd.DataFrame(tmplist,columns=['ndate','ntime','nbid','nask','close','volume']),ignore_index=True)
# print(ticksdf.head())
# print(ticksdf.info())
# import datetime
# ndate=datetime.datetime.today()
# sTime=datetime.datetime.now().time()
# ndatetime=datetime.datetime.combine(ndate,sTime)
# print(ndatetime)
import pyqtgraph.examples
pyqtgraph.examples.run()