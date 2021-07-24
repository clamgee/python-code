import multiprocessing as mp
from multiprocessing.process import current_process
import threading as td
import os
import time

def a(q):
    res = []
    print(current_process())
    while q.qsize()!=0:
        # l.acquire()
        a=q.get()
        res=str(a) + str(current_process())+str(os.getpid())  
        # l.release()
    

def c(a):
    res = str(a) + str(current_process())+str(os.getpid())
    # print(res)
    return res

        

def b(q):
    td.Thread(target=a,args=(q,)).start()


if __name__=='__main__':
    multiq = mp.Manager().Queue()
    q=mp.Queue()
    q1=mp.Queue()
    q2=mp.Queue()
    l = mp.Manager().Lock()
    for i in range(30000):
        res = i
        q.put(res)
        q1.put(res)
        q2.put(res)
        multiq.put(res)

    start = time.time()
    a(q)
    print('Normal時間: ',time.time()-start)
    start = time.time()
    b(q1)
    print('Thread時間: ',time.time()-start)
    start = time.time()
    p1 = mp.Process(target=b,args=(q2,))
    p1.start()
    p1.join()
    print('Process時間: ',time.time()-start)
    start = time.time()
    with mp.Pool() as pool:
        res=[]
        while multiq.qsize()!=0:
            a=multiq.get()
            res.append(pool.apply_async(c,(a,)))
        pool.close()
        pool.join()
    print(res[9].get())

    print('Pool時間: ',time.time()-start)

