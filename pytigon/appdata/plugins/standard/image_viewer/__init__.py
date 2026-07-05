"""Image viewer plugin for Pytigon.

Provides the IMAGEVIEWER control - a scrollable image viewer
supporting PNG, JPEG, and SVG formats with auto-resize to fit.
"""

from io import BytesIO

import wx
from PIL import Image

from pytigon_gui.guictrl.basectrl import SchBaseCtrl
from pytigon_gui.guilib.image import pil_to_image
from pytigon_lib.schtools.images import svg_to_png


def init_plugin(
    app,
    mainframe,
    desktop,
    mgr,
    menubar,
    toolbar,
    accel,
):
    """Register the Imageviewer control in the global control registry.

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

    class Imageviewer(wx.ScrolledWindow, SchBaseCtrl):
        """Scrollable image viewer with auto-resize support.

        Displays image files (PNG, JPEG, SVG) and automatically
        resizes them to fit the window when they exceed the viewport.
        """

        def __init__(self, parent, **kwds):
            """Initialize the image viewer.

            Args:
                parent: Parent window.
                **kwds: Configuration keywords.
            """
            SchBaseCtrl.__init__(self, parent, kwds)
            wx.ScrolledWindow.__init__(self, parent, **kwds)
            self.static_bitmap = wx.StaticBitmap(self)
            if self.src:
                self.set_ext(self.src)
            self.last_clipboard_state = False
            mainframe.bind_to_toolbar(self.on_copy, id=wx.ID_COPY)
            mainframe.bind_to_toolbar(self.on_cut, id=wx.ID_CUT)
            mainframe.bind_to_toolbar(self.on_paste, id=wx.ID_PASTE)
            a_table = [
                (0, wx.WXK_F2, self.on_save),
                (wx.ACCEL_CTRL, ord("S"), self.on_save),
            ]
            self.set_acc_key_tab(a_table)
            self.resize_to_win = True
            self.Bind(wx.EVT_SIZE, self.on_size)
            self.pil = None

        def _get_resized_pil(self, max_size):
            """Get a PIL image resized to fit within max_size if needed.

            Args:
                max_size: Tuple of (max_width, max_height).

            Returns:
                Tuple of (PIL.Image, was_resized_bool).
            """
            if not self.resize_to_win:
                return self.pil, False
            if self.pil.size[0] <= max_size[0] and self.pil.size[1] <= max_size[1]:
                return self.pil, False
            delta1 = self.pil.size[0] / float(max_size[0])
            delta2 = self.pil.size[1] / float(max_size[1])
            delta = max(delta1, delta2)
            new_size = (
                int(self.pil.size[0] / delta),
                int(self.pil.size[1] / delta),
            )
            return self.pil.resize(new_size, Image.BICUBIC), True

        def _update_display(self, pil_image, was_resized):
            """Update the bitmap display and scroll settings.

            Args:
                pil_image: PIL Image to display.
                was_resized: Whether the image was resized.
            """
            img = pil_to_image(pil_image)
            self.static_bitmap.SetBitmap(img.ConvertToBitmap())
            if not was_resized:
                self.SetVirtualSize(wx.Size(img.GetWidth(), img.GetHeight()))
                self.SetScrollRate(20, 20)

        def on_size(self, event):
            """Handle window resize - re-render image at new size.

            Args:
                event: Size event.
            """
            if self.pil:
                size = self.GetParent().GetSize()
                pil2, resized = self._get_resized_pil(size)
                self._update_display(pil2, resized)
            event.Skip()

        def set_ext(self, ext):
            """Set the file extension for the viewer.

            Args:
                ext: File extension string.
            """
            self.ext = ext

        def goto_pos(self, pos):
            """Go to a specific position (no-op for images).

            Args:
                pos: Position value (unused).
            """
            pass

        def set_save_path(self, href):
            """Set the save path for the image.

            Args:
                href: URL path for saving.
            """
            self.href = href

        def SetValue(self, value):
            """Set the viewer content (no-op, use load_from_url instead).

            Args:
                value: Content to set (unused for image viewer).
            """
            pass

        def load_from_url(self, url, ext):
            """Load and display an image from a URL.

            Args:
                url: URL to fetch the image from.
                ext: File extension ('svg' for SVG, otherwise raster).
            """
            self.set_ext(ext)
            http = wx.GetApp().http
            response = http.get(self, url)
            data = response.ptr()

            if ext == "svg":
                size = self.GetParent().GetSize()
                img_data = svg_to_png(data, size[0], size[1], "simple_min")
                io = BytesIO(img_data)
            else:
                io = BytesIO(data)

            self.pil = Image.open(io)
            size = self.GetParent().GetSize()
            pil2, resized = self._get_resized_pil(size)
            self._update_display(pil2, resized)
            self.url = url

        def on_save(self, event):
            """Handle save event - post image data to server.

            Args:
                event: Save event.
            """
            http = wx.GetApp().get_http(self)
            if self.href:
                http.post(self, self.href, {"data": self.GetText()})

        def on_copy(self, event):
            """Handle copy event."""
            self.Copy()

        def on_cut(self, event):
            """Handle cut event."""
            self.Cut()

        def on_paste(self, event):
            """Handle paste event."""
            self.Paste()

    pytigon_gui.guictrl.ctrl.IMAGEVIEWER = Imageviewer
