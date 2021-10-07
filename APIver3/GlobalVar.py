import multiprocessing as mp
import pandas as pd
def Initialize():
    global NS #建立一個命名空間
    NS = mp.Manager().Namespace()
    NS.df12K = pd.DataFrame() # 12K圖使用的pandas
    NS.dfMinK = pd.DataFrame() # 分鐘圖使用的pandas
    global CandleItem12K_Queue,CandleItemMinute_Queue
    CandleItem12K_Queue = mp.Manager().Queue()
    CandleItemMinute_Queue = mp.Manager().Queue()
    global Candle12KTarget
    Candle12KTarget = mp.Manager().Value(str,'')