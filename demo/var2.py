import multiprocessing as mp
import var1
import time
class MyProcess(mp.Process):  # 定義一個Class，繼承Process類
    def __init__(self):
        super(MyProcess, self).__init__()  # 實踐父類初始化方法
        self.target = 1

    def run(self):  # 必須的，啟動進程方法
        while self.target < 10 :
            self.target += 1
            var1.glovar.set(str(self.target))
            print(var1.glovar.get())
            time.sleep(2)


