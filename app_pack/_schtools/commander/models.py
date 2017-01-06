# -*- coding: utf-8 -*-

import django
from django.db import models
from schlib.schdjangoext.fields import *

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

import os, os.path
import sys
from schlib.schhtml.htmltools import superstrip








file_manager_sort_choices = (
    ("N","Name"),
    ("S","Size"),
    ("T","Time"),
    
    )






