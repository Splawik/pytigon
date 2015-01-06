# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schbuilder', '0002_remove_schview_ret_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='schview',
            name='ret_type',
            field=models.CharField(choices=[('T', 'Template'), ('O', 'Odf'), ('P', 'Pdf'), ('J', 'Json'), ('X', 'Xml'), ('U', 'User defined')], default='U', verbose_name='Return value type', max_length=1),
            preserve_default=True,
        ),
    ]
