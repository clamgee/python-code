try:
    import comtypes.gen.SKCOMLib as sk
    found=True
    path=sk.__file__
    a=path.index('_')-1
    path=path[:a]
    print(path)
except ImportError:
    found=False

print(found)
######以上需要


# import comtypes.gen.SKCOMLib as sk
# path=sk.__file__
# a=path.index('_')-1
# path=path[:a]

# print(path)