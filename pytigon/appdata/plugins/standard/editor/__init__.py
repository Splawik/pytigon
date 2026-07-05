"""Styled text editor plugin for Pytigon.

Provides the STYLEDTEXT control - a code editor with syntax highlighting,
clipboard operations, save/load, and file rename via "Save As" functionality.
"""

import os.path

import wx

from pytigon_lib.schtools.tools import bdecode, bencode


def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    """Initialize the styled text editor plugin.

    Registers the STYLEDTEXT control type that combines the CodeEditor
    widget with SchBaseCtrl for integration with the Pytigon framework.

    Args:
        app: Application instance.
        mainframe: Main window frame.
        desktop: Desktop manager.
        mgr: Plugin manager.
        menubar: Menu bar.
        toolbar: Tool bar.
        accel: Accelerator table.
    """
    import pytigon_gui.guictrl.ctrl
    from pytigon_gui.guictrl.ctrl import SchBaseCtrl

    from .editor import CodeEditor

    class Styledtext(CodeEditor, SchBaseCtrl):
        """Styled text editor control with syntax highlighting and save support."""

        def __init__(self, parent, **kwds):
            """Initialize the styled text control.

            Args:
                parent: Parent window.
                **kwds: Configuration keywords.
            """
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
            """Enable Save menu item only when content is modified."""
            event.Enable(self.GetModify())

        def on_save2(self, event):
            """Handle Save menu/toolbar action."""
            self.save()
            self.SetSavePoint()

        def on_check_can_save_as(self, event):
            """Enable Save As only when a save path is available."""
            event.Enable(bool(self.href_save))

        def on_save_as(self, event):
            """Handle Save As - rename and save the file to a new path."""
            dlg = wx.TextEntryDialog(self, "Enter new file name", "Rename file", "")

            if dlg.ShowModal() == wx.ID_OK:
                value = dlg.GetValue()
                if value:
                    x = self.href.split("/")
                    try:
                        encoded_file_path = x[-1]
                        if not encoded_file_path:
                            encoded_file_path = x[-2]
                    except IndexError:
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
            """Handle base key down - pass TAB through, delegate others.

            Args:
                event: Key event.

            Returns:
                Result from SchBaseCtrl.on_key_down_base for non-TAB keys.
            """
            if event.GetKeyCode() == wx.WXK_TAB:
                event.Skip()
            else:
                return SchBaseCtrl.on_key_down_base(self, event)

        def set_save_path(self, href, href_save=None):
            """Set the save path for the editor content.

            Args:
                href: Primary URL path for saving.
                href_save: Optional template URL for Save As operations.
            """
            self.href = href
            self.href_save = href_save

        def set_view_path(self, href):
            """Set the view path for the editor.

            Args:
                href: URL path for viewing.
            """
            self.href_view = href

        def SetValue(self, value):
            """Set editor content, preprocessing tabs to spaces.

            Args:
                value: Text content to set.
            """
            self.AddText(self.preprocess(value))

        def GetValue(self):
            """Get the current editor text content.

            Returns:
                Current text content as string.
            """
            return self.GetText()

        def load_from_url(self, url, ext):
            """Load editor content from a URL.

            Args:
                url: URL to fetch content from.
                ext: File extension for syntax highlighting.
            """
            self.set_ext(ext)
            http = wx.GetApp().http
            response = http.get(self, url)
            txt = response.str()
            self.AddText(txt)
            self.url = url

        def on_save(self, event):
            """Handle save accelerator (F2 or Ctrl+S)."""
            self.save()
            self.SetSavePoint()

        def save(self):
            """Save editor content to the server.

            Handles both string and bytes content types.
            """
            http = wx.GetApp().get_http(self)
            if self.href:
                v = self.GetTextRaw()
                if isinstance(v, str):
                    http.post(
                        self,
                        self.href,
                        {"data": self.GetText().encode("utf-8")},
                    )
                else:
                    http.post(self, self.href, {"data": self.GetTextRaw()})

        def can_copy(self):
            """Check if there is a selection to copy.

            Returns:
                True if text is selected.
            """
            return self.GetSelectionEnd() - self.GetSelectionStart() != 0

        def can_cut(self):
            """Check if there is a selection to cut.

            Returns:
                True if text is selected (same as can_copy).
            """
            return self.can_copy()

        def can_paste(self):
            """Check if clipboard has content to paste.

            Returns:
                True if paste is available.
            """
            if self.last_clipboard_state or CodeEditor.CanPaste(self):
                self.last_clipboard_state = True
                return True
            return False

        def _on_copy(self, event):
            """Execute copy operation."""
            self.Copy()

        def _on_cut(self, event):
            """Execute cut operation."""
            self.Cut()

        def _on_paste(self, event):
            """Execute paste operation."""
            self.Paste()

        def on_can_copy(self, event):
            """Update copy menu item enabled state."""
            event.Enable(self.can_copy())

        def on_can_cut(self, event):
            """Update cut menu item enabled state."""
            event.Enable(self.can_cut())

        def on_can_paste(self, event):
            """Update paste menu item enabled state."""
            event.Enable(self.can_paste())

    pytigon_gui.guictrl.ctrl.STYLEDTEXT = Styledtext
