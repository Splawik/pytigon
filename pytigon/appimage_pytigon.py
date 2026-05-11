"""Pytigon AppImage launcher entry point.

Sets the PYTIGON_APP_IMAGE environment flag before launching the
main pytigon runner. Used when pytigon is packaged as an AppImage.
"""

from os import environ

environ["PYTIGON_APP_IMAGE"] = "1"
from pytigon.pytigon_run import run

if __name__ == "__main__":
    run()
