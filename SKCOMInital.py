import comtypes.client as cc
import shutil
import os
import sys
import re
from tkinter import filedialog
# try:
#     def GetDesktopPath():
#         return os.path.join(os.path.expanduser('~'), r'AppData\Local\Programs\Python\Python37\Lib\site-packages\comtypes\gen')

#     folder=GetDesktopPath()
#     if os.path.exists(folder):
#         print(os.path.exists(folder))
#         print(folder)
#         shutil.rmtree(folder)
#         os.mkdir(folder)
#     elif not os.path.exists(folder) :
#         os.mkdir(folder)
#     else :
#         print('未安裝!!')
#     # cc.GetModule(r'./PythonExample/x64/SKCOM.dll')
#     fname = os.path.abspath(r'PythonExample\x64')
#     fname = filedialog.askopenfilename(title=u'選擇SKCOM.dll',initialdir=(os.path.expanduser(fname)))
#     print(fname)
#     if os.path.exists(fname):
#         cc.GetModule(fname)
#         print('完成更新!!')
#     else:
#         print('更新失敗!!')
#         os._exit(0)
# except OSError as e:
#     print('錯誤訊息: ',e)
# print(os.path.expanduser('~'))
# print(os.environ)
# print(os.path.expandvars${var})
paths=sys.path
# print(paths)
for path in paths:
    print(path)
    # pattern='Users+AppData+Local+Programs+Python+lib+site-packages'
    # pattern=r'lib\\site-packages'
    # pattern=r'AppData\\Local\\Programs\\Python'
    pattern=os.path.expanduser('~')
    target=re.search(pattern,path)
    print(target)
