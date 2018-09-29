import ctypes

a=12
b=ctypes.c_short(a)
c='666'
d=ctypes.c_char_p(c)
print(type(b),a,type(d),d)