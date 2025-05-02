from ollama import generate
import pandas as pd
import os
import json
import datetime

# === 檔案讀取 ===
domain = os.listdir("./data")
direct = os.path.abspath("./data")
file = direct + "\\Ticks2025-03-25.txt"
print(file)

alldayticks = pd.read_csv(file, header=None, names=["ndatetime", "nbid", "nask", "close", "volume", "deal"], low_memory=False)
alldayticks["ndatetime"] = pd.to_datetime(alldayticks["ndatetime"])

dayticks = alldayticks[(alldayticks.ndatetime.dt.hour >= 8) & (alldayticks.ndatetime.dt.hour < 15)]
dayticks.sort_values(by=["ndatetime"], ascending=True)
dayticks.index = dayticks.ndatetime

daymin = dayticks["close"].resample("1min", closed="right").ohlc()
daymin["volume"] = dayticks["volume"].resample("1min").sum()
daymin["deal"] = dayticks["deal"].resample("1min").sum()
daymin["dealminus"] = daymin["deal"].cumsum()
daymin = daymin.drop(columns=["deal"])
daymin = daymin.reset_index(drop=False)

# === 初始化 ===
Tradingpd = pd.DataFrame(columns=["openTime", "openPrice", "openContract", "closeTime", "closePrice", "closeContract"])
Tradingpd[["openTime", "closeTime"]] = Tradingpd[["openTime", "closeTime"]].apply(pd.to_datetime)
Tradingpd[["openPrice", "openContract", "closePrice", "closeContract"]] = Tradingpd[["openPrice", "openContract", "closePrice", "closeContract"]].astype(int)

MaxOI = 2
Position = 0
longprice = 0
sellprice = 0
FloatingProfit = 0
TotallProfit = 0
lastresponse = "正確"

# === 工具函式 ===
def close_first_open_contract(df, xtime, xprice, xcontract):
    flag = {"done": False}
    def modify(row):
        if not flag["done"] and row["openContract"] != 0 and row["closeContract"] == 0:
            row["closeTime"] = xtime
            row["closePrice"] = xprice
            row["closeContract"] = xcontract
            flag["done"] = True
        return row
    return df.apply(modify, axis=1)

def stream_generate(prompt):
    response = generate(
        model="deepseek-r1:1.5b",
        prompt=prompt,
        stream=True,
        options={"num_threads": 8, "temperature": 0.5, "max_tokens": 10},
        format="json"
    )
    full_response = ""
    for chunk in response:
        full_response += chunk["response"]
    return full_response

# === 主邏輯 ===
for (t, x) in daymin.iterrows():
    start = datetime.datetime.now()

    prompt = f"""
    以下是台指期貨 1 分鐘 K 線資料：
    {{"時間": "{x['ndatetime']}", "開盤價": {x['open']}, "最高價": {x['high']}, "最低價": {x['low']}, "收盤價": {x['close']}, "成交量": {x['volume']}, "多空力道": {x['dealminus']}}}
    目前倉位：{{"持仓量": {Position}, "買進價": {longprice}, "賣出價": {sellprice}, "浮动盈亏": {FloatingProfit}}}
    上次操作回復格式是否正確：{lastresponse}

    請根據以上資料進行操作，**僅能從以下 JSON 格式中擇一輸出，禁止額外說明或加入其他欄位**：
    {{"操作": "观望"}}
    {{"操作": "买多"}}
    {{"操作": "卖空"}}
    """

    full_response = stream_generate(prompt)

    try:
        result = json.loads(full_response)
        if "操作" not in result:
            raise ValueError("無操作欄位")

        action = result["操作"]
        lastresponse = "正確"
        if action == "观望":
            if Position > 0:
                FloatingProfit = (x["close"] - longprice) * 200
            elif Position < 0:
                FloatingProfit = (sellprice - x["close"]) * 200
            else:
                FloatingProfit = 0
        elif action == "买多":
            if Position < 0:
                FloatingProfit = (sellprice - x["close"]) * -1 * 200
                TotallProfit += FloatingProfit
                Tradingpd = close_first_open_contract(Tradingpd, x["ndatetime"], x["close"], 1)
                Position += 1
                longprice = x["close"]
            elif Position < MaxOI:
                Position += 1
                longprice = (longprice + x["close"]) / Position if longprice != 0 else x["close"]
                Tradingpd = pd.concat([Tradingpd, pd.DataFrame([[x["ndatetime"], x["close"], 1, x["ndatetime"], 0, 0]], columns=Tradingpd.columns)], ignore_index=True)
        elif action == "卖空":
            if Position > 0:
                FloatingProfit = (x["close"] - longprice) * 200
                TotallProfit += FloatingProfit
                Tradingpd = close_first_open_contract(Tradingpd, x["ndatetime"], x["close"], -1)
                Position -= 1
                sellprice = x["close"]
            elif abs(Position) < MaxOI:
                Position -= 1
                sellprice = (sellprice + x["close"]) / abs(Position) if sellprice != 0 else x["close"]
                Tradingpd = pd.concat([Tradingpd, pd.DataFrame([[x["ndatetime"], x["close"], -1, x["ndatetime"], 0, 0]], columns=Tradingpd.columns)], ignore_index=True)

        print(f"[{x['ndatetime']}] 操作: {action} | 未平倉: {Position} | 浮損益: {FloatingProfit} | 總損益: {TotallProfit}")
    except Exception as e:
        print(f"[{x['ndatetime']}] ⚠️ 錯誤：{e} | 回應：{full_response}")
        lastresponse = "錯誤"


#["观望","买多","卖空"]