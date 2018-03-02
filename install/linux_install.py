import os
import subprocess

s = None
fname =  os.path.expanduser("~/.config/mimeapps.list")
find_str = "[Default Applications]"
add_str = "application/pytigon=pytigon.desktop"

with open(fname,"rt") as f:
    s = f.read()

if s:
    if not add_str in s:
        if find_str in s:
            s = s.replace(find_str, find_str+"\n"+add_str)
        else:
            s = s+ "\n" + find_str + "\n" + add_str
        with open(fname,"wt") as f:
            f.write(s)

desktop_str="""[Desktop Entry]
Type=Application
Name=pytigon
Exec=%s/python/bin/python %s/pytigon.py %%f
Categories=Other
NoDisplay=true
MimeType=application/pytigon
Terminal=false
X-KeepTerminal=false
"""        

base_path = __file__.replace("linux_install.py", "")
if base_path == "":
    base_path = os.getcwd()
else:
    os.chdir(base_path)

pytigon_path = os.path.normpath(os.path.join(base_path, ".."))
desktop_str2 = desktop_str % (pytigon_path, pytigon_path)

fname2 = os.path.expanduser("~/.local/share/applications/pytigon.desktop")
#if not os.path.exists(fname2):
with open(fname2,"wt") as f:
    f.write(desktop_str2)


mime_str="""<?xml version="1.0"?>
<mime-info xmlns='http://www.freedesktop.org/standards/shared-mime-info'>
  <mime-type type="application/pytigon">
    <comment>Pytigon application</comment>
    <glob pattern="*.ptig"/>
  </mime-type>
</mime-info>
"""

fname = os.path.expanduser("~/.local/share/mime/packages/pytigon.xml")

with open(fname,"wt") as f:
    f.write(mime_str)

subprocess.run(["update-mime-database", os.path.expanduser("~/.local/share/mime")])

subprocess.run(["xdg-icon-resource", "install", "--context", "mimetypes",  \
    "--size", "48", "../pytigon.png", "application-pytigon"])
