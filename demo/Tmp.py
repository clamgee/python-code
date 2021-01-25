# import pandas as pd
# import os

# domain=os.listdir('../APIver1/data')
# print(domain[-1])
# tmp=pd.read_csv('../APIver1/data/'+domain[-1])
# tmp.rename(columns={
#     tmp.columns[0]: 'ndate',
#     tmp.columns[1]: 'ntime',
#     tmp.columns[2]: 'nbid',
#     tmp.columns[3]: 'nask',
#     tmp.columns[4]: 'close',
#     tmp.columns[5]: 'volume',
# }, inplace=True)
# print(tmp.tail(5))

import json
with open("IDPW.json",mode="r",encoding="utf-8") as file:
    data = json.load(file)

print("ID: ", data["ID"])
print("PW: ",data["PW"])


