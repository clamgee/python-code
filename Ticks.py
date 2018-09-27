import datetime
import time
import numpy as np
import pandas as pd

TicktoK = pd.DataFrame(columns=['date','time','bid','ask','close','volume'])
ndate = datetime.datetime.now().strftime("%Y/%m/%d")

def function():
    global ndate
    global TicktoK
    n=0
    ntime=datetime.datetime.now().strftime("%H:%M:%S.%f")
    while n < 10 :
        nlist=[ndate,ntime,10998,10999,10999,1]
        TicktoK=self.append(pd.DataFrame(nlist,columns=['date','time','bid','ask','close','volume']),ignore_index=True)
        n+=1
    print(nlist)
function()
