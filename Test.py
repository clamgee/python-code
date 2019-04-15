import sys
print(sys.getdefaultencoding())     # 打印出目前系統字符編碼

s1 = u"人生苦短"
s2 = s1.encode('utf-8')
print(s1,len(s1),type(s1))
print(s2,len(s2),type(s2))
# s2 = unicode("人生苦短", "utf-8")