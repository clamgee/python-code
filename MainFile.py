#寫入檔案
# file = open("data.txt",mode="w",encoding="utf-8") #開啟
# file.write("中文測試!\n 有無成功") #寫入
# file.close()
#使用 with 來開啟檔案
# with open("data2.txt",mode="w",encoding="utf-8") as file:
#     file.write("中文測試!\n 有無成功") #寫入
# with open("data.txt",mode="r",encoding="utf-8") as file:
#     data=file.read()
#     print(data)

#將檔案中有意義的數字一行行取出
# with open("data2.txt",mode="w",encoding="utf-8") as file:
#      file.write("5\n3") #寫入
#將數字取出一行行加總
# sum=0
# with open("data2.txt",mode="r",encoding="utf-8") as file:
#     for line in file:
#         sum=sum+int(line)
# print(sum)
## Jason 格式
import json
with open("Config.json",mode="r",encoding="utf-8") as file:
    data=json.load(file)
print(data)
print("名稱:",data["Name"])
print("版本:",data["Version"])
data["Name"]="中文名"
with open("Config.json",mode="w",encoding="utf-8") as file:
    json.dump(data,file)
