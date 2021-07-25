import multiprocessing as mp
import queue
import threading as td
import time


def funcq(q):
    for i in range(10):
        res = i+i**2
        q.put(res)
        time.sleep(2)

def funcget(q):
    i=1
    while q.qsize!=0:
        b=q.qsize()
        a=q.get()
        print(i,a,b)
        i+=1

def fucntd(q):
    t1=td.Thread(target=funcget,args=(q,))
    t1.start()

if __name__=='__main__':
    q=mp.Queue()
    # fucntd(q)
    w1 = mp.Process(target=fucntd,args=(q,))
    w1.start()
    funcq(q)
    w1.join()


#############方法二
import multiprocessing as mp
import threading as td
import os
import time

def a(*args):
    while True:
        with args[1]:
            a=args[0].get()
            b=os.getpid()
            print(a,str(b)+'a程式')

def b(*args):
    td.Thread(target=args[0],args=(args[1],args[2])).start()

def c(*args):
    while True:
        args[1].acquire()
        a=args[0].get()
        b=os.getpid()
        print(a,str(b)+'c程式')
        args[1].release()

def d(*args):
    td.Thread(target=args[0],args=(args[1],args[2])).start()

def multiwork(func,*args):
    pool.apply(func,(args[0],args[1],args[2],))



if __name__=='__main__':
    pool = mp.Pool()
    l=mp.Manager().Lock()
    l2=mp.Manager().Lock()
    q=mp.Manager().Queue()
    q2=mp.Manager().Queue()
    multiwork(b,a,q,l)
    multiwork(d,c,q2,l2)
    pool.close()
    for i in range(10):
        Astr='第 '+str(i)+' 步'
        q.put(Astr)
        q2.put(Astr)
    pool.join()

# ==========第三種
import multiprocessing as mp
from multiprocessing.process import current_process
import threading as td
import os
import time

def a(q):
    res = []
    while q.qsize()!=0:
        # l.acquire()
        a=q.get()
        res.append([a,current_process().name,current_process().pid])
        # l.release()
    print(res[5],len(res))
    

def c(a):
    b=current_process().name
    c=current_process().pid 
    return [a,b,c]
        

def b(q):
    td.Thread(target=a,args=(q,)).start()


if __name__=='__main__':
    multiq = mp.Manager().Queue()
    q=mp.Queue()
    q1=mp.Queue()
    q2=mp.Queue()
    l = mp.Manager().RLock()
    for i in range(30000):
        res = i
        q.put(res)
        q1.put(res)
        q2.put(res)
        multiq.put(res)

    # start = time.time()
    # a(q)
    # print('Normal時間: ',time.time()-start)
    # start = time.time()
    # p1 = mp.Process(target=b,args=(q2,))
    # p1.start()
    # p1.join()
    # print('Process時間: ',time.time()-start)
    start = time.time()
    with mp.Pool() as pool:
        res=[]
        while multiq.qsize()!=0:
            a=multiq.get()
            res.append(pool.apply_async(c,(a,)).get())
        pool.close()
        pool.join()
        print(res[5],len(res))
        

    print('Pool時間: ',time.time()-start)


