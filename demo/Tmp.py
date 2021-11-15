import numpy as np
import pandas as pd
import math

date = '2017'
df.Close[date].plot()
(df.Close.shift(-20) / df.Close > 1).astype(int)[date].plot(secondary_y=True)

def triple_barrier(price, ub, lb, max_period):

    def end_price(s):
        return np.append(s[(s / s[0] > ub) | (s / s[0] < lb)], s[-1])[0]/s[0]
    
    r = np.array(range(max_period))
    
    def end_time(s):
        return np.append(r[(s / s[0] > ub) | (s / s[0] < lb)], max_period-1)[0]

    p = price.rolling(max_period).apply(end_price, raw=True).shift(-max_period+1)
    t = price.rolling(max_period).apply(end_time, raw=True).shift(-max_period+1)
    t = pd.Series([t.index[int(k+i)] if not math.isnan(k+i) else np.datetime64('NaT') 
                   for i, k in enumerate(t)], index=t.index).dropna()

    signal = pd.Series(0, p.index)
    signal.loc[p > ub] = 1
    signal.loc[p < lb] = -1
    ret = pd.DataFrame({'triple_barrier_profit':p, 'triple_barrier_sell_time':t, 'triple_barrier_signal':signal})

    return ret

ret = triple_barrier(df.Close, 1.07, 0.97, 20)
# import numpy as np
# import pandas as pd
# lottorydf = pd.read_csv('lottory.csv')
# lottorydf=lottorydf.sort_values(by=['期號'],ascending=True)
# lottorydf=lottorydf.reset_index(drop=True)
# print(lottorydf.tail())
# lottorydf.map
# sns.set()
# Candledf=pd.read_csv('../result.dat',low_memory=False)
# Candledf['ndatetime']=pd.to_datetime(Candledf['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')


