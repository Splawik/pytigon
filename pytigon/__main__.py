#!/usr/bin/env python
"""Pytigon entry point for ``python -m pytigon``.

author: Sławomir Chołaj (slawomir.cholaj@gmail.com)
license: LGPL 3.0
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from pytigon_run import run
except ImportError:
    from pytigon.pytigon_run import run

if __name__ == "__main__":
    run()
