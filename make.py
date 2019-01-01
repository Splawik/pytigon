import os
import sys
from pathlib import Path
import sass

path = os.getcwd()

WD_PATH = os.path.join(os.getcwd(), '..')
script_path = os.path.dirname(__file__).replace("make.py","")

if script_path == '':
    script_path = path
else:
    os.chdir(script_path)

os.chdir("./static_src/sch")
sys.argv = ["", "--xpath", script_path, "-n", "pytigon.py"]
print(os.getcwd())
from transcrypt.__main__ import main
sys.path.insert(0, script_path)
print(sys.path)
main()

os.chdir(script_path)

with open("./static_src/sch/__javascript__/pytigon.js", "rt") as fin:
    with open("./static/sch/pytigon.js", "wt") as fout:
        prg = fin.read()
        #x = prg.split("__all__.__call__ = __call__;")
        x = prg.split("__all__.__setslice__ = __setslice__;")
        if len(x) == 2:
            x0 = x[0].replace("function pytigon () {", "")
            x1 = "\n\nfunction pytigon () {" + x[1]
            #xx = x0 + "__all__.__call__ = __call__;" + x1
            xx = x0 + "__all__.__setslice__ = __setslice__;" + x1
            fout.write(xx)

def scss_compile(parent_path, name):
    input_path = os.path.join(parent_path, name)
    output_path = os.path.join(parent_path.replace('static_src','static'), name.replace('.sass', '.css'))        
    with open(input_path, "rt") as f:
        print("Compile:", input_path)
        buf = sass.compile(string=f.read(), indented=True, include_paths=(parent_path,))
        with open(output_path, "wt") as f2:
            f2.write(buf)
            print("Saving result in: ", output_path)

p = Path('./static_src/')

for pos in p.glob('**/*.sass'):
    if not pos.stem.startswith('_'):
        scss_compile(pos.parent.as_posix(), pos.name)

os.chdir(path)
