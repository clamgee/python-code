import multiprocessing as mp
import threading as td

def a(q):
    while q.qsize()!=0:
        a=q.get()
        print(a)

def b(func,q):
    t1 =td.Thread(target=func,args=(q,))
    t1.start()

if __name__=='__main__':
    q=mp.Queue()
    q.put('第一步')
    w1 = mp.Process(target=b,args=(a,q,))
    w1.start()
    q.put('第二步')

    w1.join()
