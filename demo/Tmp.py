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

import time
import multiprocessing
# 3. 建立一個測試程式
def test(idx, test_dict):
    lock.acquire()
    row = test_dict['test']
    row[idx] = idx
    test_dict['test'] = row
    lock.release()
# 4. 建立程序池進行測試
if __name__ =='__main__':
    # 1. 建立一個Manger物件
    manager = multiprocessing.Manager()
    lock = manager.Lock()
    # 2. 建立一個dict
    temp_dict = manager.dict()
    temp_dict['test'] = {}
    start = time.time()
    pool = multiprocessing.Pool()
    for i in range(10000):
        pool.apply_async(test, args=(i, temp_dict))
    pool.close()
    pool.join()
    print(time.time()-start,'秒')