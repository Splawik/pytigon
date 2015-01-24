# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schbuilder', '0006_auto_20150119_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='schappset',
            name='desktop_gui_type',
            field=models.CharField(choices=[('auto', 'auto'), ('desktop_standard', 'desktop_standard'), ('desktop_modern', 'desktop_modern'), ('desktop_traditional', 'desktop_traditional'), ('tablet_standard', 'tablet_standard'), ('tablet_modern', 'tablet_modern'), ('tablet_traditional', 'tablet_traditional'), ('smartfon_standard', 'smartfon_standard'), ('smartfon_modern', 'smartfon_modern'), ('smartfon_traditional', 'smartfon_traditional')], verbose_name='Gui type for pc web browser', max_length=32, default='auto'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='schappset',
            name='smartfon_gui_type',
            field=models.CharField(choices=[('auto', 'auto'), ('desktop_standard', 'desktop_standard'), ('desktop_modern', 'desktop_modern'), ('desktop_traditional', 'desktop_traditional'), ('tablet_standard', 'tablet_standard'), ('tablet_modern', 'tablet_modern'), ('tablet_traditional', 'tablet_traditional'), ('smartfon_standard', 'smartfon_standard'), ('smartfon_modern', 'smartfon_modern'), ('smartfon_traditional', 'smartfon_traditional')], verbose_name='Gui type for smartfon', max_length=32, default='auto'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='schappset',
            name='tablet_gui_type',
            field=models.CharField(choices=[('auto', 'auto'), ('desktop_standard', 'desktop_standard'), ('desktop_modern', 'desktop_modern'), ('desktop_traditional', 'desktop_traditional'), ('tablet_standard', 'tablet_standard'), ('tablet_modern', 'tablet_modern'), ('tablet_traditional', 'tablet_traditional'), ('smartfon_standard', 'smartfon_standard'), ('smartfon_modern', 'smartfon_modern'), ('smartfon_traditional', 'smartfon_traditional')], verbose_name='Gui type for tablet', max_length=32, default='auto'),
            preserve_default=True,
        ),
    ]
