import multiprocessing as mp
import queue
import threading as td
import time


def funcq(q):
    for i in range(10):
        res = i+i**2
        q.put(res)
        # time.sleep(2)

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





