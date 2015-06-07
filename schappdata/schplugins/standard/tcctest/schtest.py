from cffi import FFI

ffi = FFI()

ffi.cdef("""long long silnia(long long l);""")

C = ffi.dlopen(__file__.replace('.py','.bin'))

def silnia(l):
    ret = C.silnia(l)
    return ret
