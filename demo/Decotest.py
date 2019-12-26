class decorateClass(object):
    def __init__(self, f):
        self.f = f
    
    def __call__(self, *args, **kwargs):
        print(f"do something before calling function {self.f.__name__}")
        self.f(*args, **kwargs)
        print(f"do something after calling function {self.f.__name__}")

@decorateClass
def myFunc():
    print('主程式')

if __name__ == '__main__':
    myFunc()