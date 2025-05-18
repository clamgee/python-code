from ollama import generate
import pandas as pd
import os
import re
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
LongTimes = 0
ShortTimes = 0
#開啟檔案訓練
# filelist = ["Ticks2025-03-28.txt","Ticks2025-03-31.txt","Ticks2025-04-01.txt","Ticks2025-04-02.txt"]
filelist = re.compile(r'Ticks2025-04-\w+\.txt')
for info in domain:
  if info != "filename.txt" and filelist.match(info):
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
    ndate = daymin.at[0,"ndatetime"].date()
    daymin["avgline"] = daymin.close.expanding().mean()
    # tmpline = daymin.close.cumsum()
    # daymin["avgline"]=tmpline.apply(lambda x: x/(tmpline[tmpline==x].index[0]+1))
    # del tmpline
    Tradingtimes = 0
    longprice = 0
    sellprice = 0
    Position = 0
    nclose = 0
    FloatingProfit = 0
    dealminus_history_mean=0
    laststyle = "正確"
    lastresponse = "正確"
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
              "temperature": 0.2,
              "max_tokens": 10,
              "num_ctx" : input_token,
              "num_predict" : 16 # 限制輸出
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
      if pd.isna(x["close"]):
        x["open"], x["close"], x["high"], x["low"], x["volume"],x["dealminus"]=lastopen, lastclose, lasthigh, lastlow, 0, lastdealminus
      else:
        lastopen, lastclose, lasthigh, lastlow, lastdealminus = x["open"], x["close"], x["high"], x["low"],x["dealminus"]
        
      if dealminus_history_mean != 0:
        dealminus_history_mean = (x['dealminus'] + dealminus_history_mean)/2
      else:
        dealminus_history_mean = x["dealminus"]
      if Position > 0 :
        FloatingProfit = (x["close"] - longprice)*Position*200 - abs(Position)*200
      elif Position < 0 :
        FloatingProfit = (x["close"] - sellprice)*Position*200 - abs(Position)*200
      else:
        FloatingProfit = 0

      prompt = f"""
      你是一個具備自我優化能力的期貨交易AI，多空靈活操作，每日進行當沖交易，目標是提升"績效"，需綜合以下要素生成操作指令：
      {{
        "K線": {{
          "時間": "{x['ndatetime']}",
          "開盤價": {x['open']},
          "最高價": {x['high']},
          "最低價": {x['low']},
          "收盤價": {x['close']},
          "成交量": {x['volume']}
        }},
        "技術分析"{{
          "多空力道": {x['dealminus']},
          "平均線" : {x['avgline']},
          "多空力道均值": {dealminus_history_mean}
        }},
        "持倉狀態": {{
          "數量": {Position},
          "多空單":{"Long" if Position > 0 else "Short" if Position < 0 else "Hold" },
          "成本價": {longprice if Position > 0 else sellprice if Position < 0 else 0}
        }},
        "當日期":{ndate},
        "當日交易次數":{Tradingtimes},
        "績效": {{          
          "當前浮動盈虧": {FloatingProfit},
          "總多單次數": {LongTimes}
          "總空單次數":{ShortTimes}
          "總盈虧": {TotallProfit}
        }},
        "上次輸出格式":{laststyle}
        "上次輸出操作":{lastresponse}
      }}

      ***強制原則（嚴格執行):
      -當前浮動盈虧小於-14000 時， 執行{{"operation": "StopLoss"}}
      -當日交易次數小於11次
      -9:00之前選Hold
      -當下時間超過過13:40，執行{{"operation": "StopLoss"}}，之後選Hold
      ***強制原則結束

      ***AI自主依據以下順序判斷趨勢判定多空，多空不明則選Hold，空方選Sell，多方選Buy:
        1.多空力道，持續減少為空方選Sell，持續增加為多方選Buy
        2.平均線，低於平均線為空方，高於平均線為空方
        3.過去5筆多空力道均值，低於均值為空方，高於均值為多方
        4.收盤價
        5.當前浮動盈虧
        6.開盤價
        7.成交量
        8.最高價
        9.最低價
      ***依據結束

      ***輸出格式以下四選一(必須嚴格遵守):
      {{"operation": "Hold"}}  # 允許
      {{"operation": "StopLoss"}}  # 允許
      {{"operation": "Sell"}}  # 允許
      {{"operation": "Buy"}}   # 允許

      **禁止添加任何其他字段或解釋！**
      """
      # 啟動事件循環
      input_token = min(count_tokens_words(prompt),4096)
      full_response = stream_generate(prompt,input_token)  
      nclose = x["close"]
      print(f"在（{x["ndatetime"]}）：")

      # 嘗試解析完整的 JSON 結果
      try:
        result = json.loads(full_response)
        lastresponse ="正確"
        laststyle ="正確"
      except json.JSONDecodeError as e:
        print("❗️JSON 解析錯誤：", e)
        print("⚠️ 回傳內容如下（用於除錯）：")
        print(full_response)
        result = {"operation": "Hold"}  # 預設 fallback 行為
      if "operation" in result.keys() and result["operation"] in ["Hold","Buy","Sell","StopLoss"]:
        action = result["operation"]
      else:
        lastresponse = "錯誤"
        action = "Hold"
        print("操作格式錯誤: ",result)
    
      if x["ndatetime"].time() > datetime.time(13,40,0) or action == "StopLoss":
        if Position > 0 and action == "StopLoss":
          print("step 1")
          FloatingProfit = (x["close"]-longprice)*Position*200 - abs(Position)*200
          TotallProfit += FloatingProfit
          while Position > 0 :
            print("多單平倉")
            Tradingpd = close_first_open_contract(Tradingpd,x["ndatetime"],x["close"],-1)
            Position -= 1
          longprice = 0
          FloatingProfit = 0
        elif Position < 0 and action == "StopLoss":
          print("step 2")
          FloatingProfit = (x["close"] - sellprice)*Position*200 - abs(Position)*200
          TotallProfit += FloatingProfit
          while Position < 0:
            print("空單平倉")
            Tradingpd = close_first_open_contract(Tradingpd,x["ndatetime"],x["close"],1)
            Position += 1
          sellprice = 0
          FloatingProfit = 0
        else:
            if action == "StopLoss":
              lastresponse = "錯誤"
            print("step 3")
            longprice = 0
            sellprice = 0
            Position = 0
            FloatingProfit = 0
      elif action == "Hold" :
        if Position == 0:
          print("step 4")
          longprice = 0
          sellprice = 0
          Position = 0
      elif action == "Buy":
        if Position == 0 : #空手
          print("step 6")
          Position += 1
          LongTimes += 1
          longprice = x["close"]
          FloatingProfit = (x["close"] - longprice)*Position*200 - abs(Position)*200
          Tradingpd = pd.concat([Tradingpd,pd.DataFrame([[x["ndatetime"],x["close"],1,x["ndatetime"],0,0]],columns=["openTime","openPrice","openContract","closeTime","closePrice","closeContract"])],ignore_index=True,sort=False)
        elif Position == MaxOI:
          print("step 7")
          FloatingProfit = (x["close"] - longprice)*Position*200 - abs(Position)*200
        elif Position < 0: #空單在手
          print("step 9")
          FloatingProfit = (x["close"] - sellprice)*Position*200 - abs(Position)*200
          TotallProfit += FloatingProfit
          while Position < 0:
            print("空單平倉")
            Tradingpd = close_first_open_contract(Tradingpd,x["ndatetime"],x["close"],1)
            Position += 1
          longprice = 0
          sellprice = 0
          FloatingProfit = 0
        elif Position < 2 : #多單在手
          print("step 8")
          Position += 1
          LongTimes += 1
          longprice = (longprice + x["close"]) / 2
          FloatingProfit = (x["close"] - longprice)*Position*200 - abs(Position)*200
          Tradingpd = pd.concat([Tradingpd,pd.DataFrame([[x["ndatetime"],x["close"],1,x["ndatetime"],0,0]],columns=["openTime","openPrice","openContract","closeTime","closePrice","closeContract"])],ignore_index=True,sort=False)
      elif action == "Sell":
        if Position == 0 : # 空手
          print("step 10")
          Position -= 1
          ShortTimes += 1
          sellprice = x["close"]
          FloatingProfit = (x["close"] - sellprice)*Position*200 - abs(Position)*200
          Tradingpd = pd.concat([Tradingpd,pd.DataFrame([[x["ndatetime"],x["close"],-1,x["ndatetime"],0,0]],columns=["openTime","openPrice","openContract","closeTime","closePrice","closeContract"])],ignore_index=True,sort=False)
        elif Position == - MaxOI :
          print("step 11")
          FloatingProfit = (x["close"] - sellprice)*Position*200 - abs(Position)*200
        elif Position > 0 : #多單
          print("step 13")
          FloatingProfit = (x["close"]-longprice)*Position*200 - abs(Position)*200
          TotallProfit = TotallProfit + FloatingProfit
          while Position > 0 :
            print("多單平倉")
            Tradingpd = close_first_open_contract(Tradingpd,x["ndatetime"],x["close"],-1)
            Position -= 1
          longprice = 0
          sellprice = 0
          FloatingProfit = 0
        elif -2 < Position : #空單
          print("step 12")
          Position -= 1
          ShortTimes += 1
          sellprice = (sellprice + x["close"]) / 2
          FloatingProfit = (x["close"] - sellprice)*Position*200 - abs(Position)*200
          Tradingpd = pd.concat([Tradingpd,pd.DataFrame([[x["ndatetime"],x["close"],-1,x["ndatetime"],0,0]],columns=["openTime","openPrice","openContract","closeTime","closePrice","closeContract"])],ignore_index=True,sort=False)
        else:
          lastresponse = "錯誤"
          print("賣出資訊錯誤")
      Tradingtimes = Tradingpd[Tradingpd["openTime"].dt.date == ndate].shape[0]
      print(f"每次運行時間: {datetime.datetime.now()-start}")
      print(f"操作: {result}| 現價: {nclose} | 買進價: {longprice}| 賣出價: {sellprice}| 未平倉: {Position}| 浮動損益: {FloatingProfit}")
      print(f"交易次數: {Tradingtimes}|多單次數:{LongTimes}|空單次數{ShortTimes}| 總損益: {TotallProfit}")
      OIpd = Tradingpd[(Tradingpd["openContract"] != 0) & (Tradingpd["closeContract"] == 0)]
      if OIpd.shape != 0 :
        print(OIpd)
      # if x["ndatetime"].time() == datetime.time(13,44,0):
      #   print(Tradingpd)
Tradingpd.to_csv('AITradeProfit.txt', header=False, index=False)
