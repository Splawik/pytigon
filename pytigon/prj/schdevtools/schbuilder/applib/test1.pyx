import cython 

#cdef extern from *:
#    """
#    static long square(long x) {return x * x / 3;}
#    """
#    long square(long x)

def sum(x:cython.int, y:cython.int) -> cython.int:

    i:cython.int
    j:cython.int
    ret:cython.int = 0

    for j in range(0,1000):
        for i in range(0,1000):
            ret += i
        for i in range(0,10001):
            ret -= i
        
    return ret
