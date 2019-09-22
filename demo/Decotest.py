def use_logging(func):
    print("%s is running" % func.__name__)
    func()

def foo():
    print('i am foo')

use_logging(foo)