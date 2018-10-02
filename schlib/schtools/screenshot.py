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

#Pytigon - wxpython and django application framework

#author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
#license: "LGPL 3.0"
#version: "0.1a"

""""based on cefpython example: screenshot.py"""

_IMPORTED = False 

def get_screenshot(url,  size, img_path):
    global _IMPORTED
    if not _IMPORTED:
        from cefpython3 import cefpython as cef
        import os
        import platform
        import subprocess
        import sys
        from PIL import Image, PILLOW_VERSION
        
    
    def create_browser(url):
        parent_window_handle = 0
        window_info = cef.WindowInfo()
        window_info.SetAsOffscreen(parent_window_handle)
        browser = cef.CreateBrowserSync(window_info=window_info, url=url)
        browser.SetClientHandler(LoadHandler())
        browser.SetClientHandler(RenderHandler())
        browser.SendFocusEvent(True)
        browser.WasResized()


    def save_screenshot(browser, path):
        nonlocal size
        buffer_string = browser.GetUserData("OnPaint.buffer_string")
        if not buffer_string:
            raise Exception("buffer_string is empty, OnPaint never called?")
        image = Image.frombytes("RGBA", (size[2], size[3]), buffer_string, "raw", "RGBA", 0, 1)
        image.save(path, "PNG")


    def exit_app(browser):
        browser.CloseBrowser()
        cef.QuitMessageLoop()


    class LoadHandler(object):
        def OnLoadingStateChange(self, browser, is_loading, **_):
            nonlocal img_path
            if not is_loading:
                save_screenshot(browser, img_path)
                cef.PostTask(cef.TID_UI, exit_app, browser)

        def OnLoadError(self, browser, frame, error_code, failed_url, **_):
            if not frame.IsMain():
                return
            cef.PostTask(cef.TID_UI, exit_app, browser)


    class RenderHandler(object):
        def __init__(self):
            self.OnPaint_called = False

        def GetViewRect(self, rect_out, **_):            
            nonlocal size
            rect_out.extend((size[0], size[1], size[2], size[3]))
            return True

        def OnPaint(self, browser, element_type, paint_buffer, **_):
            if not self.OnPaint_called:
                self.OnPaint_called = True
            if element_type == cef.PET_VIEW:
                buffer_string = paint_buffer.GetBytes(mode="rgba", origin="top-left")
                browser.SetUserData("OnPaint.buffer_string", buffer_string)
            else:
                raise Exception("Unsupported element_type in OnPaint")

    sys.excepthook = cef.ExceptHook  
    cef.Initialize(settings={"windowless_rendering_enabled": True})
    create_browser(url)
    cef.MessageLoop()
    cef.Shutdown()


if __name__ == '__main__':
    get_screenshot("https://github.com/cztomczak/cefpython",  (0,0,800,600), "test.png")
