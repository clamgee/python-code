class decorateClass(object):
    def __init__(self, f):
        self.f = f
    
    def __call__(self, *args, **kwargs):
        print(f"do something before calling function {self.f.__name__}")
        self.f(*args, **kwargs)
        print(*args, **kwargs)
        print("AAA")

@decorateClass
def myFunc():
    A=1+1
    A=str(A)
    return A
    # print("運算結果: "+str(A))

if __name__ == '__main__':
    myFunc()