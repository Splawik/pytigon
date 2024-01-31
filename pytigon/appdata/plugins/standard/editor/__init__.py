#!/usr/bin/python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General PubliLicense
# for more details.

# Pytigon - wxpython and django application framework

# author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
# copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
# license: "LGPL 3.0"
# version: "0.1a"


import os.path

import wx

from pytigon_lib.schtools.tools import bencode, bdecode


def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    from .editor import CodeEditor
    from pytigon_gui.guictrl.ctrl import SchBaseCtrl
    import pytigon_gui.guictrl.ctrl

    class Styledtext(CodeEditor, SchBaseCtrl):
        def __init__(self, parent, **kwds):
            self.href = None

            SchBaseCtrl.__init__(self, parent, kwds)
            kwds["style"] = wx.TE_PROCESS_ENTER

            CodeEditor.__init__(self, parent, **kwds)
            if self.src:
                self.set_ext(self.src)
            self.last_clipboard_state = False

            self.GetParent().bind_to_ctrl(
                self, wx.ID_COPY, self._on_copy, self.on_can_copy
            )
            self.GetParent().bind_to_ctrl(
                self, wx.ID_CUT, self._on_cut, self.on_can_cut
            )
            self.GetParent().bind_to_ctrl(
                self, wx.ID_PASTE, self._on_paste, self.on_can_paste
            )

            a_table = [
                (0, wx.WXK_F2, self.on_save),
                (wx.ACCEL_CTRL, ord("S"), self.on_save),
            ]
            self.set_acc_key_tab(a_table)

            if "data" in self.param:
                self.SetValue(self.param["data"])

            self.href_save = None

            self.Bind(wx.EVT_UPDATE_UI, self.on_check_can_save, id=wx.ID_SAVE)
            self.Bind(wx.EVT_MENU, self.on_save2, id=wx.ID_SAVE)

            self.Bind(wx.EVT_UPDATE_UI, self.on_check_can_save_as, id=wx.ID_SAVEAS)
            self.Bind(wx.EVT_MENU, self.on_save_as, id=wx.ID_SAVEAS)

        def on_check_can_save(self, event):
            modified = self.GetModify()
            event.Enable(modified)

        def on_save2(self, event):
            self.save()
            self.SetSavePoint()

        def on_check_can_save_as(self, event):
            event.Enable(True if self.href_save else False)

        def on_save_as(self, event):
            dlg = wx.TextEntryDialog(self, "Enter new file name", "Rename file", "")

            if dlg.ShowModal() == wx.ID_OK:
                value = dlg.GetValue()
                if value:
                    x = self.href.split("/")
                    try:
                        encoded_file_path = x[-1]
                        if not encoded_file_path:
                            encoded_file_path = x[-2]
                    except:
                        encoded_file_path = self.href
                    file_path = bdecode(encoded_file_path)

                    xx = file_path.replace("\\", "/").rsplit("/", 1)

                    new_file_path = os.path.join(
                        file_path[: len(xx[0]) + 1], dlg.GetValue()
                    )
                    encoded_new_file_path = bencode(new_file_path)

                    self.href = self.href_save.replace(
                        "{{file}}", encoded_new_file_path
                    )

                    self.save()
                    self.SetSavePoint()

                    self.get_parent_form().get_tab().change_notebook_page_title(
                        dlg.GetValue()
                    )

        def on_key_down_base(self, event):
            if event.GetKeyCode() == wx.WXK_TAB:
                event.Skip()
            else:
                return SchBaseCtrl.on_key_down_base(self, event)

        def set_save_path(self, href, href_save=None):
            self.href = href
            self.href_save = href_save

        def set_view_path(self, href):
            self.href_view = href

        def SetValue(self, value):
            self.AddText(self.preprocess(value))

        def GetValue(self):
            return self.GetText()

        def load_from_url(self, url, ext):
            self.set_ext(ext)
            http = wx.GetApp().http
            response = http.get(self, url)
            txt = response.str()
            self.AddText(txt)
            self.url = url

        def on_save(self, event):
            self.save()
            self.SetSavePoint()

        def save(self):
            http = wx.GetApp().get_http(self)
            if self.href:
                # http.post(self, self.href, {'data': self.GetText().encode('utf-8')})
                v = self.GetTextRaw()
                if type(v) == str:
                    http.post(self, self.href, {"data": self.GetText().encode("utf-8")})
                else:
                    http.post(self, self.href, {"data": self.GetTextRaw()})

        def can_copy(self):
            if self.GetSelectionEnd() - self.GetSelectionStart() != 0:
                return True
            else:
                return False

        def can_cut(self):
            return self.can_copy()

        def can_paste(self):
            if self.last_clipboard_state or CodeEditor.CanPaste(self):
                self.last_clipboard_state = True
                return True
            else:
                return False

        def _on_copy(self, event):
            self.Copy()

        def _on_cut(self, event):
            self.Cut()

        def _on_paste(self, event):
            self.Paste()

        def on_can_copy(self, event):
            event.Enable(self.can_copy())

        def on_can_cut(self, event):
            event.Enable(self.can_cut())

        def on_can_paste(self, event):
            event.Enable(self.can_paste())

    pytigon_gui.guictrl.ctrl.STYLEDTEXT = Styledtext
