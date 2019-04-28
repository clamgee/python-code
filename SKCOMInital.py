import comtypes.client as cc
import shutil
import os
from tkinter import filedialog
try:
    def GetDesktopPath():
        return os.path.join(os.path.expanduser('~'), r'AppData\Local\Programs\Python\Python37\Lib\site-packages\comtypes\gen')

    folder=GetDesktopPath()
    if os.path.exists(folder):
        # folder = filedialog.askdirectory(title=u'選擇資料夾',initialdir=(os.path.expanduser(folder)))
        print(folder)
        # shutil.rmtree(folder)
    
    fname = os.path.abspath(r'PythonExample\x64')
    fname = filedialog.askopenfilename(title=u'選擇SKCOM.dll',initialdir=(os.path.expanduser(fname)))
    print(fname)
    if os.path.exists(fname):
        cc.GetModule(fname)
        print('完成更新!!')
    else:
        print('更新失敗!!')
        os._exit(0)
except OSError as e:
    print('錯誤訊息: ',e)
    
