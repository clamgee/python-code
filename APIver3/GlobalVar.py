import multiprocessing as mp
import pandas as pd
def Initialize():
    global NS #建立一個命名空間
    NS = mp.Manager().Namespace()
    NS.df12K = pd.DataFrame() # 12K圖使用的pandas
    NS.list12K = [] #12K圖使用的比對參數
    NS.dfMinK = pd.DataFrame() # 分鐘圖使用的pandas
    NS.listMinK = [] # 分鐘圖使用的比對參數
    global CandleItem12K_Event,CandleItemMinute_Event
    CandleItem12K_Event = mp.Queue()
    CandleItemMinute_Event = mp.Queue()
    global CandleTarget
    CandleTarget = mp.Manager().Value(str,'')
