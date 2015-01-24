# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schbuilder', '0010_schtask'),
    ]

    operations = [
        migrations.AddField(
            model_name='schapp',
            name='user_param',
            field=models.TextField(verbose_name='Urser parameter', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='schappset',
            name='user_param',
            field=models.TextField(verbose_name='User parameter', blank=True, null=True),
            preserve_default=True,
        ),
    ]
