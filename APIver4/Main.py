import numpy as np
import datetime
import modin.pandas as pd
# import pandas as pd
dfdata = pd.read_csv('../data/Ticks2024-01-04.txt',header=None)
print('OK!!')
# a=dfdata.values.tolist()
# print(a[0])