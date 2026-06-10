import subprocess
from pytigon.pytigon_run import run
import sys


def run_esbuild(entry_point, outfile):
    try:
        ret = run(
            [
                "ptig",
                "@esbuild",
                entry_point,
                f"--outfile={outfile}",
                "--bundle",
                "--format=esm",
                "--minify",
                "--loader:.ttf=dataurl",
                "--loader:.png=dataurl",
                "--loader:.gif=dataurl",
                "--log-limit=0",
            ]
        )
        print(ret)
        print(f"✅ Sukces: {outfile}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Błąd budowania: {e}", file=sys.stderr)
        sys.exit(1)


def install_dependencies(dependencies):
    for requirement in dependencies:
        cmd = [
            "ptig",
            "@aube",
            "add",
            requirement,
            "--allow-low-downloads",
        ]
        print(cmd)
        ret = run(cmd)
        print(ret)


if __name__ == "__main__":
    install_dependencies(
        [
            "d3",
        ]
    )
    run_esbuild(
        "d3.mjs",
        "../../../pytigon/prj/_schcomponents/static/_schcomponents/d3/d3.js",
    )
