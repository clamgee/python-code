from multiprocessing import Queue
import multiprocessing as mp
import time
class Test:
    def __init__(self,inputevent) -> None:
        self.num = 0
        self.__event = inputevent

    def func(self):
        while True:
            self.__event.wait()
            print('1',self.__event.wait())
            print('wait....')
            self.num+=1
            print(self.num)
            print('2',self.__event.is_set())
            self.__event.clear()
        



if __name__ == '__main__':
    global mgr,mQueue,mval
    mgr = mp.Manager()
    mQueue=mgr.Queue()
    e = mp.Event()
    A = Test(e)
    p = mp.Process(target=A.func)
    p.start()
    i = 0
    while i < 10000 :
        e.set()
        i+=1
        time.sleep(0.1)
    # mQueue.get(block=True,timeout=None)
    # mval = mgr.Value(str,'TX00')
