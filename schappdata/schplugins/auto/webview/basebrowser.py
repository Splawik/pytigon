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

import wx
import six

from tempfile import NamedTemporaryFile
from schlib.schhttptools.httpclient import get_cookie_str
from base64 import decodebytes, b64encode, b64decode
import urllib
from schcli.guilib.tools import get_colour
from schcli.guilib.schevent import ID_WEB_NEW_WINDOW
from schlib.schtools.tools import split2

import os


class BaseWebBrowser(object):

    LOAD_CONNECT = 0
    LOAD_START = 1
    LOAD_FINISH_OK = 2
    LOAD_FINISH_FAILED = 3

    def __init__(self):
        #self.test_ctrl = True
        self.progress = -1
        self.href = ''
        self.status = {
            'stat': -1,
            'progress': -1,
            'txt': None,
            'address': None,
            }

        if hasattr(self.get_shtml_window().GetParent(), 'handleInfo'):
            self.get_shtml_window().GetParent().handleInfo['browser'] = self
        #if self.tdata:
        #    try:
        #        data =  decodestring(self.tdata[0][0].data).decode('utf-8')
        #    except:
        #        data =  decodebytes(self.tdata[0][0].data.encode('utf-8')).decode('utf-8')
        #    self.load_str(self.html_from_str(data))

        aTable = [
                #(0, wx.WXK_F2,  self.OnExtButtonClick),
                (wx.ACCEL_ALT, ord('J'), self.on_key_j),
                (wx.ACCEL_ALT, ord('K'), self.on_key_k),
                (wx.ACCEL_CTRL, ord('N'), self.on_key_n),
                (wx.ACCEL_CTRL, ord('L'), self.on_key_l),
                #(wx.ACCEL_CTRL, ord('H'), self.on_key_h),
                #(wx.ACCEL_CTRL, ord('L'), self.on_key_l),
                
                 ]
        self.set_acc_key_tab(aTable)

        self.redirect_to_html = [None, None]
        self.redirect_to_local = True
        self.last_status_txt = ''

        self.pdf = None

        if hasattr(self.GetParent(), 'get_parent'):
            self.GetParent().get_parent().on_check_can_go_forward = self.on_check_can_go_forward
            self.GetParent().get_parent().on_check_can_go_back = self.on_check_can_go_back
            self.GetParent().get_parent().back = self.back
            self.GetParent().get_parent().forward = self.forward


    def on_check_can_go_forward(self, event):
        test = self.can_go_forward()
        event.Enable(test)

    def on_check_can_go_back(self, event):
        test =  self.can_go_back()
        event.Enable(test)

    def back(self):
        return self.on_back(None)

    def forward(self):
        return self.on_forward(None)

    def afetr_init(self):
        if self.tdata:
            try:
                data =  decodestring(self.tdata[0][0].data).decode('utf-8')
            except:
                data =  decodebytes(self.tdata[0][0].data.encode('utf-8')).decode('utf-8')
            print("after_init:load_str")
            self.load_str(self.html_from_str(data))

    def html_from_str(self, str_body):
        color = get_colour(wx.SYS_COLOUR_3DFACE)
        return ("<!DOCTYPE html><html><head><base href=\"static://\" target=\"_blank\"></head><body bgcolor='%s'>" % color) + str_body+"</body></html>"

    def on_key_j(self, event):
        self.execute_javascript("window.scrollBy(0,50);")

    def on_key_k(self, event):
        self.execute_javascript("window.scrollBy(0,-50);")

    def on_key_n(self, event):
        try:
            wx.PostEvent(wx.GetApp().GetTopWindow(), wx.CommandEvent(wx.EVT_MENU.typeId, id=ID_WEB_NEW_WINDOW))
        except:
            wx.PostEvent(wx.GetApp().GetTopWindow(), wx.CommandEvent(wx.EVT_MENU.typeId, winid=ID_WEB_NEW_WINDOW))

    def on_key_l(self, event):
        self.get_shtml_window().GetParent().Body.new_child_page("^standard/webview/gotopanel.html", title="Go")

    def accept_page(self, page):
        self.status['address'] = page
        if 'pdf_info' in page:
            http = wx.GetApp().get_http(self)
            http.get(self, str(page), user_agent='webkit')
            p = http.ptr()
            f = NamedTemporaryFile(delete=False)
            f.write(p)
            name = f.name
            f.close()
            http.clear_ptr()
            okno = \
                wx.GetApp().GetTopWindow().new_main_page('^standard/pdfviewer/pdfviewer.html'
                    , page, None)
            okno.Body['PDFVIEWER'].LoadFile(name, True)
            return False
        else:
            return True
            if 'schtml=1' in page and not wx.GetApp().is_hybrid:
                self.get_shtml_window().any_parent_command('new_child_page', page)
                return False
            elif 'childwin=1' in page:
                self.new_child(page)
                return False
            #elif wx.GetKeyState(wx.WXK_CONTROL) and self.test_ctrl:
            #    self.new_win(page)
            #    return False
            return True

    def _redirect_to_local(self, event):
        self.redirect_to_local = False
        self.OnBeforeLoad(self.url)
        self.redirect_to_local = True

    def on_before_load(self, url):
        http = wx.GetApp().get_http(self)
        http.get(self, str(url), user_agent='embeded')
        s = http.str(conwert_local_path=True)
        base_dir = local_media_path()
        self.LoadString(s)
        http.clear_ptr()
        return True

    def redirect_to_file(self, url):
        http = wx.GetApp().get_http(self)
        http.get(self, str(url), user_agent='embeded')
        s = http.str(conwert_local_path=True)
        base_dir = local_media_path()
        file_url = base_dir + '/test.html'
        file_name = file_url.replace('file://', '')
        f = open(file_name, 'w')
        f.write(s.encode('utf-8'))
        f.close
        return file_url

    def get_local(self, uri, parm=None):
        http = wx.GetApp().get_http(self)
        http.get(self, uri.replace('intercept://', 'http://'), user_agent='embeded', parm=parm)
        s = http.ptr()
        http.clear_ptr()
        return s

    def status_text(self, txt):
        if txt and txt != '':
            self.status['txt'] = 'INFO:' + txt
        else:
            self.status['txt'] = ''

    def status_text_error(self, txt):
        self.status['txt'] = 'ERROR:' + txt

    def set_status(self, status, url):
        if status == self.LOAD_CONNECT:
            if url and url != 'None':
                self.status_text('Contacting ' + url)
            else:
                self.status_text('Contacting ...')
        if status == self.LOAD_START:
            if url and url != 'None':
                self.status_text('Loading ' + url)
        if status == self.LOAD_FINISH_OK:
            self.status_text('')
            self.href = url
        if status == self.LOAD_FINISH_FAILED:
            self.status_text_error('Error in load page: ' + url)


    def progress_changed(self, progress):
        self.progress = progress
        if progress < 100:
            self.status['progress'] = progress
            self.status['txt'] = 'Loading: ' + str(progress) + '%'
        else:
            self.status['progress'] = -1

    def new_win0(self):
        okno = \
            wx.GetApp().GetTopWindow().new_main_page('^standard/webview/widget_web.html'
                , '')
        return okno.Body.WEB

    def new_win(self, bstr_url):
        okno = \
            wx.GetApp().GetTopWindow().new_main_page('^standard/webview/widget_web.html'
                , bstr_url)
        #okno.Body.WEB.test_ctrl = False
        okno.Body.WEB.go(bstr_url)
        #okno.Body.WEB.test_ctrl = True
        return True

    def new_child(self, bstr_url):
        okno = self.get_shtml_window().any_parent_command('new_child_page',
                '^standard/webview/widget_web.html')
        dx = 800
        dy = 600
        if 'bestwidth' in bstr_url or 'bestheight' in bstr_url:
            url_get = bstr_url.split('?')
            if len(url_get) > 1:
                url_get = url_get[1]
                url_get = url_get.split('&')
                for pos in url_get:
                    pos2 = pos.split('=')
                    if len(pos2) > 1:
                        if pos2[0] == 'bestwidth':
                            dx = int(pos2[1])
                        if pos2[0] == 'bestheight':
                            dy = int(pos2[1])
        okno.Body.SetBestSize((dx, dy))
        okno.Body.WEB.Go(bstr_url)
        return True

    def set_title(self, title):
        if title:
            if len(title) < 32:
                #title2 = title.decode('utf-8')title
                title2 = title
            else:
                #title2 = title.decode('utf-8')[:30] + '...'
                title2 = title[:30] + '...'
        else:
            title2="Empty page" 
        if hasattr(self.get_shtml_window(), 'any_parent_command'):
            print("TITLE:", title2)
            self.get_shtml_window().any_parent_command('change_notebook_page_title', title2)

    def get_status(self):
        return self.status

    def transform_url(self, url):
        url2 = url
        #if not url2.startswith('http') and not url2.startswith('file'):
        #    url2 = 'http://' + url2
        if not "://" in url2:
            url2 = 'http://' + url2
        if not self.__class__.logged and '127.0.0.2' in url2:
            self.__class__.logged = True
            cookie = get_cookie_str()
            cookie_tab = cookie.split(';')
            sessionid = None
            for pos in cookie_tab:
                c = pos.split('=')
                if c[0].strip() == 'sessionid':
                    sessionid = c[1].strip()
                    if '?' in url:
                        url2 = url + '&' + 'sessionid=%s' % sessionid
                    else:
                        url2 = url + '?' + 'sessionid=%s' % sessionid
            if '?' in url2:
                url2 = url2 + '&client_param=' + wx.GetApp().get_parm_for_server()
            else:
                url2 = url2 + '?client_param=' + wx.GetApp().get_parm_for_server()
        return url2

    def go(self, href):
        find = False
        href2 = href.strip()
        if ' ' in href2:
            find=True
        if not 'localhost' in href2 and not '.' in href2:
            find=True
        if not find:
            url = self.transform_url(href)
            if url[-4:].lower()=='.pdf':
                self.pdf = url
                x = '/' if wx.Platform == '__WXMSW__' else ''
                return self.go("file://"+x+os.path.join(wx.GetApp().root_path, "static/pdfjs/web/viewer.html").replace('\\','/'))
                #f = open(os.path.join(wx.GetApp().root_path, "static/pdfjs/web/viewer.html"),"rb")
                #buf = f.read()
                #f.close()
                #return self.load_str(buf.decode('utf-8'), "file:///")

            if '://' in url:
                self.load_url(url)
            else:
                if '.' in url:
                    self.load_url('http://' + url)
                else:
                    self.load_url('https://www.google.pl/search?q=' + url)
            if hasattr(self.get_shtml_window(), 'go_event'):
                self.get_shtml_window().go_event(url)
        else:
            if href2=="":
                pass
            else:
                if six.PY2:
                    q = urllib.quote(href2)
                else:
                    q = urllib.parse.quote(href2)

                self.load_url('https://www.google.pl/search?q=' + q)

