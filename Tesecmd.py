# import pyqtgraph.examples
# pyqtgraph.examples.run()
OnNewData_dict={'MarketType':{'TS':'證券','TA':'盤後','TL':'零股','TF':'期貨','TO':'選擇權','OF':'海期','OO':'海選','OS':'複委託'},
                'Type':{'N':'委託','C':'取消','U':'改量','P':'改價','D':'成交','B':'改價改量','S':'動態退單'},
                'OrderErr':{'Y':'失敗','T':'逾時','N':'正常'},
                'BuySell':{'TF':{'B':'買','S':'賣','Y':'當沖','N':'新倉','O':'平倉','I':'IOC','R':'ROD','F':'FOK','1':'市價','2':'限價','3':'停損','4':'停損限價','5':'收市','7':'代沖銷'}}
                }

PERIODSET = dict(
    stock = ("盤中", "盤後", "零股"),
    future = ("ROD", "IOC", "FOK"),
    sea_future = ("ROD"),
    moving_stop_loss = ("IOC", "FOK"),
)
# print(PERIODSET['stock'])
print(OnNewData_dict['BuySell']['TF']['B'],OnNewData_dict['BuySell']['TF']['N'],OnNewData_dict['BuySell']['TF']['R'],OnNewData_dict['BuySell']['TF']['2'])