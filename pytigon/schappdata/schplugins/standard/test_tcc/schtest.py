from cffi import FFI

ffi = FFI()

ffi.cdef("""
long long silnia(long long l);
char * passed(char * arg);
int free_memory(void *ptr);
void message(char * msg);
""")

C = ffi.dlopen(__file__.replace('.py','.bin'))

def silnia(l):
    ret = C.silnia(l)
    return ret

def passed(arg):
    buf = C.passed(arg.encode('utf-8'))
    ret = ffi.string(buf).decode('utf-8')
    C.free_memory(buf)
    return ret

def message(msg):
    C.message(msg.encode('utf-8'))
