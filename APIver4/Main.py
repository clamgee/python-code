import os
os.environ["MODIN_ENGINE"] = "ray"
import numpy as np
import datetime
import modin.pandas as pd
# import pandas as pd
dfdata = pd.read_csv('../result.dat',header=None)
# print('OK!!')
# a=dfdata.values.tolist()
print(dfdata.head())