import pandas as pd
import os

domain = os.listdir("./data")
direct = os.path.abspath("./data")
file = direct + "\\Ticks2025-03-24.txt"
print(file)

alldayticks = pd.read_csv(file, header=None, names=["ndatetime", "nbid", "nask", "close", "volume", "deal"], low_memory=False)
alldayticks["ndatetime"] = pd.to_datetime(alldayticks["ndatetime"],format='mixed')
# # alldayticks["ms_len"]=alldayticks["ndatetime"].dt.strftime('%f').str[:3].str.len()
alldayticks["ms_len"]=alldayticks["ndatetime"].dt.strftime('%f').str.slice(stop=-3).str.rstrip('000').str.len()
# print(alldayticks[alldayticks["ms_len"] !=3])
print(alldayticks.tail())
# print(alldayticks[alldayticks["ndatetime"].dt.strftime('%f').str.rstrip('0').str.len() != 3])
# print(alldayticks.head())