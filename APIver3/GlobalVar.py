import multiprocessing as mp
import pandas as pd
import numpy as np
def Initialize():
    global NS #建立一個命名空間
    NS = mp.Manager().Namespace()
    NS.df12K = pd.DataFrame() # 12K圖使用的pandas
    NS.list12K = [] #12K圖使用的比對參數
    NS.dfMinK = pd.DataFrame() # 分鐘圖使用的pandas
    NS.listMinK = [] # 分鐘圖使用的比對參數
    NS.listMinDealMinus =[] # 多空力道圖使用的比對參數
    NS.Domdf = pd.DataFrame(np.arange(24).reshape(6,4), columns=['買量','買價','賣價','賣量']) #多空力道 DataFrame
    NS.Domdf[['買量','買價','賣價','賣量']]=NS.Domdf[['買量','買價','賣價','賣量']].astype(str)
    global CandleItem12K_Event,CandleItemMinute_Event,CandleMinuteDealMinus_Event
    CandleItem12K_Event = mp.Queue()
    CandleItemMinute_Event = mp.Queue()
    CandleMinuteDealMinus_Event = mp.Queue()
    global CandleTarget, DomTarget, SaveNotify
    CandleTarget = mp.Manager().Value(str,'') # 圖形介面標的
    DomTarget = mp.Manager().Value(int,0) # 五檔標的
    SaveNotify = mp.Manager().Value(bool,False) # 存檔通知
