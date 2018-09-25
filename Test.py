class t1():
    def a():
        a=55
        b=45
        x=function(a,b)
        return x

    def b():
        b=100
        return b
        
    def c(x):
        c=x**2
        return c

def function(a,b):
    x=a*b
    return x

if __name__ == '__main__' :
    print(t1.a())
    print(t1.b())
    print(t1.c(5))