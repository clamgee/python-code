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
from multiprocessing.process import current_process
import threading as td
import os
import time

def a(*args):
    while args[0].qsize>0:
        with args[1]:
            a=args[0].get()
            b=os.getpid()
            print(a,str(b)+'a程式, 程序: ',current_process().name)

def b(*args):
    t1=td.Thread(target=args[0],args=(args[1],args[2]))
    t1.start()

def c(*args):
    while True:
        args[1].acquire()
        a=args[0].get()
        b=os.getpid()
        print(a,str(b)+'c程式, 程序: ',current_process().name)
        args[1].release()

def d(*args):
    t1=td.Thread(target=args[0],args=(args[1],args[2]))
    t1.start()


def Pwork(func,*args):
    start = time.time()
    p1=mp.Process(target=func,args=(args[0],args[1],args[2],))
    p1.start()
    p1.join()
    end = time.time()
    print('process時間: ',end - start)

def multiwork(func,*args):
    start = time.time()
    with mp.Pool() as pool:
        pool.apply(func,(args[0],args[1],args[2],))
    end = time.time()
    print('pool時間: ',end - start)



if __name__=='__main__':
    # pool = mp.Pool()
    l=mp.Lock()
    l2=mp.Manager().RLock()
    q=mp.Queue()
    q2=mp.Manager().Queue()
    for i in range(10):
        Astr='第 '+str(i)+' 步'
        q.put(Astr)
        q2.put(Astr)
    # multiwork(d,c,q2,l2)
    Pwork(b,a,q,l)
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


# ====== 各種比較
import multiprocessing as mp
from multiprocessing import current_process
import threading as td
import time


def funcq(q,mq,asyncq):
    for i in range(30000):
        res = i+i**2
        q.put(res)
        mq.put(res)
        asyncq.put(res)

def funcgetp(*args):
    res=[]
    while args[0].qsize()>0:
        with args[1]:
            a=args[0].get()
            c=current_process().name
            res.append([a,c])
            # print('Process:',a,c)
    print('Process: ',res[8],', len: ',len(res))
    


def funcgetm(*args):
    res=[]
    # print('Multi Queue: ',args[0].qsize())
    while args[0].qsize()>0:
        # args[1].acquire()
        a=args[0].get()
        c=current_process().name
        res.append([a,c])
        # print('Multi: ',a,c)
        # args[1].release()
    print('Multi: ',res[8],', len: ',len(res))  

def funcgetasync(*args):
    a=[args[0],current_process().name]
    return a


def functd(*args):
    # print('thread',args[0],args[1])
    t1=td.Thread(target=args[0],args=(args[1],args[2],))
    t1.start()

def Pwork(func,*args):
    # print('work',len(args),args[0],args[1])
    start = time.time()
    w1 = mp.Process(target=func,args=(args[0],args[1],args[2],))
    w1.start()
    w1.join()
    print('Process',time.time()-start)

def Multiwork(func,*args):
    # print('work',len(args),args[0],args[1])
    start=time.time()
    pool=mp.Pool()
    pool.apply(func,(args[0],args[1],args[2],))
    pool.close()
    pool.join()
    print('Mulit',time.time()-start)

def Asyncwork(func,*args):
    pool=mp.Pool()
    res=[]
    start=time.time()
    while args[0].qsize()>0:
        a = args[0].get()
        res.append(pool.apply_async(func,(a,)))
    pool.close()    
    pool.join()
    print('Async: ',res[8],', len: ',len(res))
    print('Async',time.time()-start)


if __name__=='__main__':
    q=mp.Queue()
    l=mp.Lock()
    mq=mp.Manager().Queue()
    ml=mp.Manager().RLock()
    asyncq=mp.Manager().Queue()
    funcq(q,mq,asyncq)
    Pwork(functd,funcgetp,q,l)
    Multiwork(functd,funcgetm,mq,ml)
    Asyncwork(funcgetasync,asyncq)
    
