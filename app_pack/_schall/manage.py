#!/usr/bin/env python
import os
import sys

base_path = __file__.replace("manage.py", "")
if base_path == "":
    base_path = "./"
else:
    os.chdir(base_path)

sys.path.insert(0,base_path + "../../ext_lib")
sys.path.insert(0,base_path + "../..")

from schlib.schdjangoext.django_manage import *

if __name__ == "__main__":
    cmd(sys.argv, from_main=True)