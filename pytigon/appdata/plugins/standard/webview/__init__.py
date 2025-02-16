import wx
from .basebrowser import BaseWebBrowser


def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    import pytigon_gui.guictrl.ctrl
    from base64 import b64encode

    def Component(parent, **kwds):
        http = wx.GetApp().get_http(parent)
        response = http.get(
            parent, "/schsys/widget_web?browser_type=1", user_agent="webviewembeded"
        )
        buf = response.str()
        url = "data:text/html;base64," + b64encode(buf.encode("utf-8")).decode("utf-8")
        obj = pytigon_gui.guictrl.ctrl.HTML2(parent, **kwds)
        obj.load_url(url)
        return obj

    pytigon_gui.guictrl.ctrl.COMPONENT = Component

    from .wxwebview import init_plugin_web_view

    return init_plugin_web_view(
        app,
        mainframe,
        desktop,
        mgr,
        menubar,
        toolbar,
        accel,
        BaseWebBrowser,
    )

    #    from .cef import init_plugin_cef
    #    return init_plugin_cef(
    #        app, mainframe, desktop, mgr, menubar, toolbar, accel, BaseWebBrowser
    #    )
