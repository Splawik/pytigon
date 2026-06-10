import subprocess
import sys
from pytigon_lib.schfs.sync import rsync_style_sync
from pytigon.pytigon_run import run

SETUP_TRIGGERS = {
    "jquery": """
import { jQuery } from 'jquery';

globalThis.jQuery = jQuery;
globalThis.$ = jQuery;

jQuery.isFunction = function(obj) {
    return typeof obj === 'function';
}
jQuery.isArray = Array.isArray;
""",
    "sprintf": """
import { vsprintf, sprintf } from 'sprintf'
globalThis.vsprintf = vsprintf
globalThis.sprintf = sprintf
""",
    "sweetalert2": """import Swal from 'sweetalert2'
globalThis.Swal = Swal
""",
}

IMPORT_MODLUES = [
    "om-perfect-scrollbar:PerfectScrollbar",
    "moment",
    "ladda:Ladda",
    "bootstrap",
    "js-cookie:Cookies",
    "idiomorph:Idiomorph",
    # "imask:IMask",
]

IMPORT_ELEMENTS = {
    "om-perfect-scrollbar": "PerfectScrollbar",
    "idiomorph": "Idiomorph",
    "jsi18n": "gettext",
    "jquery": "jQuery",
}

NO_JS_MODULES = ["bootstrap-icons", "select2-bootstrap-5-theme"]

with open("requirements_js.txt", "rt") as f:
    requirements = f.read().splitlines()

buf = ""
shims = ""

for requirement in requirements:
    if requirement.startswith("#") or not requirement.strip():
        continue
    name = requirement.replace("-", "_").replace(".", "_").replace("@", "").replace("/", "_")
    test = True
    if ".css" in requirement:
        test = False
        buf += f"import '{requirement}';\n"
    elif requirement not in NO_JS_MODULES and requirement not in IMPORT_ELEMENTS:
        buf += f"import * as {name} from '{requirement}';\n"
    else:
        test = False

    if requirement in SETUP_TRIGGERS:
        shims += SETUP_TRIGGERS[requirement] + "\n"
        test = False
    elif requirement in IMPORT_ELEMENTS:
        buf += f"import {{ {IMPORT_ELEMENTS[requirement]} }} from '{requirement}';\n"
        buf += f"window.{IMPORT_ELEMENTS[requirement]} = {IMPORT_ELEMENTS[requirement]};\n"
        test = False
    else:
        for element in IMPORT_MODLUES:
            if requirement == element or element.startswith(requirement):
                element_name = element.split(":")[1] if ":" in element else element
                shims += f"import * as {element_name} from '{requirement}';\n"
                shims += f"globalThis.{element_name} = {element_name};\n"
                test = False
                break
    if test:
        buf += f"window.{name} = {name};\n"
        # buf += f"export * as {name} from '{requirement}';\n"
with open("tmp.js", "wt") as f:
    f.write(buf)

with open("shims.js", "wt") as f:
    f.write(shims)


def run_esbuild(entry_point, outfile):
    """Uruchamia esbuild jako proces zewnętrzny."""
    try:
        ret = run(
            [
                "ptig",
                "@esbuild",
                entry_point,
                f"--outfile={outfile}",
                "--bundle",
                # "--minify",
                "--loader:.ttf=dataurl",
                "--loader:.png=dataurl",
                "--loader:.gif=dataurl",
                "--log-limit=0",
                "--inject:./shims.js",
            ]
        )
        print(ret)
        print(f"✅ Sukces: {outfile}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Błąd budowania: {e}", file=sys.stderr)
        sys.exit(1)


def sync_static_files():
    """Synchronizuje pliki statyczne do katalogu docelowego."""
    with open("static_files.txt", "rt") as f:
        static_files = f.read().splitlines()
    for static_file in static_files:
        if static_file.startswith("#") or not static_file.strip():
            continue
        if ":" not in static_file:
            continue
        src, dst = static_file.split(":")
        rsync_style_sync(src, f"../pytigon/static/{dst}")


if __name__ == "__main__":
    run_esbuild("tmp.js", "../pytigon/static/pytigon-lib.js")
    sync_static_files()
