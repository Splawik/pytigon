import os
import sys
from pathlib import Path
from shutil import copyfile
import sass

import pscript
from jsmin import jsmin


def prepare_python_code(code):
    exported_id = []
    for line in code.split("\n"):
        if (line.startswith("def") and not line.startswith("def _")) or (
            line.startswith("class") and not line.startswith("class _")
        ):
            exported_id.append(line.split(" ")[1].split("(")[0].split(":")[0])
    if exported_id:
        code += "RawJS('export {" + ", ".join(exported_id) + "}')\n"
    return code


files = [
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
    "pytigon.py",
]


path = os.getcwd()

script_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__).replace("make.py", ""),
        "pytigon",
        "static_src",
        "pytigon_js",
    )
)

sass_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__).replace("make.py", ""),
        "pytigon",
        "static_src",
        "themes",
    )
)


if script_path == "":
    script_path = path
else:
    os.chdir(script_path)

with open("py_runtime.js", "wt") as fout:
    fout.write(pscript.get_full_std_lib(indent=0))

with open("py_runtime.min.js", "wt") as fout:
    fout.write(jsmin(pscript.get_full_std_lib(indent=0)))

with open("pytigon.js", "wt") as fout:
    for file in files:
        with open(file, "rt") as fin:
            js = pscript.py2js(prepare_python_code(fin.read()), inline_stdlib=False)
            fout.write(js)
            fout.write("\n\n")

with open("pytigon.js", "rt") as fin:
    with open("pytigon.min.js", "wt") as fout:
        js = fin.read()
        fout.write(jsmin(js))

os.chdir(script_path)

compiled_files = ["pytigon.js", "py_runtime.js", "pytigon.min.js", "py_runtime.min.js"]

for name in compiled_files:
    src = os.path.join("./", name)
    dst = os.path.join("../../static/pytigon_js/", name)
    print(src, "=>", dst)
    copyfile(src, dst)


def scss_compile(parent_path, name):
    input_path = os.path.join(parent_path, name)
    output_path = os.path.join(
        parent_path.replace("static_src", "static"), name.replace(".sass", ".css")
    )
    with open(input_path, "rt") as f:
        print("Compile:", input_path)
        buf = sass.compile(string=f.read(), indented=True, include_paths=(parent_path,))
        with open(output_path, "wt") as f2:
            f2.write(buf)
            print("Saving result in: ", output_path)


os.chdir(sass_path)

p = Path(sass_path)

for pos in p.glob("**/*.sass"):
    if not pos.stem.startswith("_"):
        print(pos.parent.as_posix())
        scss_compile(pos.parent.as_posix(), pos.name)

os.chdir(path)
