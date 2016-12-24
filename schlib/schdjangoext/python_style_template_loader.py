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

import os
import codecs

from django.conf import settings
from django.template import TemplateDoesNotExist
from django.utils._os import safe_join
from django.template.loaders.base  import Loader as BaseLoader
import django.template.loaders.filesystem

from schlib.schdjangoext.django_ihtml import ihtml_to_html

class FSLoader(django.template.loaders.filesystem.Loader):
    is_usable = True

    def load_template_source(self, template_name, template_dirs=None):
        return django.template.loaders.filesystem.Loader.load_template_source(self, template_name, template_dirs)


class Loader(BaseLoader):
    """Loader compile ihtml file to standard html file and based on language load related compiled template"""

    is_usable = True

    def get_template_sources(self, template_name, template_dirs=None):
        if not template_dirs:
            template_dirs = settings.TEMPLATES[0]['DIRS']
        for template_dir in template_dirs:
            try:
                yield safe_join(template_dir + '_src',
                                template_name.replace('.html', '.ihtml'))
            except UnicodeDecodeError:
                raise
            except ValueError:
                pass

    def load_template_source(self, template_name, template_dirs=None):
        tried = []
        template_name_base = template_name
        for pos in settings.LANGUAGES:
            template_name_base = template_name_base.replace('_'+pos[0]+'.html', '.html')
            for filepath in self.get_template_sources(template_name_base, template_dirs):
                filepath2 = filepath.replace('_src', '').replace('.ihtml', '.html')
                try:
                    write = False
                    if os.path.exists(filepath):
                        if not os.path.exists(os.path.dirname(filepath2)):
                            os.makedirs(os.path.dirname(filepath2))
                        if os.path.exists(filepath2):
                            time2 = os.path.getmtime(filepath2)
                            time1 = os.path.getmtime(filepath)
                            if time1 > time2:
                                write = True
                        else:
                            write = True
                        if write:
                            langs = []
                            for pos in settings.LANGUAGES:
                                langs.append(pos[0])
                            for lang in langs:
                                try:
                                    ret = ihtml_to_html(filepath, lang=lang)
                                    if ret:
                                        try:
                                            if lang=='en':
                                                with codecs.open(filepath2, 'w', encoding='utf-8') as f:
                                                    f.write(ret)
                                            else:
                                                with codecs.open(filepath2.replace('.html', '_'+lang+".html"),
                                                        'w', encoding='utf-8') as f:
                                                    f.write(ret)
                                        except:
                                            import traceback
                                            import sys
                                            print(sys.exc_info())
                                            print(traceback.print_exc())
                                except:
                                    pass
                        tried.append(filepath)
                except IOError:
                    tried.append(filepath)
        if tried:
            error_msg = 'Tried %s' % tried
        else:
            error_msg = \
                'Your TEMPLATE_DIRS setting is empty. Change it to point to at least one template directory.'
        raise TemplateDoesNotExist(error_msg)

