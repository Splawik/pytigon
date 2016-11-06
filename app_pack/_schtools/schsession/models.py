# -*- coding: utf-8 -*-

import django
from django.db import models
from schlib.schdjangoext.fields import ForeignKey, HiddenForeignKey

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.utils.encoding import python_2_unicode_compatible

import os, os.path
import sys
from schlib.schhtml.htmltools import superstrip











