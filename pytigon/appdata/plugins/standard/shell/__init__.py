"""Python shell plugin for Pytigon.

Provides interactive Python shells: standard Shell, Crust (with
namespace viewer), and SlicesShell (with tutorial) - all integrated
with SchBaseCtrl for the Pytigon framework.
"""


def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    """Register Python shell controls in the global control registry.

    Provides three shell types:
    - SHELL: Basic Python interactive shell
    - CRUST_SHELL: Crust shell with namespace viewer
    - SLICE_SHELL: SlicesShell with tutorial support

    Args:
        app: Application instance.
        mainframe: Main window frame.
        desktop: Desktop manager.
        mgr: Plugin manager.
        menubar: Menu bar.
        toolbar: Tool bar.
        accel: Accelerator table.
    """
    import wx
    import wx.py as py

    import pytigon_gui.guictrl.ctrl
    from pytigon_gui.guictrl.ctrl import SchBaseCtrl

    _DEFAULT_LOCALS = {
        "app": wx.GetApp(),
        "topwin": wx.GetApp().GetTopWindow(),
        "wx": wx,
    }

    class Shell(py.shell.Shell, SchBaseCtrl):
        """Basic Python interactive shell."""

        def __init__(self, parent, **kwds):
            SchBaseCtrl.__init__(self, parent, kwds)
            kwds.pop("name", None)
            kwds["locals"] = dict(_DEFAULT_LOCALS, self=self)
            py.shell.Shell.__init__(self, parent, **kwds)

    class CrustShell(py.crust.Crust, SchBaseCtrl):
        """Crust shell with namespace viewer and calltip support."""

        def __init__(self, parent, **kwds):
            SchBaseCtrl.__init__(self, parent, kwds)
            kwds.pop("name", None)
            kwds["locals"] = dict(_DEFAULT_LOCALS, self=self)
            py.crust.Crust.__init__(self, parent, **kwds)

    class SliceShell(py.sliceshell.SlicesShell, SchBaseCtrl):
        """SlicesShell with tutorial and slice management."""

        def __init__(self, parent, **kwds):
            SchBaseCtrl.__init__(self, parent, kwds)
            kwds.pop("name", None)
            kwds["locals"] = dict(_DEFAULT_LOCALS, self=self)
            kwds.setdefault("showPySlicesTutorial", False)
            py.sliceshell.SlicesShell.__init__(self, parent, **kwds)

    pytigon_gui.guictrl.ctrl.SHELL = Shell
    pytigon_gui.guictrl.ctrl.CRUST_SHELL = CrustShell
    pytigon_gui.guictrl.ctrl.SLICE_SHELL = SliceShell
