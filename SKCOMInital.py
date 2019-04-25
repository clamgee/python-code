import comtypes.client as cc
import shutil
try:
    path=r'C:\Users\Clam\AppData\Local\Programs\Python\Python37\Lib\site-packages\comtypes\gen'
    # shutil.rmtree(path)
    cc.GetModule('./PythonExample/x64/SKCOM.dll')
except OSError as e:
    print('錯誤訊息: ',e)
else:
    print('完成更新!!')