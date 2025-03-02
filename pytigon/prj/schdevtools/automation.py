import sys
import wx
from pytigon.pytigon_run import run
from pytigon_gui.wxauto import autoit


def main(argv):
    if len(argv) > 0:
        s = argv[0]
        avi_name = s.split(".")[-2]
        setattr(wx, "pseudoimport", autoit)
        sys.argv = sys.argv[:1] + [
            "--video=%s.avi" % avi_name,
            "--rpc=8090",
            "schdevtools",
            "--inspection",
        ]
        run()
