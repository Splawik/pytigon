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
    install_dependencies(["plotly.js-dist-min", "plotly.js"])
    rsync_style_sync(
        "./node_modules/plotly.js-dist-min/",
        "../../../pytigon/prj/_schcomponents/static/_schcomponents/plotly/",
    )
    rsync_style_sync(
        "./node_modules/plotly.js/dist/plotly.css",
        "../../../pytigon/prj/_schcomponents/static/_schcomponents/plotly/plotly.css",
    )