# callbacks
    def on_key_pressed(self, event):
        #print("OnKeyPressed:basebrowser")
        event.Skip()

    def on_status_message(self, event):
        self.status_text(event.GetString())
        
    def on_address_changed(self, event):
        pass

    def on_load_start(self, event):
        self.set_status(self.LOAD_START, event.GetString())


    def on_load_end(self, event):
        self.set_status(self.LOAD_FINISH_OK, event.GetString())
        if hasattr(self.get_shtml_window(), 'loaded_event'):
            self.get_shtml_window().loaded_event()
        #print("XXXXXXXX", self.GetParent().get_parent())
        #self.GetParent().get_parent().reg_href(event.GetString(), {})

        if self.pdf:
            print("X1================================================")
            if self.pdf.startswith('file://'):
                if wx.Platform == '__WXMSW__':
                    x = open(self.pdf.replace('file:///',''), "rb")
                else:
                    x = open(self.pdf.replace('file://',''), "rb")
                buf = b64encode(x.read())
                x.close()
                self.pdf = None
                cmd = "var pdf_ptr=base64toBlob(\"%s\", 'application/pdf'); PDFView.open(URL.createObjectURL(pdf_ptr), 0);" % buf.decode('utf-8')
                #cmd = "PDFView.open(\"%s\", 0);" % self.pdf
                self.execute_javascript(cmd)
                self.pdf = None
            else:
                cmd = "PDFView.open(\"%s\", 0);" % self.pdf
                self.execute_javascript(cmd)
                self.pdf = None



    def on_load_error(self, event):
        self.set_status(self.LOAD_FINISH_FAILED, event.GetString())
   
        
    def on_title_changed(self, event):
        event.Skip()
        title = event.GetString()
        if title.startswith(':'):
            print("TITLE:", title)
            if title != ":":
                self.run_command_from_js(title[1:])
        else:
            self.set_title(title)
        
