import pandas as pd
import numpy as np
import time

from pandas.core import series
bestfive = pd.DataFrame(np.arange(24).reshape(6,4), columns=['bidQty','nbid','nask','askQty'])
# bestfive = bestfive.astype(int)
bestfive[['bidQtyitem','nbiditem','naskitem','askQtyitem']]=''
total_dict={'bidQty':{0:11,1:12,2:13,3:14,4:15,5:0},'nbid':{0:int(21),1:int(22),2:int(23),3:int(24),4:int(25),5:int(1000)},'nask':{0:30,1:30,2:30,3:30,4:30,5:0},'askQty':{0:40,1:40,2:40,3:40,4:40,5:200}}
# total_dict = {'a':10,'b':20,'c':30,'d':40,'e':50}
start = time.time()

bestfive[['bidQty','nbid','nask','askQty']] = pd.DataFrame.from_dict(total_dict)

# for col in bestfive[['bidQty','nbid','nask','askQty']].columns:
#     # print(bestfive[col][bestfive[col]==21].index[0])
#     # bestfive[col] = bestfive[col].map(lambda x : total_dict[col][x[0]])
#     bestfive[col] = bestfive[col].map(lambda x : total_dict[col][bestfive[col][bestfive[col]==x].index[0]])


reslt=time.time()-start
print(bestfive)
# print(total_dict['nbid'][bestfive['nbid'][bestfive['nbid']==9].index[0]])
# print(type(bestfive['nbid'][bestfive['nbid']==9].index[0]))

print(reslt)

# print(bestfive.info())