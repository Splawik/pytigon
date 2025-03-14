def build(**argv):
    import os
    import subprocess
    from django.conf import settings
    import pytigon
    from pytigon_lib.schtools.nim_integration import install_if_not_exists

    path = argv["path"]
    base_name = os.path.split(path)[1].rsplit(".", 1)[0]
    nim_path = install_if_not_exists(settings.DATA_PATH)

    if os.name == "nt":
        os.environ["PATH"] = os.environ["PATH"] + (";%s\\bin\\" % nim_path)
        exe = "nim.exe"
        out_path = os.path.join(
            settings.DATA_PATH,
            "prg",
            settings.PRJ_NAME + "_" + base_name + ".exe",
        )
    else:
        os.environ["PATH"] = os.environ["PATH"] + (":%s/bin/" % nim_path)
        exe = "nim"
        out_path = os.path.join(
            settings.DATA_PATH,
            "prg",
            settings.PRJ_NAME + "_" + base_name,
        )

    packages = "nimja"
    if packages:
        packages_list = packages.replace(",",";").split(";")
        for package in packages_list:
            subprocess.run(
                [   
                    os.path.join(nim_path, "bin", exe.replace("nim", "nimble")),
                    "install",
                    package
                ]
            )

    subprocess.run(
        [
            os.path.join(nim_path, "bin", exe),
            "c",
            "--path:" + pytigon.__file__.replace("__init__.py", "ext_lib"),
            "--out:" + out_path,
            "--cc:clang",
            "--clang.exe=zigcc",
            "--clang.linkerexe=zigcc",
            "-d:release",
            "--gc:orc",
            "--opt:size",
            path,
        ]
    )
    return True


if __name__ == "__main__":
    build(path=__file__.replace("_build.py", ".nim"))
