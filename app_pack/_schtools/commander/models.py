# -*- coding: utf-8 -*-

import django
from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.utils.encoding import python_2_unicode_compatible

import os, os.path
import sys
from schlib.schhtml.htmltools import superstrip








file_manager_sort_choices = (
    ("N","Name"),
    ("S","Size"),
    ("T","Time"),
    
    )





