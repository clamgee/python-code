
import pandas as pd
a = []
a.append([1,2,3])
a.append([4,5,6])
a.append([7,8,9])

b = pd.DataFrame(columns=[1,2,3])
b=b.append(pd.DataFrame(a,columns=[1,2,3]))

print(a)
print(b)