import pandas as pd

avgpd = pd.read_csv('../APIver1/result.dat')
avgpd.sort_values(by=['ndatetime'], ascending=True)
avgpd = avgpd.reset_index(drop=True)
avgpd['high_avg'] = 0
avgpd['low_avg'] = 0

def avgline(x):
    # x = avgpd['high'].iloc[-20:].mean(0)
    if x.last_valid_index() != x.index[0]:
        # return x.iloc[-20:].mean(0)
        return  x.index[0]
    else:
        return -1


avgpd['high_avg'] = avgpd.loc[:'high'].rolling(20).mean()
# avgpd['low_avg'] = avgpd.low.rolling(20).mean()

# a = avgpd['high'].iloc[-20:].mean(0)
print(avgpd.tail(25))