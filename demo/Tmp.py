import pandas as pd
import multiprocessing as mp

e =mp.Event()

e.set()
e.clear()

print(e.is_set())

# A = pd.DataFrame()
# print(A.shape[0])