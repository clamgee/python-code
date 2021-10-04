from multiprocessing import Queue


Msgstr = 'A'
globals()['Test'+Msgstr]= Queue()
import multiprocessing as mp
if __name__ == '__main__':
    global mgr,mQueue,mval
    mgr = mp.Manager()
    mQueue=mgr.Queue()
    mval = mgr.Value(str,'TX00')
    print(mval.value)
    mval.value = ('TXF00')
    print(globals()['Test'+Msgstr])
    setattr(globals()['Test'+Msgstr],'idx',str(00))
    print(globals()['Test'+Msgstr].idx)
    print(mval.value)