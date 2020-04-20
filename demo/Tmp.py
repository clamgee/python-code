import pandas as pd

avgpd = pd.read_csv('../APIver1/result.dat')
avgpd.sort_values(by=['ndatetime'], ascending=True)
avgpd = avgpd.reset_index(drop=True)
avgpd['high_avg'] = 0
avgpd['low_avg'] = 0

def avgline(x):
    for idx in avgpd.index:
        if idx < x:
            oldx = x
            x = idx

        avgpd.loc[idx,'high_avg'] = avgpd['high'].iloc[-x:].mean(0)
        avgpd.loc[idx,'low_avg'] = avgpd['low'].iloc[-x:].mean(0)

#
avgpd.apply(avgline(20))

# a = avgpd['high'].iloc[-20:].mean(0)
print(avgpd.tail(5))