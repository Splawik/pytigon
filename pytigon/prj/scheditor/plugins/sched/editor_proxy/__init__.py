import wx
import types
from base64 import b32encode, b32decode
from schcli.guilib.image import bitmap_from_href


def init_plugin(
    app,
    mainframe,
    desktop,
    mgr,
    menubar,
    toolbar,
    accel,
):
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

    def xmlrpc_edit(self, path):
        x = path.replace("\\", "/").split("/")
        name = x[-1]
        okno = self.GetTopWindow().new_main_page("^standard/editor/editor.html", name)
        p = "/schcommander/table/FileManager/open/%s/" % b32encode(
            path.encode("utf-8")
        ).decode("utf-8")
        p_save = p.replace("/open/", "/save/")
        p_save_as = "schcommander/table/FileManager/save/{{file}}/"
        this = self

        def _init():
            ed = okno.body.EDITOR
            ed.load_from_url(p, "py")
            ed.set_save_path(p_save, p_save_as)
            ed.GotoPos(0)
            this.GetTopWindow().Raise()

        wx.CallAfter(_init)
        return "OK"

    app.xmlrpc_edit = types.MethodType(xmlrpc_edit, app)

    def xmlrpc_test(self):
        return "OK"

    app.xmlrpc_test = types.MethodType(xmlrpc_test, app)

    def on_edit3(self):
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    mainframe.on_edit = types.MethodType(on_edit3, mainframe)

    idn = mainframe._append_command("python", "self.on_edit3()")
    bitmap = bitmap_from_href("client://emblems/emblem-favorite.png")

    page = toolbar.create_page("page2")
    panel = page.create_panel("special")
    panel.append(idn, "test", bitmap)
    toolbar.create()
