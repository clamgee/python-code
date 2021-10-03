Msgstr = 'A'
globals()['Test'+Msgstr]=['a',1,22]
import multiprocessing as mp
if __name__ == '__main__':
    global mgr,mQueue,mval
    mgr = mp.Manager()
    mQueue=mgr.Queue()
    mval = mgr.Value(str,'TX00')
    print(mval.value)