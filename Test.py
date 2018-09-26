import datetime
import time
import numpy as np
import pandas as pd
class Transfor:
    name2=''
    def __init__(self,type,name):
        self.type=type
        self.name=name
        self.tickpd=pd.DataFrame(columns=['date','time','bid','ask','close','volume'])
    
    def TicktoK(self,newname):
        self.name=newname
        # return self.name


    # def TicktoK(date,time,bid,ask,close,volume):
    #     newlist=[date,time,bid,ask,close,volume]
    #     self.tickpd=self.tickpd.append(pd.DataFrame(newlist,columns=['date','time','bid','ask','close','volume']),ignore_index=True)
    #     return self.tickpd

if __name__ == '__main__' :
    A=Transfor(0,'TX00')
    A.TicktoK('MTX00')
    print(A.name)
