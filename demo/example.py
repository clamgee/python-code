import pandas as pd
import datetime as dt

def get_interval_days(arrLike, start, end):   
    start_date = dt.datetime.strptime(arrLike[start], '%Y-%m-%d')
    end_date = dt.datetime.strptime(arrLike[end], '%Y-%m-%d') 

    return (end_date - start_date).days


wbs = {
    "wbs": ["job1", "job2", "job3", "job4"],
    "date_from": ["2019-04-01", "2019-04-07", "2019-05-16","2019-05-20"],
    "date_to": ["2019-05-01", "2019-05-17", "2019-05-31", "2019-06-11"]
}

df = pd.DataFrame(wbs)
print(df)
df['elapsed'] = df.apply(
    get_interval_days, axis=1, args=('date_from', 'date_to'))
print(df)