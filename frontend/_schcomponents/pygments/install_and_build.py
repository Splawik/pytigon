from pytigon.pytigon_run import run
from pytigon_lib.schfs.sync import rsync_style_sync


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
            "pygments-css",
        ]
    )
    rsync_style_sync(
        "./node_modules/pygments-css/",
        "../../../pytigon/static/vanillajs_plugins/pygments/",
    )
