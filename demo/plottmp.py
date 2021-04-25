import plotly.graph_objs as go
import pandas as pd
from datetime import datetime

df=pd.read_csv('../result.dat')

print(df.head(5))

fig = go.Figure(data=[go.Candlestick(x=df['ndatetime'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])

fig.show()