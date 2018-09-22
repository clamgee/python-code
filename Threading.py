import threading
import time
def fun1():
    for i in range(10):
        time.sleep(0.5)
    print('完成的工作程序: ',threading.current_thread())
def fun2():
    for i in range(10):
        time.sleep(1)
    print('完成工作程序2: %s '%threading.current_thread())

def main():
    add_thread=threading.Thread(target=fun1())
    add_thread2=threading.Thread(target=fun2())
    add_thread.start()
    add_thread2.start()
    print('完成主程序')

if __name__=='__main__' :
    main()
