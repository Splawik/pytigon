#!/usr/bin/python

# -*- coding: utf-8 -*-

from django.utils.translation import gettext_lazy as _

import os
import sys
import datetime
import time
from queue import Empty
from pytigon_lib.schtasks.publish import publish


@publish("demo")
def fun2(cproxy=None, **kwargs):

    with RemoteScreen(cproxy, direction="up") as out:
        out.log("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA1")
        for i in range(0, 30):
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA2")
            out.log("item %d" % i)
            time.sleep(1)
        out.info("Info info info")
        out.warning("Warning warning warning")
        out.error("Error error error")
    return "Hello world"
