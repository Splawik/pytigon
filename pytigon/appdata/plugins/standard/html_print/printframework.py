"""HTML print framework for Pytigon.

Provides HTML-to-PDF preview and printing capabilities using
the wxPython printing framework and custom SPDF-to-PDF conversion.
"""

import os

import wx

from pytigon_lib.schhtml.wxdc import DcDc
from pytigon_lib.schfs.vfstools import convert_file


class HtmlCanvas(object):
    """Canvas for rendering HTML content via SPDF format.

    Loads a pre-rendered SPDF document and provides drawing
    and PDF export functionality.
    """

    def __init__(self, zip_name):
        """Initialize the HTML canvas from an SPDF file.

        Args:
            zip_name: Path to the SPDF file.
        """
        self.zip_name = zip_name
        self.scale = 1.0
        self.dc_zip = DcDc(calc_only=False, scale=self.scale)
        self.dc_zip.load(self.zip_name)
        self.dc_zip.base_font_size = self.dc_zip.base_font_size
        self.page_no = 1

        self.width = self.dc_zip.width * self.scale
        self.height = self.dc_zip.height * self.scale

        self.page_count = self.dc_zip.get_page_count()
        self.state = self.dc_zip.state()

    def set_page(self, page_no):
        """Set the current page number for rendering.

        Args:
            page_no: Page number (1-based).
        """
        self.page_no = page_no

    def getWidth(self):
        """Get the canvas width in device units.

        Returns:
            Width value.
        """
        return self.width

    def getHeight(self):
        """Get the canvas height in device units.

        Returns:
            Height value.
        """
        return self.height

    def DoDrawing(self, dc, option, scale):
        """Render the current page onto a device context.

        Args:
            dc: wx.DC device context to draw on.
            option: Drawing option flag.
            scale: Scale factor for rendering.
        """
        self.scale = scale
        self.dc_zip.restore_state(self.state)
        self.dc_zip.set_scale(scale)
        dc_buf = self.dc_zip.dc
        self.dc_zip.dc = dc
        self.dc_zip.play(self.page_no - 1)
        self.dc_zip.dc = dc_buf

    def save(self, file_name):
        """Export the document to a PDF file.

        Args:
            file_name: Output PDF file path.
        """
        with open(file_name, "wb") as output_stream:
            convert_file(
                self.zip_name,
                output_stream,
                input_format="spdf",
                output_format="pdf",
                for_vfs_input=False,
                for_vfs_output=False,
            )


class MyPrintout(wx.Printout):
    """wxPython printout adapter for HtmlCanvas."""

    def __init__(self, canvas):
        """Initialize the printout.

        Args:
            canvas: HtmlCanvas instance to print.
        """
        wx.Printout.__init__(self)
        self.canvas = canvas

    def HasPage(self, page):
        """Check if the given page number exists.

        Args:
            page: Page number to check.

        Returns:
            True if the page exists.
        """
        return page <= self.canvas.page_count

    def GetPageInfo(self):
        """Get page range information.

        Returns:
            Tuple of (min_page, max_page, from_page, to_page).
        """
        return (1, self.canvas.page_count, 1, self.canvas.page_count)

    def OnPrintPage(self, page):
        """Render a single page for printing.

        Args:
            page: Page number to render.

        Returns:
            True on success.
        """
        dc = self.GetDC()
        max_x = self.canvas.getWidth()
        max_y = self.canvas.getHeight()
        (w, h) = dc.GetSize()
        scale_x = 1.0 * w / max_x
        scale_y = 1.0 * h / max_y
        actual_scale = min(scale_x, scale_y)
        pos_x = (w - self.canvas.getWidth() * actual_scale) / 2.0
        pos_y = (h - self.canvas.getHeight() * actual_scale) / 2.0
        dc.SetDeviceOrigin(int(pos_x), int(pos_y))
        dc.Clear()
        self.canvas.set_page(page)
        self.canvas.DoDrawing(dc, True, actual_scale)
        return True


class HtmlPreviewCanvas(wx.PreviewCanvas):
    """Print preview canvas for HTML documents."""

    def __init__(self, parent, **argv):
        """Initialize the preview canvas.

        Args:
            parent: Parent window.
            **argv: Keyword arguments including 'parameters' (SPDF file path)
                    and optional 'name'.
        """
        self.canvas = HtmlCanvas(parent.parameters)
        self.printData = wx.PrintData()
        self.printData.SetPaperId(wx.PAPER_A4)
        self.printData.SetPrintMode(wx.PRINT_MODE_PRINTER)
        self.printData.SetOrientation(wx.PORTRAIT)

        data = wx.PrintDialogData(self.printData)
        printout = MyPrintout(self.canvas)
        printout2 = MyPrintout(self.canvas)
        self.preview = wx.PrintPreview(printout, printout2, data)
        name = argv.get("name", "htmlpreview")
        wx.PreviewCanvas.__init__(self, self.preview, parent, name=name)

        self.preview.SetCanvas(self)
        self.preview.SetZoom(100)

    def save(self):
        """Save the document as PDF via a file dialog."""
        dlg = wx.FileDialog(
            self,
            message="Save file as ...",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard="Pdf document (*.pdf)|*.pdf",
            style=wx.FD_SAVE,
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.canvas.save(path)
        dlg.Destroy()

    def Print(self):
        """Print the document using the system printer dialog."""
        pdd = wx.PrintDialogData(self.printData)
        printer = wx.Printer(pdd)
        printout = MyPrintout(self.canvas)

        if not printer.Print(self, printout, True):
            wx.MessageBox(
                "There was a problem printing.\n"
                "Perhaps your current printer is not set correctly?",
                "Printing",
                wx.OK,
            )
        else:
            self.printData = wx.PrintData(printer.GetPrintDialogData().GetPrintData())
        printout.Destroy()


def get_printout(spdf_filename):
    """Create a wx.Printout from an SPDF file.

    Args:
        spdf_filename: Path to the SPDF file.

    Returns:
        MyPrintout instance ready for printing.
    """
    canvas = HtmlCanvas(spdf_filename)
    return MyPrintout(canvas)
