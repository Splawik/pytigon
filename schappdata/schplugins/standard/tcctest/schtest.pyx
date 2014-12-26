#import time


def test_loop():
    cdef long long i, sum, maxx
    maxx = 10000000

    sum = 0
    i = 0
    while i<maxx:
        sum = sum+i
        i=i+1

    sum2 = sum
    return sum2

#def spr_test():
#    x1 = time.clock()
#    test_loop()
#    x2 = time.clock()
#    print(x2-x1)


#spr_test()