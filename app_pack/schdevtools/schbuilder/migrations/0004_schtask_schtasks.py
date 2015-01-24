# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import schserw.schsys.initdjango


class Migration(migrations.Migration):

    dependencies = [
        ('schbuilder', '0003_schview_ret_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='SChTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='Name', max_length=255)),
                ('code', models.TextField(null=True, verbose_name='Code', blank=True)),
                ('doc', models.TextField(verbose_name='Doc')),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name': 'SChTask',
                'verbose_name_plural': 'SChTask',
            },
            bases=(models.Model,),
        ),
    ]
