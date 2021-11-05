import multiprocessing as mp
import pandas as pd
import numpy as np
def Initialize():
    global NS #建立一個命名空間
    NS = mp.Manager().Namespace()
    # 12K圖形用
    global CandleItem12K_Event
    NS.df12K = pd.DataFrame() # 12K圖使用的pandas
    NS.list12K = [] #12K圖使用的比對參數
    CandleItem12K_Event = mp.Queue() # 12K圖形變更通知
    #分鐘K圖形用
    global CandleItemMinute_Event,CandleMinuteDealMinus_Event,CandleMinuteBig_Event,CandleMinuteSmall_Event
    NS.dfMinK = pd.DataFrame() # 分鐘圖使用的pandas
    NS.listMinK = [] # 分鐘圖使用的比對參數
    NS.listMinDealMinus =[] # 多空力道圖使用的比對參數
    NS.listMinBig =[] # 大單比對參數
    NS.listMinSmall =[] # 小單比對參數
    NS.listFT = [] #期貨交易委買賣資訊
    CandleItemMinute_Event = mp.Queue()
    CandleMinuteDealMinus_Event = mp.Event()
    CandleMinuteBig_Event = mp.Event()
    CandleMinuteSmall_Event = mp.Event()
    # 五檔介面
    global DomDataQueue, Dom_Event
    NS.Domdf = pd.DataFrame()
    DomDataQueue = mp.Queue()
    Dom_Event = mp.Event()
    # 商品力道表
    global MP_Event,PowerQueue 
    MP_Event = mp.Event()
    PowerQueue = mp.Queue()
    #全介面標的
    global CandleTarget, DomTarget, SaveNotify
    CandleTarget = mp.Manager().Value(str,'') # 所有圖形介面標的
    SaveNotify = mp.Manager().Value(bool,False) # 存檔通知
