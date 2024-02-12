from django.utils.translation import gettext_lazy as _

import os
import sys
import datetime
import time
from queue import Empty
from pytigon_lib.schtasks.publish import publish


from pytigon_lib.schtasks.publish import publish
from pytigon_lib.schfs.tasks import filesystemcmd


@publish("vfs_action")
def vfs_action(cproxy=None, **kwargs):

    return filesystemcmd(cproxy, **kwargs)
