# import pandas as pd
# import numpy as np
# csvpf=pd.read_csv('result.csv')
# csvpf['ndatetime']=pd.to_datetime(csvpf['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')
# print(csvpf.index.values[-1])
# import pyqtgraph.examples
# pyqtgraph.examples.run()
import sys
import comtypes.client
import imp
try:
    import comtypes.gen.SKCOMLib as sk
    imp.find_module('SKCOMLib')
    found = True
    print(found)
except ImportError:
    found = False
    print(found)

# try:
#     import comtypes.gen.SKCOMLib as sk
#     # import extension_magic_module
# except ImportError:
#     print('NO!!')