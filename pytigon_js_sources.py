"""Canonical list of pscript sources compiled into ``pytigon.js``.

Both ``make.py`` (legacy entry point) and ``tasks.py`` (``invoke build-js``)
read this list so the two build paths cannot drift apart.

The order matters: modules are concatenated into a single output file, so a
module must appear after everything it imports.

Note: ``pytigon.py`` is deliberately absent. It is a leftover pscript-module
aggregator containing a self-import (``import pytigon.py``), which makes it
fail to compile with ``PScript does not support imports``. The real client
entry point is ``pytigon_main.py``.
"""

PSCRIPT_SOURCES = [
    "__init__.py",
    "resources.py",
    "tools.py",
    "component.py",
    "ajax_region.py",
    "db.py",
    "events.py",
    "offline.py",
    "tabmenu.py",
    "tbl.py",
    "widget.py",
    "pytigon_inline.py",
    "pytigon_main.py",
]
