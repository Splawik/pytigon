"""CFFI bridge to TCC-compiled C test functions.

Loads a shared library (.bin) compiled by TCC and exposes
its functions as Python callables.
"""

from cffi import FFI

ffi = FFI()

ffi.cdef("""
long long silnia(long long l);
char * passed(char * arg);
int free_memory(void *ptr);
void message(char * msg);
""")

# Load the compiled shared library (same base name, .bin extension)
C = ffi.dlopen(__file__.replace(".py", ".bin"))


def silnia(l):
    """Compute the factorial using the C implementation.

    Args:
        l: Input number.

    Returns:
        Factorial of l (long long).
    """
    return C.silnia(l)


def passed(arg):
    """Call the C 'passed' function and return the result as a string.

    Args:
        arg: String argument to pass to C.

    Returns:
        Result string from the C function.
    """
    buf = C.passed(arg.encode("utf-8"))
    ret = ffi.string(buf).decode("utf-8")
    C.free_memory(buf)
    return ret


def message(msg):
    """Send a message to the C 'message' function.

    Args:
        msg: Message string to send.
    """
    C.message(msg.encode("utf-8"))
