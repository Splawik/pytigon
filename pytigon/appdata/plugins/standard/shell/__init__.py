def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    import wx.py as py
    import wx
    from pytigon_gui.guictrl.ctrl import SchBaseCtrl
    import pytigon_gui.guictrl.ctrl

    class Shell(py.shell.Shell, SchBaseCtrl):
        def __init__(self, parent, **kwds):
            SchBaseCtrl.__init__(self, parent, kwds)
            if 'name' in kwds:
                del kwds['name']
            kwds['locals'] = {'self': self, 'app': wx.GetApp(),'topwin': wx.GetApp().GetTopWindow(), 'wx': wx }
            py.shell.Shell.__init__(self, parent, **kwds)


    class CrustShell(py.crust.Crust, SchBaseCtrl):
        def __init__(self, parent, **kwds):
            SchBaseCtrl.__init__(self, parent, kwds)
            if 'name' in kwds:
                del kwds['name']
            kwds['locals'] = {'self': self, 'app': wx.GetApp(),'topwin': wx.GetApp().GetTopWindow(), 'wx': wx }
            py.crust.Crust.__init__(self, parent, **kwds)


    class SliceShell(py.sliceshell.SlicesShell, SchBaseCtrl):
        def __init__(self, parent, **kwds):
            SchBaseCtrl.__init__(self, parent, kwds)
            if 'name' in kwds:
                del kwds['name']
            kwds['locals'] = {'self': self, 'app': wx.GetApp(),'topwin': wx.GetApp().GetTopWindow(), 'wx': wx }
            kwds['showPySlicesTutorial'] = False
            py.sliceshell.SlicesShell.__init__(self, parent, **kwds)

    pytigon_gui.guictrl.ctrl.SHELL = Shell
    pytigon_gui.guictrl.ctrl.CRUST_SHELL = CrustShell
    pytigon_gui.guictrl.ctrl.SLICE_SHELL = SliceShell


