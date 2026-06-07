from django.utils.translation import gettext_lazy as _

import os
import sys
import datetime
import time
from queue import Empty
from pytigon_lib.schtasks.publish import publish


def deadline_exceeded(cproxy=None, **kwargs):

    actions = Action.objects.exclude(status="CLOSED").filter(
        deadline__lt=timezone.now()
    )
    for action in actions:
        emails = []
        if action.email_action_owner:
            send_mail(
                "You did not complete the task in the allotted time",
                'Action "%s" with a due date of %s has not been completed yet!'(
                    action.description, str(action.deadline)
                ),
                settings.DEFAULT_FROM_EMAIL,
                [
                    action.email_action_owner,
                ],
                fail_silently=False,
            )
        if action.email_deadline_exceeded:
            send_mail(
                "The task was not completed on time",
                'Action "%s" with a due date of %s has not been completed yet!'(
                    action.description, str(action.deadline)
                ),
                settings.DEFAULT_FROM_EMAIL,
                [
                    action.email_deadline_exceeded,
                ],
                fail_silently=False,
            )
