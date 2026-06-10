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
    install_dependencies(["pivottable", "jquery-ui"])
    rsync_style_sync(
        "./node_modules/pivottable/dist/",
        "../../../pytigon/prj/_schcomponents/static/_schcomponents/pivottable/",
    )
    rsync_style_sync(
        "./node_modules/jquery-ui/dist/",
        "../../../pytigon/prj/_schcomponents/static/_schcomponents/jquery-ui/",
    )
