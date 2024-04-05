import pandas as pd
import os
from statsmodels.tsa.arima.model import ARIMA

df1=pd.read_csv('filename.txt')
# print(df1)
# print(os.path.abspath('data'))
df = pd.read_csv(r'data/Ticks2024-03-21.txt',header=None)
df.columns = ['ndatetime','nbid','nask','close','volume','deal']
print(df.tail())
target = 'nask'
# 建立ARIMA模型
model = ARIMA(df[target], order=(5,1,0))

# 擬合模型
model_fit = model.fit()

# 進行預測
forecast = model_fit.forecast(steps=1)
print(forecast)
