#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys

_lp  = os.path.dirname(os.path.abspath(__file__))
_rp = _lp+"/../.."

sys.path.append(_lp)
sys.path.append(_rp)

from schserw.settings import *

APPSET_TITLE = "Remote connection"
APPSET_NAME = "remote"

LOCAL_SERW_PATH = _lp
LOCAL_ROOT_PATH = _lp+"/.."
ROOT_PATH = _rp

URL_POSTFIX = ''

if len(URL_POSTFIX) > 0:
    STATIC_URL = '/' + URL_POSTFIX + '/static/'
else:
    STATIC_URL = '/static/'

if len(URL_POSTFIX) > 0:
    MEDIA_URL = '/' + URL_POSTFIX + '/app_media/'
else:
    MEDIA_URL = '/app_media/'

sys.path.append(LOCAL_ROOT_PATH)
