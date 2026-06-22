"""Build and maintenance tasks for Pytigon.

Usage:
    invoke build        # Full build (JS + CSS)
    invoke build-js     # Compile Python to JavaScript
    invoke build-css    # Compile SASS to CSS
    invoke build-templates  # Compile .ihtml templates
    invoke clean        # Remove build artifacts
    invoke lint         # Run ruff linter
    invoke format       # Run ruff formatter
    invoke test         # Run pytest
    invoke typecheck    # Run mypy
"""

import os
import sys
from contextlib import chdir
from pathlib import Path
from shutil import copyfile

from invoke import task

ROOT = Path(__file__).parent
STATIC_SRC = ROOT / "pytigon" / "static_src"
STATIC = ROOT / "pytigon" / "static"
JS_SRC = STATIC_SRC / "pytigon_js"
THEMES_SRC = STATIC_SRC / "themes"


@task
def build(ctx):
    """Full build: JS + CSS."""
    build_js(ctx)
    build_css(ctx)


@task
def build_js(ctx):
    """Compile Python source files to JavaScript (pytigon.js)."""
    import pscript
    from pytigon_lib.schindent.py_to_js import compile, prepare_python_code
    from jsmin import jsmin

    print("Compiling Python → JavaScript...")

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
        "pytigon_inline.py",
        "pytigon.py",
    ]

    with chdir(JS_SRC):
        with open("py_runtime.js", "wt") as fout:
            fout.write(pscript.get_full_std_lib(indent=0))

        with open("py_runtime.min.js", "wt") as fout:
            fout.write(jsmin(pscript.get_full_std_lib(indent=0)))

        with open("pytigon.js", "wt") as fout:
            for file in files:
                with open(file, "rt") as fin:
                    error, js = compile(prepare_python_code(fin.read()))
                    if error:
                        print(f"  ERROR in {file}: {js}")
                    else:
                        fout.write(js)
                        fout.write("\n\n")

        _remove_duplicate_exports(Path("pytigon.js"))

        with open("pytigon.js", "rt") as fin:
            with open("pytigon.min.js", "wt") as fout:
                fout.write(jsmin(fin.read()))

    compiled = ["pytigon.js", "py_runtime.js", "pytigon.min.js", "py_runtime.min.js"]
    dst_dir = STATIC / "pytigon_js"
    dst_dir.mkdir(parents=True, exist_ok=True)
    for name in compiled:
        src = JS_SRC / name
        dst = dst_dir / name
        copyfile(src, dst)
        print(f"  {src.relative_to(ROOT)} => {dst.relative_to(ROOT)}")

    print("JS build complete.")


@task
def build_css(ctx):
    """Compile SASS files to CSS."""
    import sass

    print("Compiling SASS → CSS...")

    for pos in sorted(THEMES_SRC.glob("**/*.sass")):
        if pos.stem.startswith("_"):
            continue
        input_path = pos
        output_path = Path(str(input_path).replace("static_src", "static")).with_suffix(
            ".css"
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        css = sass.compile(
            string=input_path.read_text(),
            indented=True,
            include_paths=(str(pos.parent),),
        )
        output_path.write_text(css)
        rel_in = input_path.relative_to(ROOT)
        rel_out = output_path.relative_to(ROOT)
        print(f"  {rel_in} => {rel_out}")

    print("CSS build complete.")


@task
def build_templates(ctx):
    """Compile .ihtml templates to .html for all projects."""
    print("Compiling templates...")
    prj_dir = ROOT / "pytigon" / "prj"
    if not prj_dir.exists():
        print("  No prj/ directory found.")
        return

    for project in sorted(prj_dir.iterdir()):
        if project.is_dir() and not project.name.startswith("."):
            cmd = f"ptig --dev manage_{project.name} compiletemplates"
            print(f"  {project.name}: {cmd}")
            ctx.run(cmd, warn=True)
    print("Template compilation complete.")


@task
def clean(ctx):
    """Remove build artifacts."""
    patterns = [
        "pytigon/static/pytigon_js/pytigon.js",
        "pytigon/static/pytigon_js/pytigon.min.js",
        "pytigon/static/pytigon_js/py_runtime.js",
        "pytigon/static/pytigon_js/py_runtime.min.js",
        "pytigon/static_src/pytigon_js/pytigon.js",
        "pytigon/static_src/pytigon_js/pytigon.min.js",
        "pytigon/static_src/pytigon_js/py_runtime.js",
        "pytigon/static_src/pytigon_js/py_runtime.min.js",
    ]
    for pat in patterns:
        for f in ROOT.glob(pat):
            f.unlink()
            print(f"  removed {f.relative_to(ROOT)}")

    # Remove compiled CSS
    for css in (STATIC / "themes").glob("**/*.css"):
        css.unlink()
        print(f"  removed {css.relative_to(ROOT)}")

    print("Clean complete.")


@task
def lint(ctx):
    """Run ruff linter."""
    ctx.run("ruff check pytigon tests", echo=True)


@task
def format_(ctx):
    """Run ruff formatter."""
    ctx.run("ruff format pytigon tests", echo=True)


@task
def test(ctx, path="tests"):
    """Run pytest."""
    ctx.run(f"pytest {path} -v", echo=True)


@task
def typecheck(ctx):
    """Run mypy type checker."""
    ctx.run("mypy pytigon --ignore-missing-imports", warn=True, echo=True)


def _remove_duplicate_exports(filepath):
    """Remove duplicate consecutive export lines from a file."""
    lines = filepath.read_text(encoding="utf-8").splitlines(keepends=True)
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("export") and i + 1 < len(lines) and lines[i + 1] == line:
            result.append(line)
            i += 2
            continue
        result.append(line)
        i += 1

    filepath.write_text("".join(result), encoding="utf-8")
    removed = len(lines) - len(result)
    if removed:
        print(f"  Removed {removed} duplicate export(s) from {filepath.name}")
