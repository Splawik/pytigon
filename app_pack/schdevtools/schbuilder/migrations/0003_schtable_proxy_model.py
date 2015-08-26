# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schbuilder', '0002_remove_schtable_proxy_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='schtable',
            name='proxy_model',
            field=models.CharField(null=True, blank=True, max_length=255, verbose_name='Proxy model'),
        ),
    ]
