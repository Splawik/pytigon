#!/usr/bin/env python

"""Pytigon CLI entry point (ptig command).

The ``ptig`` command is the primary command-line interface for pytigon.
It supports project initialization, running scripts, managing web servers,
and other administrative tasks.

author: Sławomir Chołaj (slawomir.cholaj@gmail.com)
license: LGPL 3.0
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from pytigon_run import run
except ImportError:
    from pytigon.pytigon_run import run


def init(prj_name):
    """Initialize a new pytigon project.

    Args:
        prj_name: Name of the project to initialize.
    """
    run(["ptig", f"init_{prj_name}"])


if __name__ == "__main__":
    run()
