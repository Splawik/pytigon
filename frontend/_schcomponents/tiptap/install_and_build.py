import subprocess
import sys

from pytigon.pytigon_run import run


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
            "@tiptap/core",
            "@tiptap/starter-kit",
            "@tiptap/starter-kit",
            "@tiptap/extension-link",
            "@tiptap/extension-text-style",
            "@tiptap/extension-color",
            "@tiptap/extension-highlight",
            "@tiptap/extension-table",
            "@tiptap/extension-table-row",
            "@tiptap/extension-table-cell",
            "@tiptap/extension-table-header",
            "@tiptap/extension-image",
            "@tiptap/extensions",
        ]
    )
    run_esbuild(
        "tiptap.mjs",
        "../../../pytigon/prj/_schcomponents/static/_schcomponents/tiptap/tiptap.js",
    )
