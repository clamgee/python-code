import multiprocessing as mp
import timeit
import time
_event = mp.Event()

def func():
    for i in range(10):
        if _event.is_set() is False:
            _event.set()
        _event.wait()
        # time.sleep(0.0001)
        _event.clear()
t = timeit.timeit(func,number=100)
print(t)

# sns.set()
# Candledf=pd.read_csv('../result.dat',low_memory=False)
# Candledf['ndatetime']=pd.to_datetime(Candledf['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')


