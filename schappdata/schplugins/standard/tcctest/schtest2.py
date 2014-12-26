import schtest 
import time

def spr_test():
    x1 = time.clock()
    ret= schtest.test_loop()
    #print(dir(schtest))
    x2 = time.clock()
    print(x2-x1)
    return ret

print(spr_test())