from django.utils.translation import gettext_lazy as _

import os
import sys
import datetime
import time
from queue import Empty
from pytigon_lib.schtasks.publish import publish


@publish("demo")
def test_task(cproxy=None, **kwargs):

    if "param" in kwargs:
        print(kwargs["param"])
    if cproxy:
        cproxy.send_event(
            "<ul class='data'></ul><div name='task_end_info' style='display: none;'>Finish</div>"
        )
    for i in range(0, 30):
        if cproxy:
            cproxy.send_event("<li>item %d</li>===>>.data" % i)
        time.sleep(1)
    return True


def test_task2(cproxy=None, **kwargs):

    for i in range(0, 30):
        print("item:", i)
        time.sleep(1)
    return "tast task2 result"
