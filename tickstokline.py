#匯入所需module
import datetime
import time
import numpy as np
import pandas as pd


class dataprocess:
    def __init__(self,type,name):
        self.name=name
        self.type=type
        self.klinepd=pd.DataFrame(columns=['date','time','open','high','low','close','volume'])
        self.newlist=[]
        self.tmpcontract=0
    
    def Ticks(self,sMarketNo,sIndex,nPtr,nTimehms,nTimemillismicros,nBid,nAsk,nClose,nQty,nSimulate):
        nTime=str(nTimehms)
        while len(nTime)<6:
            nTime='0'+nTime
        nTimemicro=str(nTimemillismicros)
        while len(nTimemicro)<6:
            nTimemicro='0'+nTimemicro
        nTime=datetime.datetime.strptime(nTime,'%H%M%S').strftime('%H:%M:%S')+"."+nTimemicro.strip()
        nDate=datetime.datetime.now().strftime('%Y/%m/%d')
        self.newlist=[nDate,nTime,int(nBid/100),int(nAsk/100),int(nClose/100),int(nQty)]
        # return self.newlist
    
    def contractk(self):
        if self.tmpcontract=0:
            
