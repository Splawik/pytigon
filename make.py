import os
from pathlib import Path
from shutil import copyfile

import pscript
import sass
from jsmin import jsmin

from pytigon_js_sources import PSCRIPT_SOURCES
from pytigon_lib.schindent.py_to_js import compile, prepare_python_code


def remove_duplicate_exports(input_file, output_file=None):
    """
    Removes one of two identical consecutive lines starting with 'export'.

    Args:
        input_file: Path to the input file
        output_file: Path to the output file (optional)
    """
    if output_file is None:
        output_file = input_file

    with open(input_file, encoding="utf-8") as f:
        lines = f.readlines()

    result = []
    i = 0
    while i < len(lines):
        current_line = lines[i]

        # Check if the line starts with 'export'
        if current_line.strip().startswith("export"):
            # Check if the next line is identical
            if i + 1 < len(lines) and lines[i + 1] == current_line:
                # Add only one copy (skip the duplicate)
                result.append(current_line)
                i += 2  # Skip both lines (jump by 2)
                continue

        result.append(current_line)
        i += 1

    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(result)

    removed = len(lines) - len(result)
    print(f"Processed: {len(lines)} lines")
    print(f"Duplicates removed: {removed}")
    print(f"Result saved to: {output_file}")


# def prepare_python_code(code):
#    exported_id = []
#    for line in code.split("\n"):
#        if (line.startswith("def") and not line.startswith("def _")) or (
#            line.startswith("class") and not line.startswith("class _")
#        ):
#            exported_id.append(line.split(" ")[1].split("(")[0].split(":")[0])
#    if exported_id:
#        code += "RawJS('export {" + ", ".join(exported_id) + "}')\n"
#    return code


files = PSCRIPT_SOURCES


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

with open("py_runtime.js", "w") as fout:
    fout.write(pscript.get_full_std_lib(indent=0))

with open("py_runtime.min.js", "w") as fout:
    fout.write(jsmin(pscript.get_full_std_lib(indent=0)))

with open("pytigon.js", "w") as fout:
    for file in files:
        with open(file) as fin:
            # js = pscript.py2js(prepare_python_code(fin.read()), inline_stdlib=False)

            error, js = compile(prepare_python_code(fin.read()))
            if error:
                print("Error in", file)
                print(js)
            else:
                fout.write(js)
                fout.write("\n\n")

remove_duplicate_exports("pytigon.js")

with open("pytigon.js") as fin:
    with open("pytigon.min.js", "w") as fout:
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
    with open(input_path) as f:
        print("Compile:", input_path)
        buf = sass.compile(string=f.read(), indented=True, include_paths=(parent_path,))
        with open(output_path, "w") as f2:
            f2.write(buf)
            print("Saving result in: ", output_path)


os.chdir(sass_path)

p = Path(sass_path)

for pos in p.glob("**/*.sass"):
    if not pos.stem.startswith("_"):
        print(pos.parent.as_posix())
        scss_compile(pos.parent.as_posix(), pos.name)

os.chdir(path)
