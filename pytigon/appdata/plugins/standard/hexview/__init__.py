"""Hex viewer plugin for Pytigon.

Provides the HEXVIEWER control - a hexadecimal file viewer
based on the styled text editor.
"""

import wx
import string
import binascii


def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    """Register the Hexviewer control in the global control registry.

    Args:
        app: Application instance.
        mainframe: Main window frame.
        desktop: Desktop manager.
        mgr: Plugin manager.
        menubar: Menu bar.
        toolbar: Tool bar.
        accel: Accelerator table.
    """
    import pytigon_gui
    import pytigon_gui.guictrl.ctrl

    class Hexviewer(pytigon_gui.guictrl.ctrl.STYLEDTEXT):
        """Hexadecimal file viewer based on the styled text control.

        Displays binary file contents as hexadecimal bytes alongside
        an ASCII representation.
        """

        def __init__(self, *args, **kwds):
            """Initialize the hex viewer.

            Args:
                *args: Positional arguments.
                **kwds: Keyword arguments.
            """
            pytigon_gui.guictrl.ctrl.STYLEDTEXT.__init__(self, *args, **kwds)
            if self.src:
                self.SetExt(self.src)
            self.last_clipboard_state = False

        def set_save_path(self, href):
            """Set the save path for the hex viewer.

            Args:
                href: URL path for saving.
            """
            self.href = href

        def SetValue(self, value):
            """Append text to the viewer.

            Args:
                value: Text content to append.
            """
            self.AddText(value)

        def GetValue(self):
            """Get the current text content.

            Returns:
                Full text content of the viewer.
            """
            return self.GetText()

        def print_hex(self, hex_str):
            """Render hexadecimal data with ASCII preview.

            Displays each 16-byte chunk as hex pairs on the left
            and a printable ASCII representation on the right.

            Args:
                hex_str: Hexadecimal string to display.
            """
            _REPLACEMENTS = str.maketrans(
                "\n\r\t'\"",
                "......",
            )
            num_buf = len(hex_str) // 32
            for i in range(num_buf):
                h = hex_str[i * 32 : (i + 1) * 32]
                hh = " ".join(a + b for a, b in zip(h[::2], h[1::2]))
                b = binascii.unhexlify(h)
                p = b.decode("utf-8", "replace").translate(_REPLACEMENTS)
                pp = "".join(x if x in string.printable else "." for x in p)
                self.AddText(hh + " | " + pp + "\n")

        def load_from_url(self, url, ext):
            """Load and display hex content from a URL.

            Args:
                url: URL to fetch content from.
                ext: File extension (ignored, always displays as hex).
            """
            self.set_ext("txt")
            http = wx.GetApp().http
            response = http.get(self, url + "0/")
            txt = response.str()
            self.print_hex(txt)
            self.url = url

        def on_save(self, event):
            """Handle save event (no-op for hex viewer)."""
            pass

    pytigon_gui.guictrl.ctrl.HEXVIEWER = Hexviewer
