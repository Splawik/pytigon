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

import cherrypy
import django.core.handlers.wsgi
import os

from schlib.schtasks.cherrypy_task import subscribe,  get_process_manager


cherrypy.server.max_request_body_size = 0
cherrypy.server.socket_timeout = 60


class ModWsgiHandler(django.core.handlers.wsgi.WSGIHandler):

    def __init__(self, address):
        self.address = address
        return django.core.handlers.wsgi.WSGIHandler.__init__(self)

    def __call__(self, environ, start_response):
        if self.address:
            from django.conf import settings
            settings.BASE_URL = 'http://' + self.address
            settings.URL_ROOT_FOLDER = ''
        return django.core.handlers.wsgi.WSGIHandler.__call__(self, environ,
                start_response)


class CherryServer(object):

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.engine = cherrypy.engine

        log_name_error = os.path.join(os.path.expanduser('~'), '.pytigon/schserw_error.log')
        log_name_access = os.path.join(os.path.expanduser('~'), '.pytigon/schserw_access.log')

        globalconf = {
            'server.socket_host': self.address,
            'server.socket_port': self.port,
            'server.thread_pool': 10,
            'log.screen': False,
            'log.access_file': log_name_access,
            'log.error_file': log_name_error,
            'environment': 'production',
            }
        cherrypy.config.update(globalconf)
        if '127.0.0' in self.address:
            cherrypy.tree.graft(ModWsgiHandler(self.address + ':' + str(self.port)))
        else:
            cherrypy.tree.graft(ModWsgiHandler(None))

        subscribe()
        get_process_manager()


    def start(self):
        try:
            cherrypy.engine.start()
            cherrypy.engine.wait(state=cherrypy.engine.states.STARTED)
        except KeyboardInterrupt:
            cherrypy.engine.stop()

    def stop(self):
        cherrypy.engine.stop()
        cherrypy.engine.exit()

    def restart(self):
        cherrypy.engine.restart()


