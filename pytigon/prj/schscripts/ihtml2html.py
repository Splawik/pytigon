import sys
import os

from pytigon_lib.schindent.indent_style import ihtml_to_html_base

cwd = os.getcwd()
file_name = sys.argv[-1]
print(sys.argv)
if file_name.endswith(".ihtml"):
    if file_name.startswith("//") or ":" in file_name:
        file_name2 = file_name2
    else:
        file_name2 = os.path.join(cwd, file_name)
    file_name3 = file_name2.replace(".ihtml", ".html")
    with open(file_name2, "rt", encoding="utf-8") as f:
        buf = f.read()
        print(buf)
        buf = ihtml_to_html_base(None, input_str=buf)
        with open(file_name3, "wt", encoding="utf-8") as f2:
            f2.write(buf)
