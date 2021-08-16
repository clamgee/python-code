import random
#列表中隨機取一
# data=random.choice([1,888,231,12,56,8465])
# print(data)
#列表中隨機娶幾個
# data=random.sample([1,888,231,12,56,8465],3)
# print(data)
#將列表中隨機調換順序(洗牌)
# data=[6521,56,8745,745,9865,56,12]
# random.shuffle(data)
# print(data)
#隨機亂數
#data=random.random() #0~1 之間
#data=random.uniform(60,100) #可以指定區間
#print(int(data))
#常態分配，中間數-+一個亂數值,但會有超過這個亂數值
#data=random.normalvariate(100,10)
#print(int(data))
## 統計
import statistics as stac
#平均數
# data=stac.mean([78,213,54,16,52,45])
# print(data)
#中位數，去除極端值
data=stac.median([78,213,54,16,52,45])
print(data)
