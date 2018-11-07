def chart():    
    hist_data = ts.get_hist_data('600519',start='2017-05-01',end='2017-11-24')    
    data_list = []    
    for dates,row in hist_data.iterrows():        
        # 將時間轉換為數字# 
        date_time = datetime.datetime.strptime(dates,'%Y-%m-%d')        
        t = date2num(date_time)        
        t = dict(enumerate(datetime))        
        open,high,close,low = row[:4]        
        datas = (t,open,close,low,high)        
        data_list.append(datas)    
    axis_dict = dict(enumerate(axis))    
    item = CandlestickItem(data_list)    
    plt = pg.PlotWidget()    
    plt.addItem(item,)    
    plt.showGrid(x=True,y=True)    
    return plt