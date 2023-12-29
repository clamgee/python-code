import multiprocessing as mp

def varinital():
    global ns
    ns = mp.Manager().Namespace()
    ns.nlist = []
    global glovar
    glovar = mp.Manager().Value(str,'')
