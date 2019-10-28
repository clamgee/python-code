def ndouble(x):
    return x*2

def nsquare(x):
    return x**2

def recuclate(getNum):
    k=5
    i=k+getNum(k)
    return i

print(recuclate(ndouble),recuclate(nsquare))