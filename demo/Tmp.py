import threading as td
import multiprocessing as mp

def Func(a,b):
    print(a,b)

t1 = td.Thread(target=Func,args=('clam','sivve'))
t1.start()
p1 = mp.Process(target=t1,args=())
p1.start()
t1.join()
p1.join()