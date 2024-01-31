#!/usr/bin/python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

# Pytigon - wxpython and django application framework

# author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
# copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
# license: "LGPL 3.0"
# version: "0.1a"


import os

import wx

from pytigon_lib.schhtml.wxdc import DcDc
from pytigon_lib.schfs.vfstools import convert_file


class HtmlCanvas(object):
    def __init__(self, zip_name):
        self.zip_name = zip_name
        self.scale = 1.0
        self.dc_zip = DcDc(calc_only=False, scale=self.scale)
        self.dc_zip.load(self.zip_name)
        # self.dc_zip.base_font_size = self.dc_zip.base_font_size * 0.9
        self.dc_zip.base_font_size = self.dc_zip.base_font_size
        self.page_no = 1

        self.width = self.dc_zip.width * self.scale
        self.height = self.dc_zip.height * self.scale

        self.page_count = self.dc_zip.get_page_count()
        self.state = self.dc_zip.state()

    def set_page(self, page_no):
        self.page_no = page_no

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def DoDrawing(self, dc, option, scale):
        self.scale = scale
        self.dc_zip.restore_state(self.state)
        self.dc_zip.set_scale(scale)
        dc_buf = self.dc_zip.dc
        self.dc_zip.dc = dc
        self.dc_zip.play(self.page_no - 1)
        self.dc_zip.dc = dc_buf

    def save(self, file_name):
        output_stream = open(file_name, "wb")
        convert_file(
            self.zip_name,
            output_stream,
            input_format="spdf",
            output_format="pdf",
            for_vfs_input=False,
            for_vfs_output=False,
        )
        output_stream.close()


class MyPrintout(wx.Printout):
    def __init__(self, canvas):
        wx.Printout.__init__(self)
        self.canvas = canvas

    def HasPage(self, page):
        if page <= self.canvas.page_count:
            return True
        else:
            return False

    def GetPageInfo(self):
        return (1, self.canvas.page_count, 1, self.canvas.page_count)

    def OnPrintPage(self, page):
        dc = self.GetDC()
        max_x = self.canvas.getWidth()
        max_y = self.canvas.getHeight()
        margin_x = 0
        margin_y = 0
        max_x = max_x + 2 * margin_x
        max_y = max_y + 2 * margin_y
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
    def __init__(self, parent, **argv):
        self.canvas = HtmlCanvas(parent.parameters)
        self.printData = wx.PrintData()
        self.printData.SetPaperId(wx.PAPER_A4)
        self.printData.SetPrintMode(wx.PRINT_MODE_PRINTER)
        self.printData.SetOrientation(wx.PORTRAIT)

        data = wx.PrintDialogData(self.printData)
        printout = MyPrintout(self.canvas)
        printout2 = MyPrintout(self.canvas)
        self.preview = wx.PrintPreview(printout, printout2, data)
        if "name" in argv:
            name = argv["name"]
        else:
            name = "htmlpreview"
        wx.PreviewCanvas.__init__(self, self.preview, parent, name=name)

        self.preview.SetCanvas(self)
        self.preview.SetZoom(100)

    def save(self):
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
        pdd = wx.PrintDialogData(self.printData)
        printer = wx.Printer(pdd)
        printout = MyPrintout(self.canvas)

        if not printer.Print(self, printout, True):
            wx.MessageBox(
                "There was a problem printing.\nPerhaps your current printer is not set correctly?",
                "Printing",
                wx.OK,
            )
        else:
            self.printData = wx.PrintData(printer.GetPrintDialogData().GetPrintData())
        printout.Destroy()


def get_printout(spdf_filename):
    canvas = HtmlCanvas(spdf_filename)

    # self.printData = wx.PrintData()
    # self.printData.SetPaperId(wx.PAPER_A4)
    # self.printData.SetPrintMode(wx.PRINT_MODE_PRINTER)
    # self.printData.SetOrientation(wx.PORTRAIT)
    # data = wx.PrintDialogData(self.printData)
    printout = MyPrintout(canvas)
    return printout
