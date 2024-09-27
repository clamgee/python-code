import os
# os.environ["MODIN_ENGINE"] = "ray"
# import pandas as pd
import modin.pandas as pd
import datetime

dfMon=pd.DataFrame(columns=['ndatetime','open','high','low','close','volume'])
dfMon['ndatetime']=pd.to_datetime(dfMon['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
dfMon[['open','high','low','close','volume']]=dfMon[['open','high','low','close','volume']].astype(int)
# print(dfMon.shape)

domain=os.listdir('../data/')
checkMon=0
# 取得當月第幾週
def get_week_of_month(ndate): 
    end = int(datetime.datetime(ndate.year, ndate.month, ndate.day).strftime("%W"))
    begin = int(datetime.datetime(ndate.year, ndate.month, 1).strftime("%W"))
    if datetime.datetime(ndate.year, ndate.month, 1).weekday()>2:
        if (end - begin + 1)==4:
            result = True
        else:
            result = False
    else:
        if (end - begin + 1)==3:
            result = True
        else:
            result = False 
    return result
# print(domain[-1].strip('Ticks').strip('.txt'))
# print(ndate,type(ndate))
for info in domain:
    if info != 'filename.txt':
        ndate=datetime.datetime.strptime(info.strip('Ticks').strip('.txt'),'%Y-%m-%d').date()
        week = get_week_of_month(ndate)
        is_third_thurs = (ndate.weekday() == 3 and week)

        if is_third_thurs==False and (ndate.month!=checkMon and ndate.month<3) and ndate.weekday()>2 and week:
            is_third_thurs = True
        df1=pd.read_csv('../data/'+info,header=None)
        df1[0]=pd.to_datetime(df1[0],format='ISO8601')
        # df1[0]=pd.to_datetime(df1[0],format='%Y-%m-%d %H:%M:%S.%f')
        # if is_third_thurs:
        if dfMon.shape[0]==0 or is_third_thurs:
            end = int(datetime.datetime(ndate.year, ndate.month, ndate.day).strftime("%W"))
            begin = int(datetime.datetime(ndate.year, ndate.month, 1).strftime("%W"))
            print(info,', 第幾週: ',(end-begin+1),datetime.datetime(ndate.year, ndate.month, 1).weekday())
            tmplist=[[df1.iloc[-1,0],df1.iloc[0,3],df1[3].max(),df1[3].min(),df1.iloc[-1,3],df1[4].sum()]]
            dfMon=pd.concat([dfMon,pd.DataFrame(tmplist,columns=['ndatetime','open','high','low','close','volume'])],ignore_index=True)
            checkMon = ndate.month
        else:
            dfMon.iloc[-1,0]=df1.iloc[-1,0]
            dfMon.iloc[-1,2]=max(dfMon.iloc[-1,2],df1[3].max())
            dfMon.iloc[-1,3]=min(dfMon.iloc[-1,3],df1[3].min())
            dfMon.iloc[-1,4]=df1.iloc[-1,3]
            dfMon.iloc[-1,5]=dfMon.iloc[-1,5]+df1[4].sum()

print(dfMon.tail())
# dfMon.to_csv('MonKline.dat',header=True,index=False,mode='w')
        # if is_third_thurs :
        #     print(is_third_thurs,ndate)
    


# df=pd.read_csv('../data/'+domain[-1],header=None)
# df.columns=['ndatetime','nBid','nAsk','nClose','nQty']
# df['ndatetime'] = pd.to_datetime(df['ndatetime'], format='%Y-%m-%d %H:%M:%S.%f')
# df.sort_values(by=['ndatetime'],ascending=True)
# df.reset_index(drop=True)
# print(df.nClose.max(),df.nClose.min())
# print(df.iloc[-1,0].date().weekday(),datetime.datetime.today().weekday())
import pyqtgraph as pg
from pyqtgraph import GraphicsLayoutWidget,QtCore,QtGui,GraphicsItem

class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data  ## data must have fields: time, open, close, min, max
        self.generatePicture()
    
    def generatePicture(self):
        ## pre-computing a QPicture object allows paint() to run much more quickly, 
        ## rather than re-drawing the shapes every time.
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        w=1/3
        # w = (self.data[1][0] - self.data[0][0]) / 3.
        for (t, x) in self.data.loc[0:self.data.last_valid_index(), ['open', 'high', 'low', 'close']].iterrows():
            # picture = QtGui.QPicture()
            # p = QtGui.QPainter(picture)
            if x.open>x.close:
                p.setBrush(pg.mkBrush('g'))
                p.setPen(pg.mkPen('g'))
            elif x.open<x.close:
                p.setBrush(pg.mkBrush('r'))
                p.setPen(pg.mkPen('r'))
            else:
                p.setBrush(pg.mkBrush('w'))
                p.setPen(pg.mkPen('w'))
            p.drawLine(QtCore.QPointF(t, x.low), QtCore.QPointF(t, x.high))
            p.drawRect(QtCore.QRectF(t-w, x.open, w*2, x.close-x.open))
        p.end()
            # self.pictures.append(picture)
        # for (t, open, close, min, max) in self.data:
        #     p.drawLine(QtCore.QPointF(t, min), QtCore.QPointF(t, max))
        #     if open > close:
        #         p.setBrush(pg.mkBrush('r'))
        #     else:
        #         p.setBrush(pg.mkBrush('g'))
        #     p.drawRect(QtCore.QRectF(t-w, open, w*2, close-open))
        # p.end()
    
    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
    
    def boundingRect(self):
        ## boundingRect _must_ indicate the entire area that will be drawn on
        ## or else we will get artifacts and possibly crashing.
        ## (in this case, QPicture does all the work of computing the bouning rect for us)
        return QtCore.QRectF(self.picture.boundingRect())

dict_tmp = dfMon['ndatetime'].dt.strftime('%Y/%m/%d %H:%M:%S.%f').to_dict()
kline=CandlestickItem(dfMon)
pic = pg.plot()
MyAxis = pg.AxisItem(orientation='bottom')
MyAxis.setTicks([dict_tmp.items()])
# pic.addPlot(row=0,col=0,axisItems={'bottom': MyAxis},y=dfMon)
pic.addItem(kline)
pic.get

if __name__ == '__main__':
    pg.exec()