# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Autocomplete',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('type', models.CharField(max_length=64)),
                ('label', models.CharField(max_length=64)),
                ('value', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('key', models.CharField(max_length=32)),
                ('value', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name': 'Parameter',
                'verbose_name_plural': 'Parameter',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('identifier', models.CharField(max_length=16)),
                ('name', models.CharField(max_length=64)),
                ('type', models.CharField(max_length=1, choices=[('O', 'Operator'), ('E', 'Employee'), ('C', 'Customer'), ('F', 'Firm')])),
                ('user', models.ForeignKey(unique=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'Person',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProxyGroup',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.group',),
        ),
        migrations.CreateModel(
            name='ProxyUser',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.user',),
        ),
    ]
