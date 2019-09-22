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


import wx

def init_plugin_sch_web(app, mainframe, desktop, mgr, menubar, toolbar, accel, base_web_browser,):
    from pytigon_gui.guictrl.ctrl import SChBaseCtrl
    import pytigon_gui.guictrl.ctrl
    from pytigon_gui.guilib import events
    from pytigon_gui.guiframe import form
    from urllib.parse import quote as escape
    init_css_str = \
        """
        body {font-family:sans-serif;font-size:100%; padding:2;}
        table {border:0;vertical-align:top; padding:2;}
        td table { padding: 2; }
        th {border:0; cellpadding:2;}
        td {border:0; vertical-align:top; cellpadding:2;}
        strong,b {font-weight:bold;}
        p { cellpadding:1; border:0; width:100%; }
        h1 {font-size:300%; font-weight: bold; cellpadding:12;}
        h2 {font-size:240%; font-weight: bold; cellpadding:10;}
        h3 {font-size:190%; font-weight: bold; cellpadding:8;}
        h4 {font-size:150%; font-weight: bold; cellpadding:6;}
        h5 {font-size:120%; font-weight: bold; cellpadding:4;}
        h6 {font-size:100%; font-weight: bold; cellpadding:2;}
        a { color:#0000ff; text-decoration: underline; }
        ul {border:0;}
        li {cellpadding:5; width:95%; }
    """

    class Html2(form.SChSashWindow, SChBaseCtrl, base_web_browser):

        logged = False

        def __init__(self, parent, **kwds):
            base_web_browser.__init__(self)
            self.redirect_to_html = [None, None]
            self.redirect_to_local = True
            SChBaseCtrl.__init__(self, parent, kwds)
            form.SChSashWindow.__init__(self, parent, self.href, None,
                                        name=kwds['name'])
            self.body.set_css(init_css_str)
            self.GetParent().any_parent_command('set_handle_info', 'browser', self)
            self.GetParent().any_parent_command('show_info')

            self.source_mod = False

        def on_souce_mod(self, event):
            if self.source_mod:
                self.source_mod = False
            else:
                self.source_mod = True
            self.ctrl.set_view_source_mode(self.source_mod)
            self.Reload()

        def _redirect_to_local(self, event):
            self.redirect_to_local = False
            http = wx.GetApp().get_http(self)
            response = http.get(self, str(self.url), user_agent='webkit')
            s = response.str(conwert_local_path=True)
            self.ctrl.load_html_string(s, 'file://')
            self.redirect_to_local = True

        def _navigation(self, web_view, frame, request, navigation_action, policy_decision):
            url = request.get_uri()
            if self.accept_page(url):
                if self.redirect_to_local and '127.0.0.2' in url:
                    policy_decision.ignore()
                    self.url = url
                    evt = events.RefrParmEvent(events.userEVT_REFRPARM,
                                               self.GetId())
                    self.GetEventHandler().AddPendingEvent(evt)
                    return True
                else:
                    if int(navigation_action.get_reason()) == 0\
                         and int(navigation_action.get_button()) == 2:
                        policy_decision.ignore()
                        self.new_win(url)
                        return True
                    else:
                        return False
            else:
                policy_decision.ignore()
                return True

        def _navigation_new(self, web_view, frame, request, navigation_action, policy_decision):
            url = request.get_uri()
            if self.new_win(url):
                policy_decision.ignore()
                return True
            else:
                return False

        def _create_new(self, web_view, frame):
            return self.new_win0().ctrl

        def _link(self, web_view, title, uri):
            if title and title != '':
                return self.status_text(title)
            if uri and uri != '':
                return self.status_text(uri)
            self.status_text('')

        def _redirect_to_str(self, url):
            http = wx.GetApp().get_http(self)
            response = http.get(self, str(url), user_agent='webkit')
            s = response.str(conwert_local_path=True)
            return s

        def _load_resource(self, web_view, web_frame, web_resource, request, response):
            url = request.get_uri()
            if '127.0.0.2' in url:
                request.set_uri('about:blank')
                if '|' in url:
                    u = url.split('|')
                    s0 = self._redirect_to_str(u[0])
                    s = escape(s0.encode('utf-8'))
                    self.ctrl.execute_script('document.getElementById(\'%s\').innerHTML=decodeURIComponent("%s");'
                             % (u[1], s))
                else:
                    s = escape(self._redirect_to_str(url).encode('utf-8'))

        def _load_status2(self, view, status):
            s = int(self.ctrl.get_property('load-status'))
            uri = str(self.ctrl.get_property('uri'))
            if s == self.WEBKIT_LOAD_PROVISIONAL:
                if uri and uri != 'None':
                    self.StatusText('Contacting ' + uri)
                else:
                    self.StatusText('Contacting ...')
            if s == self.WEBKIT_LOAD_COMMITTED:
                if uri:
                    self.StatusText('Loading: ' + uri)
            if s == self.WEBKIT_LOAD_FINISHED:
                if uri:
                    self.StatusText('')
                self.href = uri
                self.GetParent().any_parent_command('refr_info', 'browser')
                wx.EndBusyCursor()
            if s == self.WEBKIT_LOAD_FIRST_VISUALLY_NON_EMPTY_LAYOUT:
                if uri:
                    self.StatusText('Loading: ' + uri)
                pass
            if s == self.WEBKIT_LOAD_FAILED:
                self.StatusText('Error in load page: ' + uri)

        def _load_status(self, view, status):
            s = int(self.ctrl.get_property('load-status'))
            url = str(self.ctrl.get_property('uri'))
            if s == self.WEBKIT_LOAD_PROVISIONAL:
                self.set_status(self.LOAD_CONNECT, url)
            elif s == self.WEBKIT_LOAD_COMMITTED:
                self.set_status(self.LOAD_START, url)
            elif s == self.WEBKIT_LOAD_FINISHED:
                self.set_status(self.LOAD_FINISH_OK, url)
            elif s == self.WEBKIT_LOAD_FIRST_VISUALLY_NON_EMPTY_LAYOUT:
                pass
            elif s == self.WEBKIT_LOAD_FAILED:
                self.set_status(self.LOAD_FINISH_FAILED, url)

        def _title(self, web_view, frame, title,):
            if title and title != '':
                self.title(title)

        def _progress_changed(self, view, progress):
            return self.progress_changed(progress)

        def on_back(self, event):
            self.HistoryBack()

        def on_forward(self, event):
            self.HistoryForward()

        def on_stop(self, event):
            self.StopLoading()

        def on_refresh(self, event):
            self.Reload()

        def load_url(self, url):
            print('LoadURL')
            self.address_or_parser = url
            self._Refresh()

        def go(self, url):
            print('GO')
            url2 = self.transform_url(url)
            self.GetParent().GetParent().body.GetItem('WEB').LoadURL(url2)

        def on_char(self, event):
            if event.GetKeyCode() == wx.WXK_RETURN:
                return self.OnGo(event)
            else:
                event.Skip()

        def status_text(self, txt):
            self.GetParent().any_parent_command('set_status_text2', txt)

        def on_new_window(self, event):
            event.Skip()

        def on_add_bookmark(self, event):
            event.Skip()

        def can_go_back(self):
            return self.ctrl.can_go_back()

        def can_go_forward(self):
            return self.ctrl.can_go_forward()

        def can_stop(self):
            return True

        def reload(self):
            return self.ctrl.reload()

        def get_status(self):
            return self.get_status()

    pytigon_gui.guictrl.ctrl.HTML2 = Html2


