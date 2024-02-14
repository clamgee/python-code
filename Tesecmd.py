import pandas as pd
import numpy as np
import time
a=pd.DataFrame(np.zeros((5,2)),columns=['close','open'])
a=a.astype(int)
# a.loc[a.index[-1]+1]=[2,2]
b=pd.DataFrame(np.random.choice(5,(4,2)),columns=['close','open'])

# print(type(a.loc[a.index[-1]].values))

c=pd.concat([a,b],ignore_index=True)
c.loc[c.last_valid_index()+1,:]=[8,8]
print(c.columns.to_list())

# import pyqtgraph.examples
# pyqtgraph.examples.run()
# OnNewData_dict={'MarketType':{'TS':'證券','TA':'盤後','TL':'零股','TF':'期貨','TO':'選擇權','OF':'海期','OO':'海選','OS':'複委託'},
#                 'Type':{'N':'委託','C':'取消','U':'改量','P':'改價','D':'成交','B':'改價改量','S':'動態退單'},
#                 'OrderErr':{'Y':'失敗','T':'逾時','N':'正常'},
#                 'BuySell':{'TF':{'B':'買','S':'賣','Y':'當沖','N':'新倉','O':'平倉','I':'IOC','R':'ROD','F':'FOK','1':'市價','2':'限價','3':'停損','4':'停損限價','5':'收市','7':'代沖銷'}}
#                 }

# PERIODSET = dict(
#     stock = ("盤中", "盤後", "零股"),
#     future = ("ROD", "IOC", "FOK"),
#     sea_future = ("ROD"),
#     moving_stop_loss = ("IOC", "FOK"),
# )
# # print(PERIODSET['stock'])
# print(OnNewData_dict['BuySell']['TF']['B'],OnNewData_dict['BuySell']['TF']['N'],OnNewData_dict['BuySell']['TF']['R'],OnNewData_dict['BuySell']['TF']['2'])

# 持倉回報:  TF,F0200006674146,MTX08,S,1,0,10223000,50,90,0.2  次數: 0
# 持倉回報:  ##,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,  次數: 1

# import pandas as pd
# import numpy as np
# import time
# a=pd.DataFrame(np.arange(27).reshape(27),columns=['close'])
# b=pd.DataFrame(np.arange(27).reshape(27),columns=['close'])

# # a['bid']=0
# # a['ask']=0
# a['close']=a['close'].map(lambda x:10500+13-(a['close'][a['close']==x].index[0]))
# dict_bid={'bid':{10499:28,10498:30,10497:22,10496:35,10495:18},'ask':{10500:22,10501:25}}
# # a.set_index('close')
# # a['bid']=a['close'].map(dict_bid['bid']).fillna(value=0).astype(int)
# # print('1: ',a['bid'])
# a['bid']=a.set_index(['close']).update(dict_bid)
# print('2: ',a['close'].tolist())
# a['ask']=a['close'].map(dict_bid['ask']).fillna(value=0).astype(int)
# # b['close']=b['close'].map(lambda x:10505+13-(b['close'][b['close']==x].index[0]))
# # start=time.time()
# # print((a['close']!=b['close']).index.tolist())
# # end=time.time()
# # print(round((end-start),6))
# # print(dict_bid['bid'])
# # total_dict={'bid':{10500:25,10501:22},'ask':{10503:27,10504:21}}
# # print(total_dict['bid'],total_dict['ask'])
# Change=False
# bidlist=a['bid'][a['bid']!=0].index.tolist()
# if a.loc[13,'close'] != 10500 :
#     Change=True
#     print(a.loc[13,'close'],Change)
# tmplist=[15,16,17,18,19]
# if Change is True :
#     bidlist=list(set(bidlist+tmplist))
#     print(bidlist)
