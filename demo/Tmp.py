import multiprocessing as mp
from multiprocessing.process import current_process
import threading as td
import os
import time

def a(*args):
    while args[0].qsize!=0:
        with args[1]:
            a=args[0].get()
            b=os.getpid()
            print(a,str(b)+'a程式, 程序: ',current_process().name)

def b(*args):
    td.Thread(target=args[0],args=(args[1],args[2])).start()

def c(*args):
    while True:
        args[1].acquire()
        a=args[0].get()
        b=os.getpid()
        print(a,str(b)+'c程式, 程序: ',current_process().name)
        args[1].release()

def d(*args):
    td.Thread(target=args[0],args=(args[1],args[2])).start()

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
    Pwork(b,a,q,l)
    multiwork(d,c,q2,l2)

