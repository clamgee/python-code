import multiprocessing as mp
import threading as td
import os
import time

def a(q):
    while q.qsize()!=0:
        a=q.get()
        b=os.getpid()
        print(a,str(b)+'a程式')

def b(q):
    td.Thread(target=a,args=(q,)).start()


if __name__=='__main__':
    q = mp.Manager().Queue()
    l = mp.Manager().Lock()
    for i in range(10):
        res = '第 '+ str(i) + ' 步'
        q.put(res)

    with mp.Pool(mp.cpu_count()) as pool:
        pool.apply_async(b,(q,))
        pool.close()
        pool.join()


