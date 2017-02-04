import os
import subprocess

mime_str="""<?xml version="1.0"?>
<mime-info xmlns='http://www.freedesktop.org/standards/shared-mime-info'>
  <mime-type type="application/pytigon">
    <comment>Pytigon application</comment>
    <glob pattern="*.ptig"/>
  </mime-type>
</mime-info>
"""        

fname = "/usr/share/mime/application/pytigon.xml"

with open(fname,"wt") as f:
    f.write(mime_str)

subprocess.run(["update-mime-database", "/usr/share/mime"])

subprocess.run(["xdg-icon-resource", "install", "--context", "mimetypes",  \
    "--size", "48", "../pytigon.png", "application-pytigon"])
