import multiprocessing as mp
from multiprocessing import current_process
import threading as td
import time,os
from pyqtgraph import GraphicsLayoutWidget

# from PySide6.QtCore import Object

class DatatoQueue(object):
    def __init__(self) -> None:
        super().__init__()
        self.queue=mp.Queue()
        self.idx = 4196

def funcq(q,mq,asyncq):
    for i in range(30):
        res = i+i**2
        q.put(res)
        mq.put(res)
        asyncq.put(res)

def funcgetp(*args):
    res=[]
    print('傳入get Q:',args[0])
    while True:
        with args[1]:
            a=args[0].get()
            c=current_process().name
            res.append([a,c])
            print('執行結果Process:',a,c)
    


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
    global q
    print('執行續Q:', args[1])
    t1=td.Thread(target=args[0],args=(args[1],args[2],))
    t1.start()

def Pwork(func,*args):
    # print('work',len(args),args[0],args[1])
    print('Proc stock Q:',args[1])
    start = time.time()
    w1 = mp.Process(target=func,args=(args[0],args[1],args[2],),daemon=True)
    w1.run()
    # w1.join()
    
    print('Process',time.time()-start,os.getpid())

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
    q = mp.Queue()
    print('建立Q: ',q)
    l=mp.Lock()
    mq=mp.Manager().Queue()
    ml=mp.Manager().RLock()
    asyncq=mp.Manager().Queue()
    Pwork(functd,funcgetp,q,l)
    funcq(q,mq,asyncq)
    # Multiwork(functd,funcgetm,mq,ml)
    # Asyncwork(funcgetasync,asyncq)


# import sys
# from PySide6 import QtCore,QtWidgets
# import typing
# # define a new slot that receives a string and has
# # 'saySomeWords' as its name
# class Communicate(QtCore.QObject):
#     speak = QtCore.Signal(str)
#     def __init__(self):
#         super(Communicate, self).__init__()
#         self.ButtonA = None
#         print('in class %s',self.ButtonA)
#         self.speak.connect(self.saySomeWords)
#     @QtCore.Slot(str)
#     def saySomeWords(self,words):
#         print(words)

# if __name__=='__main__':
#     someone = Communicate()
#     # connect signal and slot
#     # someone.speak.connect(saySomeWords)
#     # emit 'speak' signal
#     someone.speak.emit("Hello everybody!")