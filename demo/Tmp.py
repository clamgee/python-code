import datetime
# 取得當月第幾週
def get_week_of_month(ndate): 
    end = int(datetime.datetime(ndate.year, ndate.month, ndate.day).strftime("%W"))
    begin = int(datetime.datetime(ndate.year, ndate.month, 1).strftime("%W"))
    return end - begin + 1