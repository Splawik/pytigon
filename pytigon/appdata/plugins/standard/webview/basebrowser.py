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

from tempfile import NamedTemporaryFile
from base64 import decodebytes, b64encode, b64decode
import urllib
import os

import wx

from pytigon_gui.guilib.tools import get_colour
from pytigon_gui.guilib.events import *
from pytigon_lib.schtools.tools import split2

JAVASCRIPT_CODE = "var pdf_ptr=base64toBlob(\"%s\", 'application/pdf'); PDFView.open(URL.createObjectURL(pdf_ptr), 0);"


class BaseWebBrowser(object):
    LOAD_CONNECT = 0
    LOAD_START = 1
    LOAD_FINISH_OK = 2
    LOAD_FINISH_FAILED = 3

    def __init__(self):
        self.progress = -1
        self.href = ""
        self.status = {
            "stat": -1,
            "progress": -1,
            "txt": None,
            "address": None,
        }
        aTable = [
            (wx.ACCEL_ALT, ord("J"), self.on_key_j),
            (wx.ACCEL_ALT, ord("K"), self.on_key_k),
            (wx.ACCEL_CTRL, ord("N"), self.on_key_n),
            (wx.ACCEL_CTRL, ord("L"), self.on_key_l),
        ]
        self.set_acc_key_tab(aTable)
        self.last_status_txt = ""
        self.pdf = None

        self.Bind(wx.EVT_UPDATE_UI, self.on_check_can_goback, id=ID_WEB_BACK)
        self.Bind(wx.EVT_UPDATE_UI, self.on_check_can_goforward, id=ID_WEB_FORWARD)
        self.Bind(wx.EVT_UPDATE_UI, self.on_check_can_stop, id=ID_WEB_STOP)
        self.Bind(wx.EVT_UPDATE_UI, self.on_check_can_refresh, id=ID_WEB_REFRESH)
        self.Bind(
            wx.EVT_UPDATE_UI, self.on_check_can_addbookmark, id=ID_WEB_ADDBOOKMARK
        )
        self.Bind(wx.EVT_MENU, self._on_back, id=ID_WEB_BACK)
        self.Bind(wx.EVT_MENU, self._on_forward, id=ID_WEB_FORWARD)
        self.Bind(wx.EVT_MENU, self._on_stop, id=ID_WEB_STOP)
        self.Bind(wx.EVT_MENU, self._on_refresh, id=ID_WEB_REFRESH)
        self.Bind(wx.EVT_MENU, self._on_addbookmark, id=ID_WEB_ADDBOOKMARK)

    def on_check_can_goforward(self, event):
        if self.get_parent_form().get_parent_page().is_active():
            test = self.can_go_forward()
            event.Enable(test)
        else:
            event.Skip()

    def on_check_can_goback(self, event):
        if self.get_parent_form().get_parent_page().is_active():
            test = self.can_go_back()
            event.Enable(test)
        else:
            event.Skip()

    def on_check_can_stop(self, event):
        if self.get_parent_form().get_parent_page().is_active():
            test = self.can_stop()
            event.Enable(test)
        else:
            event.Skip()

    def on_check_can_refresh(self, event):
        if self.get_parent_form().get_parent_page().is_active():
            test = self.can_refresh()
            event.Enable(test)
        else:
            event.Skip()

    def on_check_can_addbookmark(self, event):
        if self.get_parent_form().get_parent_page().is_active():
            test = self.can_addbookmark()
            event.Enable(test)
        else:
            event.Skip()

    def _on_back(self, event):
        if self.get_parent_form().get_parent_page().is_active():
            self.on_back(None)
        else:
            event.Skip()

    def _on_forward(self, event):
        if self.get_parent_form().get_parent_page().is_active():
            self.on_forward(None)
        else:
            event.Skip()

    def _on_stop(self, event):
        if self.get_parent_form().get_parent_page().is_active():
            self.on_stop(None)
        else:
            event.Skip()

    def _on_refresh(self, event):
        if self.get_parent_form().get_parent_page().is_active():
            self.on_refresh(None)
        else:
            event.Skip()

    def _on_addbookmark(self, event):
        if self.get_parent_form().get_parent_page().is_active():
            self.on_addbookmark(None)
        else:
            event.Skip()

    def afetr_init(self):
        if self.tdata:
            try:
                data = decodestring(self.tdata[0][0].data).decode("utf-8")
            except:
                data = decodebytes(self.tdata[0][0].data.encode("utf-8")).decode(
                    "utf-8"
                )
            self.load_str(self.html_from_str(data))

    def html_from_str(self, str_body):
        color = get_colour(wx.SYS_COLOUR_3DFACE)
        return (
            (
                '<!DOCTYPE html><html><head><base href="static://" target="_blank"></head><body bgcolor=\'%s\'>'
                % color
            )
            + str_body
            + "</body></html>"
        )

    def on_key_j(self, event):
        self.execute_javascript("window.scrollBy(0,50);")

    def on_key_k(self, event):
        self.execute_javascript("window.scrollBy(0,-50);")

    def on_key_n(self, event):
        wx.PostEvent(
            wx.GetApp().GetTopWindow(),
            wx.CommandEvent(wx.EVT_MENU.typeId, id=ID_WEB_NEW_WINDOW),
        )

    def on_key_l(self, event):
        self.get_parent_form().GetParent().body.new_child_page(
            "^standard/webview/gotopanel.html", title="Go"
        )

    def accept_page(self, page):
        self.status["address"] = page
        if "pdf_info" in page:
            http = wx.GetApp().get_http(self)
            response = http.get(self, str(page), user_agent="webkit")
            p = response.ptr()
            f = NamedTemporaryFile(delete=False)
            f.write(p)
            name = f.name
            f.close()
            okno = (
                wx.GetApp()
                .GetTopWindow()
                .new_main_page("^standard/pdfviewer/pdfviewer.html", page, None)
            )
            okno.body["PDFVIEWER"].LoadFile(name, True)
            return False
        else:
            return True

    def status_text(self, txt):
        if txt and txt != "":
            self.status["txt"] = "INFO:" + txt
        else:
            self.status["txt"] = ""

    def status_text_error(self, txt):
        self.status["txt"] = "ERROR:" + txt

    def set_status(self, status, url):
        if status == self.LOAD_CONNECT:
            if url and url != "None":
                self.status_text("Contacting " + url)
            else:
                self.status_text("Contacting ...")
        if status == self.LOAD_START:
            if url and url != "None":
                self.status_text("Loading " + url)
        if status == self.LOAD_FINISH_OK:
            self.status_text("")
            self.href = url
        if status == self.LOAD_FINISH_FAILED:
            self.status_text_error("Error in load page: " + url)

    def progress_changed(self, progress):
        self.progress = progress
        if progress < 100:
            self.status["progress"] = progress
            self.status["txt"] = "Loading: " + str(progress) + "%"
        else:
            self.status["progress"] = -1

    def new_win0(self):
        okno = (
            wx.GetApp()
            .GetTopWindow()
            .new_main_page("^standard/webview/widget_web.html", "")
        )
        return okno.body.WEB

    def new_win(self, bstr_url):
        okno = (
            wx.GetApp()
            .GetTopWindow()
            .new_main_page("^standard/webview/widget_web.html", bstr_url)
        )
        okno.body.WEB.go(bstr_url)
        return True

    def new_child(self, bstr_url):
        okno = self.get_parent_form().any_parent_command(
            "new_child_page", "^standard/webview/widget_web.html"
        )
        dx = 800
        dy = 600
        if "bestwidth" in bstr_url or "bestheight" in bstr_url:
            url_get = bstr_url.split("?")
            if len(url_get) > 1:
                url_get = url_get[1]
                url_get = url_get.split("&")
                for pos in url_get:
                    pos2 = pos.split("=")
                    if len(pos2) > 1:
                        if pos2[0] == "bestwidth":
                            dx = int(pos2[1])
                        if pos2[0] == "bestheight":
                            dy = int(pos2[1])
        okno.body.SetBestSize((dx, dy))
        okno.body.WEB.Go(bstr_url)
        return True

    def set_title(self, title):
        if title:
            if len(title) < 32:
                title2 = title
            else:
                title2 = title[:30] + "..."
        else:
            title2 = "Empty page"
        if hasattr(self.get_parent_form(), "any_parent_command"):
            self.get_parent_form().any_parent_command(
                "change_notebook_page_title", title2
            )

    def get_status(self):
        return self.status

    def go(self, href):
        find = False
        href2 = href.strip()
        if " " in href2:
            find = True
        if not "localhost" in href2 and not "." in href2:
            find = True
        if not find:
            url = href
            # if url[-4:].lower() == ".pdf":
            #    self.pdf = url
            #    x = "/" if wx.Platform == "__WXMSW__" else ""
            #    return self.go(
            #        "file://"
            #        + x
            #        + os.path.join(
            #            wx.GetApp().root_path, "static/pdfjs/web/viewer.html"
            #        ).replace("\\", "/")
            #    )
            if "://" in url:
                if "127.0.0.2" in url:
                    s = self._local_request(url + "&only_content=1")
                    self.load_str(s)
                else:
                    self.load_url(url)
            else:
                if "." in url:
                    self.load_url("http://" + url)
                else:
                    self.load_url("https://www.google.pl/search?q=" + url)

            if hasattr(self.get_parent_form(), "go_event"):
                self.get_parent_form().go_event(url)
        else:
            if href2 == "":
                pass
            else:
                q = urllib.parse.quote(href2)
                self.load_url("https://www.google.pl/search?q=" + q)

    def on_key_pressed(self, event):
        event.Skip()

    def on_status_message(self, event):
        self.status_text(event.GetString())

    def on_address_changed(self, event):
        pass

    def on_load_start(self, event):
        self.set_status(self.LOAD_START, event.GetString())

    def on_load_end(self, event):
        self.set_status(self.LOAD_FINISH_OK, event.GetString())
        if hasattr(self.get_parent_form(), "loaded_event"):
            self.get_parent_form().loaded_event()

        if self.pdf:
            if self.pdf.startswith("file://"):
                if wx.Platform == "__WXMSW__":
                    x = open(self.pdf.replace("file:///", ""), "rb")
                else:
                    x = open(self.pdf.replace("file://", ""), "rb")
                buf = b64encode(x.read())
                x.close()
                self.pdf = None
                cmd = JAVASCRIPT_CODE % buf.decode("utf-8")
                self.execute_javascript(cmd)
                self.pdf = None
            else:
                cmd = 'PDFView.open("%s", 0);' % self.pdf
                self.execute_javascript(cmd)
                self.pdf = None

    def on_load_error(self, event):
        self.set_status(self.LOAD_FINISH_FAILED, event.GetString())

    def on_title_changed(self, event):
        event.Skip()
        title = event.GetString()
        if title.startswith(":"):
            if title != ":":
                self.run_command_from_js(title[1:])
        else:
            self.set_title(title)

    def on_progress(self, event):
        pass

    def on_add_bookmark(self, event):
        if hasattr(self.get_parent_form(), "addbookmark_event"):
            self.get_parent_form().addbookmark_event()

    def get_parent_form(self):
        return None

    def load_url(self, url, cookies=None):
        pass

    def load_str(self, data, base=None):
        pass

    def on_back(self, event):
        pass

    def on_forward(self, event):
        pass

    def on_stop(self, event):
        pass

    def on_refresh(self, event):
        pass

    def can_go_back(self):
        pass

    def can_go_forward(self):
        pass

    def can_stop(self):
        if self.progress < 100:
            return True
        else:
            return False

    def can_refresh(self):
        return True

    def can_addbookmark(self):
        return True

    def execute_javascript(self, script):
        pass

    def on_source(self, event):
        pass

    def on_edit(self, event):
        pass

    def value_to_elem(self, selector, s):
        buf = urllib.parse.quote(s.decode("utf-8"), safe="~@#$&()*!+=:;,.?/'")
        cmd = '$("%s").html(decodeURI("%s"));' % (selector, buf)
        self.execute_javascript(cmd.encode("utf-8"))

    def value_to_var(self, var, s):
        buf = urllib.parse.quote(s.decode("utf-8"), safe="~@#$&()*!+=:;,.?/'")
        cmd = '%s = decodeURI("%s");' % (var, buf)
        self.execute_javascript(cmd.encode("utf-8"))

    def run_command_from_js(self, cmd):
        l = split2(cmd, "??")
        if l[0] == "href_to_elem":
            x = split2(l[1], "??")
            s = self._local_request(x[0])
            self.value_to_elem(x[1], s)
        elif l[0] == "href_to_var":
            if "?" in l[1]:
                x = l[1].split("?")
                href = x[0]
                parm = x[1]
            else:
                href = l[1]
                parm = None
            s = self._local_request(href, parm)
            self.value_to_var(l[2], s)
        elif l[0] == "run_js":
            self.execute_javascript(l[1])
        elif l[0] == "python":
            self.GetParent().exec_code(l[1])
        elif l[0] == "ajax_get":
            # print("ajax_get", l[1])
            if l[1].startswith("static:/"):
                x = os.path.join(l[1].replace("static:/", wx.GetApp().root_path))
                f = open(x, "rt")
                txt = b64encode(f.read().encode("utf-8")).decode("utf-8")
                f.close()
            else:
                txt = b64encode(self._local_request(l[1])).decode("utf-8")
            fun_id = l[1].split("?")[0]
            if "//127.0.0.2" in fun_id:
                fun_id = fun_id.split("//127.0.0.2")[1]
            cmd = """window.ajax_get_response_fun['%s'](window.atob("%s"));""" % (
                fun_id,
                txt,
            )
            self.execute_javascript(cmd)

        elif l[0] == "ajax_post":
            # print("ajax_post", l[1])
            x = split2(l[1], "??")
            parm = b64decode(x[1].encode("utf-8")).decode("utf-8")
            s = self._local_request(x[0], parm)
            txt = b64encode(s).decode("utf-8")
            fun_id = x[0].split("?")[0]
            if "//127.0.0.2" in fun_id:
                fun_id = fun_id.split("//127.0.0.2")[1]
            cmd = (
                """window.ajax_get_response_fun['%s'](decodeURIComponent(escape(window.atob("%s"))));"""
                % (fun_id, txt)
            )
            self.execute_javascript(cmd)
        elif l[0] == "action":
            x = split2(l[1], "??")
            # cmd = f"window.get_action_data("""
        return

    def clear_history(self):
        pass

    def _local_request(self, uri, parm=None):
        http = wx.GetApp().get_http(self)
        response = http.get(self, uri, user_agent="embeded", parm=parm)
        s = response.ptr()
        return s

    def _get_http_file(self, uri):
        if "schXML" in uri:
            print(uri)
        if uri.startswith("http://127.0.0.2"):
            if uri.startswith("http://127.0.0.2/data") and "?" in uri:
                data = split2(uri, "?")
                s = b64decode(data[1].encode("utf-8"))
                return (s, None)
            elif uri.startswith("http://127.0.0.2/fonts/"):
                if uri.startswith("http://127.0.0.2/fonts/fontawesome"):
                    uri2 = uri.replace(
                        "127.0.0.2/fonts/", "127.0.0.2/static/fonts/fork-awesome/fonts/"
                    )
                else:
                    uri2 = uri.replace(
                        "127.0.0.2/fonts/",
                        "127.0.0.2/static/themes/bootstrap-material-design/fonts/",
                    )
            elif uri.startswith("http://127.0.0.2/file/"):
                return (None, uri.replace("http://127.0.0.2/file/", ""))
            else:
                uri2 = uri

            if "/images/ui" in uri2:
                uri2 = (
                    "/static/themes/bootstrap/images/ui"
                    + uri2.split("/images/ui")[1].split("#")[0]
                )

            if uri.startswith("http://127.0.0.2/static") and not "?" in uri:
                path = uri.replace("http://127.0.0.2", "")
                return (None, path)
            elif "/site_media/" in uri and not "?" in uri:
                path = wx.GetApp().cwd + uri.replace("http://127.0.0.2", "").replace(
                    "site_media", "media"
                )
                return (None, path)
            elif uri.startswith("http://127.0.0.2/?:"):
                self.run_command_from_js(uri.replace("http://127.0.0.2/?:", ""))
                return ("", None)
            else:
                s = self._local_request(uri2)
                return (s, None)
        return (None, None)

    def show_error(self, title, description):
        # toaster = TB.ToasterBox(self, scrollType=TB.TB_SCR_TYPE_FADE)
        # toaster.SetPopupPauseTime(5000)
        # toaster.SetPopupText(description)
        # toaster.SetTitle(title)
        # toaster.Play()
        print("ERROR: ", title)
        print(description)

    def WebBack(self):
        return self.on_back(None)

    def WebForward(self):
        return self.on_forward(None)

    def CanWebBack(self):
        return self.can_go_back()

    def CanWebForward(self):
        return self.can_go_forward()
