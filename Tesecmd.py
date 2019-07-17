# import pyqtgraph.examples
# pyqtgraph.examples.run()
OnNewData_dict={'MarketType':{'TS':'證券','TA':'盤後','TL':'零股','TF':'期貨','TO':'選擇權','OF':'海期','OO':'海選','OS':'複委託'},
                'Type':{'N':'委託','C':'取消','U':'改量','P':'改價','D':'成交','B':'改價改量','S':'動態退單'},
                'OrderErr':{'Y':'失敗','T':'逾時','N':'正常'},

                }
print(OnNewData_dict['OrderErr']['N'])