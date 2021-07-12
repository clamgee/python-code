import threading as td
import multiprocessing as mp
import time
import os

def Func(a,b):
    i=0
    while i<20:
        print(i,a,b)
        time.sleep(3)
        print('process id:', os.getpid())
        i+=1

def ThdFucn():
    t1 = td.Thread(target=Func,args=('clam','sivve'))
    t1.start()
    print('Thread.daemon = %s' % t1.daemon)

    # t1.join()

if __name__=='__main__':
    p1 = mp.Process(target=ThdFucn)
    p1.start()
    print('Process.daemon = %s' % p1.daemon)
    print('process id:', os.getpid())
