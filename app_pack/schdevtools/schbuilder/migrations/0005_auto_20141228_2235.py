# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import schserw.schsys.initdjango


class Migration(migrations.Migration):

    dependencies = [
        ('schbuilder', '0004_schtask_schtasks'),
    ]

    operations = [
        #migrations.RemoveField(
        #    model_name='schtasks',
         #   name='parent',
        #),
        #migrations.DeleteModel(
        #    name='SChTasks',
        #),
        #migrations.AddField(
        #    model_name='schapp',
        #    name='tasks_code',
        #    field=models.TextField(verbose_name='Tasks code', null=True, blank=True),
         #   preserve_default=True,
        #),
        migrations.AddField(
            model_name='schtask',
            name='parent',
            field=schserw.schsys.initdjango.HiddenForeignKey(default=None, to='schbuilder.SChApp', verbose_name='Parent'),
            preserve_default=False,
        ),
    ]
