import os
import sys
import shutil

from cffi import FFI

os.environ["CC"] = sys.executable + " -m ziglang cc"

ffibuilder = FFI()
ffibuilder.cdef("int add(int a, int b);")
ffibuilder.set_source(
    "cffi_add",
    '#include "add.h"',
    sources=["./add.c"],
)
ffibuilder.compile(tmpdir="./src")
l = os.listdir("./src")
for item in l:
    if item.endswith(".so") or item.endswith(".dll"):
        shutil.copy(os.path.join("./src", item), "..")
