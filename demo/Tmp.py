# import pandas as pd
# import os

# domain=os.listdir('../APIver1/data')
# print(domain[-1])
# tmp=pd.read_csv('../APIver1/data/'+domain[-1])
# tmp.rename(columns={
#     tmp.columns[0]: 'ndate',
#     tmp.columns[1]: 'ntime',
#     tmp.columns[2]: 'nbid',
#     tmp.columns[3]: 'nask',
#     tmp.columns[4]: 'close',
#     tmp.columns[5]: 'volume',
# }, inplace=True)
# print(tmp.tail(5))
import pandas as pd
import multiprocessing as mp

df = pd.DataFrame({'ser_no': [1, 2, 3, 4, 5, 6, 7, 8, 9, 0],
                'co_nm': ['aa', 'aa', 'aa', 'bb', 'bb', 'bb', 'bb', 'cc', 'cc', 'cc'],
                'lat': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                'lon': [21, 22, 23, 24, 25, 26, 27, 28, 29, 30]})



def calc_dist(x):
    ret =  pd.DataFrame(
               [ [grp,
                  df.loc[c[0]].ser_no,
                  df.loc[c[1]].ser_no,
                  vincenty(df.loc[c[0], x],
                           df.loc[c[1], x])
                 ]
                 for grp,lst in df.groupby('co_nm').groups.items()
                 for c in combinations(lst, 2)
               ],
               columns=['co_nm','machineA','machineB','distance'])
    print(ret)
    return ret

if __name__ == '__main__':
    pool = mp.Pool(processes = (mp.cpu_count() - 1))
    pool.map(calc_dist, ['lat','lon'])
    pool.close()
    pool.join()