#    def on_loaded(self, event):
#        if hasattr(self.get_shtml_window(), 'loaded_event'):
#            self.get_shtml_window().loaded_event()
        
    def on_progress(self, event):
        pass

    def on_add_bookmark(self, event):
        if hasattr(self.get_shtml_window(), 'addbookmark_event'):
            self.get_shtml_window().addbookmark_event()


# abstract method

    def get_shtml_window(self):
        return None

    def load_url(self, url):
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
        if self.progress >= 0:
            return True
        else:
            return False

    def execute_javascript(self, script):
        pass

    def on_source(self, event):
        pass


    def on_edit(self, event):
        pass


    def value_to_elem(self, selector, s):
        buf = urllib.parse.quote(s.decode('utf-8'), safe='~@#$&()*!+=:;,.?/\'')
        cmd = "$(\"%s\").html(decodeURI(\"%s\"));" % (selector, buf)
        self.execute_javascript(cmd.encode('utf-8'))

    def value_to_var(self, var, s):
        buf = urllib.parse.quote(s.decode('utf-8'), safe='~@#$&()*!+=:;,.?/\'')
        cmd = "%s = decodeURI(\"%s\");" % (var, buf)
        self.execute_javascript(cmd.encode('utf-8'))


    def run_command_from_js(self, cmd):
        l = split2(cmd, '??')
        if l[0] == 'href_to_elem':
            x = split2(l[1], '??')
            s = self.get_local(x[0])
            self.value_to_elem(x[1], s)
        elif l[0] == 'href_to_var':
            if '?' in l[1]:
                x = l[1].split('?')
                href = x[0]
                parm = x[1]
            else:
                href = l[1]
                parm = None
            s = self.get_local(href, parm)
            self.value_to_var(l[2], s)
        elif l[0] == 'run_js':
            self.execute_javascript(l[1])
        elif l[0] == 'python':
            self.GetParent().exec_code(l[1])
        elif l[0] == 'ajax_get':
            if l[1].startswith('static:/'):
                x = os.path.join( l[1].replace('static:/',wx.GetApp().root_path))
                f = open(x, "rt")
                txt = b64encode(f.read().encode('utf-8')).decode('utf-8')
                f.close()
            else:
                txt = b64encode(self.get_local(l[1])).decode('utf-8')
            fun_id = l[1].split('?')[0]
            if '//127.0.0.2' in fun_id:
                fun_id = fun_id.split('//127.0.0.2')[1]
            print("FUN_ID_GET:", fun_id)
            cmd = """window.ajax_get_response_fun['%s'](decodeURIComponent(escape(window.atob("%s"))));""" % (fun_id,txt)
            self.execute_javascript(cmd)

        elif l[0] == 'ajax_post':
            x = split2(l[1], '??')
            parm = b64decode(x[1].encode('utf-8')).decode('utf-8')
            s = self.get_local(x[0], parm)
            txt = b64encode(s).decode('utf-8')
            fun_id = x[0].split('?')[0]
            if '//127.0.0.2' in fun_id:
                fun_id = fun_id.split('//127.0.0.2')[1]
            print("FUN_ID_POST:", fun_id)
            cmd = """window.ajax_get_response_fun['%s'](decodeURIComponent(escape(window.atob("%s"))));""" % (fun_id,txt)
            self.execute_javascript(cmd)
        return

    def clear_history(self):
        pass
