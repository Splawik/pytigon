# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import schserw.schsys.initdjango


class Migration(migrations.Migration):

    dependencies = [
        ('schbuilder', '0009_auto_20150119_2129'),
    ]

    operations = [
        migrations.CreateModel(
            name='SChTask',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('code', models.TextField(blank=True, verbose_name='Code', null=True)),
                ('doc', models.TextField(blank=True, verbose_name='Doc', null=True)),
                ('parent', schserw.schsys.initdjango.HiddenForeignKey(to='schbuilder.SChApp', verbose_name='Parent')),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name_plural': 'SChTask',
                'verbose_name': 'SChTask',
            },
            bases=(models.Model,),
        ),
    ]
