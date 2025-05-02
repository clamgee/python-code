from ollama import generate
import pandas as pd
import os
import json
import datetime
domain=os.listdir("./data")
direct=os.path.abspath("./data")
#定義交易
Tradingpd = pd.DataFrame(columns=["openTime","openPrice","openContract","closeTime","closePrice","closeContract"])
Tradingpd["openTime"]=pd.to_datetime(Tradingpd["openTime"])#,format="%Y-%m-%d %H:%M:%S.%f")
Tradingpd["closeTime"]=pd.to_datetime(Tradingpd["closeTime"])#,format="%Y-%m-%d %H:%M:%S.%f")
Tradingpd[["openPrice","openContract","closePrice","closeContract"]]=Tradingpd[["openPrice","openContract","closePrice","closeContract"]].astype(int)
MaxTrading = 2
MaxOI = 2
TotallProfit = 0
#開啟檔案訓練
for info in domain:
  if info != "filename.txt":
    alldayticks = pd.read_csv('data/'+info,header=None,names=["ndatetime","nbid","nask","close","volume","deal"],low_memory=False)
    alldayticks["ndatetime"]=pd.to_datetime(alldayticks["ndatetime"],format="mixed")
    nightticks = alldayticks[(alldayticks.ndatetime.dt.hour>14) | (alldayticks.ndatetime.dt.hour<8)] # 夜盤
    dayticks = alldayticks[(alldayticks.ndatetime.dt.hour>=8) & (alldayticks.ndatetime.dt.hour<15)] # 日盤
    dayticks.sort_values(by=["ndatetime"],ascending=True)
    dayticks.index = dayticks.ndatetime
    daymin = dayticks["close"].resample("1min",closed="right").ohlc()
    tmpdf=dayticks["volume"].resample("1min").sum()
    daymin=pd.concat([daymin,tmpdf],axis=1)
    del tmpdf
    tmpdf=dayticks["deal"].resample("1min").sum()
    daymin=pd.concat([daymin,tmpdf],axis=1)
    daymin["dealminus"] = daymin["deal"].cumsum()
    del daymin["deal"]
    del tmpdf
    daymin = daymin.reset_index(drop=False)
    #日內交易定義
    Tradingtimes = 0
    longprice = 0
    sellprice = 0
    Position = 0
    nclose = 0
    FloatingProfit = 0
    lastresponse = '正確'
    full_response = ""
    def close_first_open_contract(df,xtime,xprice,xcontract): #平倉程式
        flag = {"done": False}
        def modify(row):
            if not flag["done"] and row["openContract"] != 0 and row["closeContract"] == 0:
                row["closeTime"] = xtime
                row["closePrice"] = xprice
                row["closeContract"] = xcontract
                flag["done"] = True
                print('row: ',row)
            return row
        return df.apply(modify, axis=1)

    def count_tokens_words(text: str) -> int:
        """
        近似估算 Token 数量（适用于英文：1 Token ≈ 0.75 单词）
        """
        words = text.split()
        return max(int(len(words) * 1.3),128)  # 增加30%余量

    def stream_generate(prompt,input_token): #匯入 AI
      response = generate(
          model="deepseek-r1:1.5b",
          prompt=prompt,
          stream=True,
          options={
              "num_threads": 8,
              "temperature": 0.1,
              "max_tokens": 10,
              "num_ctx" : input_token
          },
          format="json"
      )
      full_response = ""
      for chunk in response:
        full_response += chunk["response"]
        # print(chunk["response"], end="", flush=True)
        # print()
      return full_response
    # 進入K線
    for (t, x) in daymin.loc[:, :].iterrows():
      start = datetime.datetime.now()
      prompt = f"""
      你是一個專業的期貨交易AI，嚴格根據以下條件分析即時K線數據，返回交易指令：
      {{
        {{"K線":"時間": "{x['ndatetime']}",
          "開盤價": {x['open']},
          "最高價": {x['high']},
          "最低價": {x['low']},
          "收盤價": {x['close']},
          "成交量": {x['volume']},
          "多空力道": {x['dealminus']}
        }}
        {{"目前倉位"：
          "當前方向": {"多單" if Position > 0 else "空單" if Position < 0 else "空手"},
          "持仓量": {abs(Position)},
          "持倉價": {longprice if Position > 0 else sellprice if Position < 0 else x['close']}
        }}
        {{"上次操作回覆"：
        "回覆格式":{lastresponse},
        "浮动盈亏": {FloatingProfit},
        "总盈亏" : {TotallProfit}
        }}
        {{"交易限制":
          "最大持倉" : {MaxOI},
          "止損金額": -14000
        }}
      }}

      根據以下交易邏輯判斷要執行的操作：
      - 依照目前K線資料與往前累積一到十五筆資料做比對
      - 多空力道累積增加，選 操作:buy
      - 多空力道累積減少，選 操作:sell
      - 多空力道趨勢不明，選 操作:hold
      - 成交量瞬間放大則可能為價格突破或反轉

      **只能選擇並回覆下列 JSON 格式之一，禁止回覆任何其他內容**：
      {{"操作": "Hold"}}
      {{"操作": "Sell"}}
      {{"操作": "Buy"}}

      請注意：**禁止添加任何解釋或其他欄位**。
      """
      # 啟動事件循環
      input_token = min(count_tokens_words(prompt),4096)
      full_response = stream_generate(prompt,input_token)  
      nclose = x["close"]
      lastresponse ='正確'
      print(f"在（{x["ndatetime"]}）：")

      # 嘗試解析完整的 JSON 結果
      result = json.loads(full_response)
      if "操作" in result.keys() and result["操作"] in ["Hold","Buy","Sell"]:
        action = result["操作"]
        if x["ndatetime"].time() > datetime.time(13,40,0):
          if Position > 0:
            if (Position-1) == 0 :
              print("step 13")
              FloatingProfit = (x["close"]-longprice)*1*200
              TotallProfit = TotallProfit + FloatingProfit
              FloatingProfit = (x["close"]-longprice)*Position*200
              longprice = 0
              sellprice = 0
              Position = 0
              FloatingProfit = 0
              Tradingpd = close_first_open_contract(Tradingpd,x["ndatetime"],x["close"],-1)
            else:
              print("step 14")
              Position -= 1
              FloatingProfit = (x["close"] - longprice)*Position*200
              TotallProfit = TotallProfit + FloatingProfit
              Tradingpd = close_first_open_contract(Tradingpd,x["ndatetime"],x["close"],-1)
          elif Position < 0:
            if (Position+1) == 0 :
              print("step 15")
              FloatingProfit = (sellprice - x["close"])*-1*200
              TotallProfit = TotallProfit + FloatingProfit
              longprice = 0
              sellprice = 0
              Position = 0
              FloatingProfit = 0
              Tradingpd = close_first_open_contract(Tradingpd,x["ndatetime"],x["close"],1)
            else:
              print("step 16")
              Position += 1
              FloatingProfit = (sellprice - x["close"])*-1*200
              TotallProfit = TotallProfit + FloatingProfit
              FloatingProfit = (sellprice - x["close"])*Position*200
              Tradingpd = close_first_open_contract(Tradingpd,x["ndatetime"],x["close"],1)
          else:
              print("step 17")
              longprice = 0
              sellprice = 0
              Position = 0
              FloatingProfit = 0
        elif action == "Hold" :
          if Position == 0:
            print("step 1")
            longprice = 0
            sellprice = 0
            Position = 0
            FloatingProfit = 0        
          elif Position > 0:
            print("step 2")
            FloatingProfit = (x["close"] - longprice)*200*Position
          elif Position < 0:
            FloatingProfit = (sellprice - x["close"])*200*Position
          else:
            lastresponse = '錯誤'
            print("觀望回復錯誤")
        elif action == "Buy":
          if Position == 0 : #空手
            print("step 3")
            Position += 1
            longprice = x["close"]
            FloatingProfit = (x["close"] - longprice)*Position*200
            Tradingpd = pd.concat([Tradingpd,pd.DataFrame([[x["ndatetime"],x["close"],1,x["ndatetime"],0,0]],columns=["openTime","openPrice","openContract","closeTime","closePrice","closeContract"])],ignore_index=True,sort=False)
          elif 0 < Position < 2 : #多單在手
            print("step 4")
            Position += 1
            longprice = (longprice + x["close"]) / Position
            FloatingProfit = (x["close"] - longprice)*Position*200
            Tradingpd = pd.concat([Tradingpd,pd.DataFrame([[x["ndatetime"],x["close"],1,x["ndatetime"],0,0]],columns=["openTime","openPrice","openContract","closeTime","closePrice","closeContract"])],ignore_index=True,sort=False)
          elif abs(Position) == MaxOI:
            print("step 5")
            FloatingProfit = (x["close"] - longprice)*Position*200
          elif Position < 0: #空單在手
            if (Position+1) == 0 :
              print("step 6")
              FloatingProfit = (sellprice - x["close"])*-1*200
              TotallProfit = TotallProfit + FloatingProfit
              longprice = 0
              sellprice = 0
              Position = 0
              FloatingProfit = 0
              Tradingpd = close_first_open_contract(Tradingpd,x["ndatetime"],x["close"],1)
            else:
              print("step 7")
              Position += 1
              FloatingProfit = (sellprice - x["close"])*-1*200
              TotallProfit = TotallProfit + FloatingProfit
              FloatingProfit = (sellprice - x["close"])*Position*200
              Tradingpd = close_first_open_contract(Tradingpd,x["ndatetime"],x["close"],1)
          else:
              print("買進資訊錯誤")
        elif action == "Sell":
          if Position == 0 : # 空手
            print("step 8")
            Position -= 1
            sellprice = x["close"]
            FloatingProfit = (sellprice - x["close"])*Position*200
            Tradingpd = pd.concat([Tradingpd,pd.DataFrame([[x["ndatetime"],x["close"],-1,x["ndatetime"],0,0]],columns=["openTime","openPrice","openContract","closeTime","closePrice","closeContract"])],ignore_index=True,sort=False)
          elif -2 < Position < 0 : #空單
            print("step 9")
            Position -= 1
            sellprice = (sellprice + x["close"]) / abs(Position)
            FloatingProfit = (sellprice - x["close"])*Position*200
            Tradingpd = pd.concat([Tradingpd,pd.DataFrame([[x["ndatetime"],x["close"],-1,x["ndatetime"],0,0]],columns=["openTime","openPrice","openContract","closeTime","closePrice","closeContract"])],ignore_index=True,sort=False)
          elif Position < 0 and abs(Position) == MaxOI :
            print("step 10")
            FloatingProfit = (sellprice - x["close"])*Position*200
          elif Position > 0 : #多單
            if (Position-1) == 0 :
              print("step 11")
              FloatingProfit = (x["close"]-longprice)*1*200
              TotallProfit = TotallProfit + FloatingProfit
              FloatingProfit = (x["close"]-longprice)*Position*200
              longprice = 0
              sellprice = 0
              Position = 0
              FloatingProfit = 0
              Tradingpd = close_first_open_contract(Tradingpd,x["ndatetime"],x["close"],-1)
            else:
              print("step 12")
              Position -= 1
              FloatingProfit = (x["close"] - longprice)*Position*200
              TotallProfit = TotallProfit + FloatingProfit
              Tradingpd = close_first_open_contract(Tradingpd,x["ndatetime"],x["close"],-1)
          else:
            lastresponse = '錯誤'
            print("賣出資訊錯誤")
      else:
          lastresponse = '錯誤'
          print("操作格式錯誤: ",result)
      print(f"每次運行時間: {datetime.datetime.now()-start}")
      print(f"操作: {result}| 現價: {nclose} | 買進價: {longprice}| 賣出價: {sellprice}| 未平倉: {Position}| 浮動損益: {FloatingProfit}| 總損益: {TotallProfit}")
      OIpd = Tradingpd[(Tradingpd["openContract"] != 0) & (Tradingpd["closeContract"] == 0)]
      print(OIpd)
      # if x["ndatetime"].time() == datetime.time(13,44,0):
      #   print(Tradingpd)
Tradingpd.to_csv('AITradeProfit.txt', header=False, index=False)