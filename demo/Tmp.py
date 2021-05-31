import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QTableWidgetItem
bestfive = pd.DataFrame(np.arange(24).reshape(6,4), columns=['bidQty','nbid','nask','askQty'])
bestfive = bestfive.astype(int)
bestfive['bidQtyitem']=''
bestfive['nbiditem']=''
bestfive['naskitem']=''
bestfive['askQtyitem']=''
i=0
while i < 6:
    bestfive.at[i, 'bidQtyitem'] = QTableWidgetItem('')
    bestfive.at[i, 'nbiditem'] = QTableWidgetItem('')
    bestfive.at[i, 'naskitem'] = QTableWidgetItem('')
    bestfive.at[i, 'askQtyitem'] = QTableWidgetItem('')
    i+=1

total_dict={'bidQtyitem':{0:'a',1:'b',2:'c',3:'d',4:'e',5:'f'}}
bestfive['bidQtyitem'].se

print(bestfive)