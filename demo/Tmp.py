import multiprocessing as mp
import threading as td
import os
import time

def a(*args):
    print(len(args))
    while True:
        args[1].acquire()
        a=args[0].get()
        b=os.getpid()
        print(a,str(b)+'a程式')
        args[1].release()

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
    # pool = mp.Pool()
    # pool.apply(b,(a,l,q,))
    multiwork(b,a,q,l)
    multiwork(d,c,q2,l2)
    pool.close()
    pool.join()
    for i in range(10):
        Astr='第 '+str(i)+' 步'
        q.put(Astr)
        q2.put(Astr)
    # pool.apply(b,(c,l2,q2,))
    # pool.close()
        # time.sleep(1)   
    # pool.join()
