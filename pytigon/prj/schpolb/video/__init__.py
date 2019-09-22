# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

ModuleTitle = _('Video')
Title = _('Video')
Perms = True
Index = ''
Urls  = (
    ('table/Video/-/form/list/?schtml=desktop',_('Materiały video'),'video.list_video','client://mimetypes/video-x-generic.png'),
)
UserParam = {'icon': 'fa-file-video-o'}