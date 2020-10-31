import os
import sys
from pathlib import Path
from shutil import copyfile
import sass

path = os.getcwd()

script_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__).replace("make.py", ""), "pytigon", "static_src"
    )
)

if script_path == "":
    script_path = path
else:
    os.chdir(script_path)

# os.chdir("./static_src/")
sys.argv = ["", "--xpath", script_path, "--map", "pytigon_js/pytigon.py"]
from transcrypt.__main__ import main

sys.path.insert(0, script_path)
print(sys.path)
main()

os.chdir(script_path)

compiled_files = os.listdir("./pytigon_js/__target__/")

for name in compiled_files:
    src = os.path.join("./pytigon_js/__target__/", name)
    dst = os.path.join("../static/pytigon_js/", name)
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

p = Path("../static_src/")

for pos in p.glob("**/*.sass"):
    if not pos.stem.startswith("_"):
        scss_compile(pos.parent.as_posix(), pos.name)

os.chdir(path)
