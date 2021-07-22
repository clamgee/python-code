import multiprocessing as mp
import threading as td
import os
import time

def a(l,q):
    while True:
        l.acquire()
        a=q.get()
        b=os.getpid()
        print(a,str(b)+'a程式')
        l.release()

def b(func,l,q):
    td.Thread(target=func,args=(l,q,)).start()

def c(l,q):
    while True:
        l.acquire()
        a=q.get()
        b=os.getpid()
        print(a,str(b)+'c程式')
        l.release()

def d(func,l,q):
    t1 =td.Thread(target=func,args=(l,q,))
    t1.start()



if __name__=='__main__':
    l=mp.Manager().Lock()
    l2=mp.Manager().Lock()
    q=mp.Manager().Queue()
    q2=mp.Manager().Queue()
    pool = mp.Pool()
    pool.apply(b,(a,l,q,))
    pool.apply(b,(c,l2,q2,))
    pool.close()
    for i in range(10):
        Astr='第 '+str(i)+' 步'
        q.put(Astr)
        q2.put(Astr)
        # time.sleep(1)   
    pool.join()
