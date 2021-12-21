import multiprocessing as mp
import pandas as pd
import numpy as np
def Initialize():
    global NS #建立一個命名空間
    NS = mp.Manager().Namespace()
    # 12K圖形用
    global CandleItem12K_Event
    NS.df12K = pd.DataFrame() # 12K圖使用的pandas
    NS.nPtr12K = 0 #12K圖使用的比對參數
    CandleItem12K_Event = mp.Queue() # 12K圖形變更通知
    #分鐘K圖形用
    global CandleItemMinute_Event,CandleMinuteDealMinus_Event,CandleMinuteBig_Event,CandleMinuteSmall_Event
    NS.dfMinK = pd.DataFrame() # 分鐘圖使用的pandas
    NS.nPtrMinK = 0 # 分鐘圖使用的比對參數
    NS.nPtrMinDealMinus = 0 # 多空力道圖使用的比對參數
    NS.nPtrMinBig = 0 # 大單比對參數
    NS.nPtrMinSmall = 0 # 小單比對參數
    NS.listFT = [] #期貨交易委買賣資訊
    NS.Domdict = {} #五檔報價處理
    NS.Domlist = [] #五檔報價傳送list
    CandleItemMinute_Event = mp.Queue()
    CandleMinuteDealMinus_Event = mp.Queue()
    CandleMinuteBig_Event = mp.Queue()
    CandleMinuteSmall_Event = mp.Queue()
    # 五檔介面
    global DomDataQueue, Dom_Event
    NS.Domdf = pd.DataFrame()
    # DomDataQueue = mp.Queue()
    Dom_Event = mp.Event()
    # 商品力道表
    global MP_Event,PowerQueue 
    MP_Event = mp.Event()
    PowerQueue = mp.Queue()
    #全介面標的
    global CandleTarget, DomTarget, SaveNotify
    CandleTarget = mp.Manager().Value(str,'') # 所有圖形介面標的
    SaveNotify = mp.Manager().Value(bool,False) # 存檔通知
    # 分鐘線座標
    global DailyAxis, NightlyAxis
    DailyAxis={0:'08:45:00', 15: '09:00:00', 75: '10:00:00', 135: '11:00:00', 195: '12:00:00', 255: '13:00:00', 300: '13:45:00'}
    NightlyAxis = {0: '15:00:00', 60: '16:00:00', 120: '17:00:00', 180: '18:00:00', 240: '19:00:00', 300: '20:00:00', 360: '21:00:00', 420: '22:00:00', 480: '23:00:00', 540: '00:00:00', 600: '01:00:00', 660: '02:00:00', 720: '03:00:00', 780: '04:00:00', 840: '05:00:00'}
