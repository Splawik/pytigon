# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import schserw.schsys.initdjango


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SChApp',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Name', max_length=255)),
                ('module_title', models.CharField(verbose_name='Module title', null=True, max_length=32, blank=True)),
                ('title', models.CharField(verbose_name='Title', null=True, max_length=255, blank=True)),
                ('perms', models.BooleanField(verbose_name='Perms', default=False)),
                ('index', models.CharField(verbose_name='Index', null=True, max_length=255, blank=True)),
                ('model_code', models.TextField(editable=False, verbose_name='Model code', null=True, blank=True)),
                ('view_code', models.TextField(editable=False, verbose_name='View code', null=True, blank=True)),
                ('urls_code', models.TextField(editable=False, verbose_name='Urls code', null=True, blank=True)),
                ('tasks_code', models.TextField(verbose_name='Tasks code', null=True, blank=True)),
                ('doc', models.TextField(editable=False, verbose_name='Doc', null=True, blank=True)),
                ('user_param', models.TextField(verbose_name='Urser parameter', null=True, blank=True)),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name': 'SChApp',
                'verbose_name_plural': 'SChApp',
            },
        ),
        migrations.CreateModel(
            name='SChAppMenu',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Name', max_length=255)),
                ('url', models.CharField(verbose_name='Url', max_length=255)),
                ('url_type', models.CharField(max_length=16, verbose_name='Url type', null=True, default='-', choices=[('Default', '-'), ('shtml', 'shtml'), ('panel', 'panel')], blank=True)),
                ('perms', models.CharField(verbose_name='Perms', null=True, max_length=255, blank=True)),
                ('icon', models.CharField(verbose_name='Icon', max_length=255)),
                ('icon_size', models.CharField(verbose_name='Icon size', default='1', max_length=1, choices=[('0', 'small'), ('1', 'medium'), ('2', 'large')])),
                ('parent', schserw.schsys.initdjango.HiddenForeignKey(verbose_name='Parent', to='schbuilder.SChApp')),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name': 'SChAppMenu',
                'verbose_name_plural': 'SChAppMenu',
            },
        ),
        migrations.CreateModel(
            name='SChAppSet',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Name', max_length=64)),
                ('title', models.CharField(verbose_name='Title', max_length=255)),
                ('ext_apps', models.CharField(verbose_name='Extern applications', null=True, max_length=255, blank=True)),
                ('plugins', models.CharField(verbose_name='Plugins', null=True, max_length=255, blank=True)),
                ('gui_type', models.CharField(verbose_name='Gui type', max_length=32, choices=[('standard', 'standard'), ('modern', 'modern'), ('tree', 'tree'), ('tray', 'tray'), ('dialog', 'dialog'), ('one_form', 'one_form')])),
                ('gui_elements', models.CharField(verbose_name='Gui elements', null=True, max_length=255, blank=True)),
                ('is_hybrid', models.BooleanField(verbose_name='Is hybrid', default=False)),
                ('start_page', models.CharField(verbose_name='Start page', null=True, max_length=255, blank=True)),
                ('user_app_template', models.TextField(editable=False, verbose_name='User application template', null=True, blank=True)),
                ('doc', models.TextField(editable=False, verbose_name='Doc', null=True, blank=True)),
                ('desktop_gui_type', models.CharField(verbose_name='Gui type for pc web browser', default='auto', max_length=32, choices=[('auto', 'auto'), ('desktop_standard', 'desktop_standard'), ('desktop_modern', 'desktop_modern'), ('desktop_traditional', 'desktop_traditional'), ('tablet_standard', 'tablet_standard'), ('tablet_modern', 'tablet_modern'), ('tablet_traditional', 'tablet_traditional'), ('smartfon_standard', 'smartfon_standard'), ('smartfon_modern', 'smartfon_modern'), ('smartfon_traditional', 'smartfon_traditional')])),
                ('smartfon_gui_type', models.CharField(verbose_name='Gui type for smartfon', default='auto', max_length=32, choices=[('auto', 'auto'), ('desktop_standard', 'desktop_standard'), ('desktop_modern', 'desktop_modern'), ('desktop_traditional', 'desktop_traditional'), ('tablet_standard', 'tablet_standard'), ('tablet_modern', 'tablet_modern'), ('tablet_traditional', 'tablet_traditional'), ('smartfon_standard', 'smartfon_standard'), ('smartfon_modern', 'smartfon_modern'), ('smartfon_traditional', 'smartfon_traditional')])),
                ('tablet_gui_type', models.CharField(verbose_name='Gui type for tablet', default='auto', max_length=32, choices=[('auto', 'auto'), ('desktop_standard', 'desktop_standard'), ('desktop_modern', 'desktop_modern'), ('desktop_traditional', 'desktop_traditional'), ('tablet_standard', 'tablet_standard'), ('tablet_modern', 'tablet_modern'), ('tablet_traditional', 'tablet_traditional'), ('smartfon_standard', 'smartfon_standard'), ('smartfon_modern', 'smartfon_modern'), ('smartfon_traditional', 'smartfon_traditional')])),
                ('user_param', models.TextField(verbose_name='User parameter', null=True, blank=True)),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name': 'SChAppSet',
                'verbose_name_plural': 'SChAppSet',
            },
        ),
        migrations.CreateModel(
            name='SChChoice',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Name', max_length=255)),
                ('verbose_name', models.CharField(verbose_name='Verbose name', max_length=255)),
                ('parent', schserw.schsys.initdjango.HiddenForeignKey(verbose_name='Parent', to='schbuilder.SChApp')),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name': 'SChChoice',
                'verbose_name_plural': 'SChChoice',
            },
        ),
        migrations.CreateModel(
            name='SChChoiceItem',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Name', max_length=255)),
                ('value', models.CharField(verbose_name='Value', max_length=255)),
                ('parent', schserw.schsys.initdjango.HiddenForeignKey(verbose_name='Parent', to='schbuilder.SChChoice')),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name': 'SChChoiceItem',
                'verbose_name_plural': 'SChChoiceItem',
            },
        ),
        migrations.CreateModel(
            name='SChField',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Name', null=True, max_length=255, blank=True)),
                ('description', models.CharField(verbose_name='Description', null=True, max_length=255, blank=True)),
                ('type', models.CharField(verbose_name='Type', max_length=64, choices=[('AutoField', 'AutoField'), ('BooleanField', 'BooleanField'), ('CharField', 'CharField'), ('CommaSeparatedIntegerField', 'CommaSeparatedIntegerField'), ('DateField', 'DateField'), ('DateTimeField', 'DateTimeField'), ('DecimalField', 'DecimalField'), ('EmailField', 'EmailField'), ('FileField', 'FileField'), ('FilePathField', 'FilePathField'), ('FloatField', 'FloatField'), ('ImageField', 'ImageField'), ('IntegerField', 'IntegerField'), ('IPAddressField', 'IPAddressField'), ('NullBooleanField', 'NullBooleanField'), ('PositiveIntegerField', 'PositiveIntegerField'), ('PositiveSmallIntegerField', 'PositiveSmallIntegerField'), ('SlugField', 'SlugField'), ('SmallIntegerField', 'SmallIntegerField'), ('TextField', 'TextField'), ('TimeField', 'TimeField'), ('URLField', 'URLField'), ('XMLField', 'XMLField'), ('ForeignKey', 'ForeignKey'), ('GForeignKey', 'GenericForeignKey'), ('ManyToManyField', 'ManyToManyField'), ('GManyToManyField', 'GenericManyToManyField'), ('HiddenForeignKey', 'HiddenForeignKey'), ('GHiddenForeignKey', 'GenericHiddenForeignKey'), ('UserField', 'UserField'), ('ForeignKeyWidthIcon', 'ForeignKeyWidthIcon'), ('ManyToManyFieldWidthIcon', 'ManyToManyFieldWidthIcon'), ('AutocompleteTextField', 'AutocompleteTextField'), ('ForeignKeyExt', 'ForeignKeyExt'), ('TreeForeignKey', 'TreeForeignKey'), ('GTreeForeignKey', 'GTreeForeignKey')])),
                ('null', models.BooleanField(verbose_name='Null', default=False)),
                ('blank', models.BooleanField(verbose_name='Blank', default=False)),
                ('editable', models.BooleanField(verbose_name='Editable', default=False)),
                ('unique', models.BooleanField(verbose_name='Unique', default=False)),
                ('db_index', models.BooleanField(verbose_name='DB index', default=False)),
                ('default', models.CharField(verbose_name='Default', null=True, max_length=255, blank=True)),
                ('help_text', models.CharField(verbose_name='Help text', null=True, max_length=255, blank=True)),
                ('choices', models.CharField(verbose_name='Choices', null=True, max_length=255, blank=True)),
                ('rel_to', models.CharField(verbose_name='Relation to', null=True, max_length=255, blank=True)),
                ('param', models.CharField(verbose_name='Param', null=True, max_length=255, blank=True)),
                ('url_params', models.CharField(verbose_name='Url params', null=True, max_length=255, blank=True)),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name': 'SChField',
                'verbose_name_plural': 'SChField',
            },
        ),
        migrations.CreateModel(
            name='SChForm',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Name', max_length=64)),
                ('module', models.CharField(verbose_name='Module', null=True, max_length=64, blank=True)),
                ('process_code', models.TextField(verbose_name='Process code', null=True, blank=True)),
                ('end_class_code', models.TextField(verbose_name='End class code', null=True, blank=True)),
                ('end_code', models.TextField(verbose_name='End code', null=True, blank=True)),
                ('doc', models.TextField(verbose_name='Doc', null=True, blank=True)),
                ('parent', schserw.schsys.initdjango.HiddenForeignKey(verbose_name='Parent', to='schbuilder.SChApp')),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name': 'Form',
                'verbose_name_plural': 'Form',
            },
        ),
        migrations.CreateModel(
            name='SChFormField',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Name', max_length=64)),
                ('type', models.CharField(verbose_name='Type', max_length=64, choices=[('BooleanField', 'BooleanField'), ('CharField', 'CharField'), ('ChoiceField', 'ChoiceField'), ('TypedChoiceField', 'TypedChoiceField'), ('DateField', 'DateField'), ('DateTimeField', 'DateTimeField'), ('DecimalField', 'DecimalField'), ('EmailField', 'EmailField'), ('FileField', 'FileField'), ('FilePathField', 'FilePathField'), ('FloatField', 'FloatField'), ('ImageField', 'ImageField'), ('IntegerField', 'IntegerField'), ('IPAddressField', 'IPAddressField'), ('GenericIPAddressField', 'GenericIPAddressField'), ('MultipleChoiceField', 'MultipleChoiceField'), ('TypedMultipleChoiceField', 'TypedMultipleChoiceField'), ('NullBooleanField', 'NullBooleanField'), ('RegexField', 'RegexField'), ('SlugField', 'SlugField'), ('TimeField', 'TimeField'), ('URLField', 'URLField'), ('UserField', 'UserField')])),
                ('required', models.NullBooleanField(verbose_name='Required')),
                ('label', models.CharField(verbose_name='Label', max_length=64)),
                ('initial', models.CharField(verbose_name='Initial', null=True, max_length=64, blank=True)),
                ('widget', models.CharField(verbose_name='Widget', null=True, max_length=64, blank=True)),
                ('help_text', models.CharField(verbose_name='Help text', null=True, max_length=64, blank=True)),
                ('error_messages', models.CharField(verbose_name='Error messages', null=True, max_length=64, blank=True)),
                ('param', models.CharField(verbose_name='Param', null=True, max_length=64, blank=True)),
                ('parent', schserw.schsys.initdjango.HiddenForeignKey(verbose_name='Parent', to='schbuilder.SChForm')),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name': 'Form field',
                'verbose_name_plural': 'Form field',
            },
        ),
        migrations.CreateModel(
            name='SChTable',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('base_table', models.CharField(verbose_name='Base table', null=True, max_length=255, blank=True)),
                ('name', models.CharField(verbose_name='Name', max_length=255)),
                ('verbose_name', models.CharField(verbose_name='Verbose name', max_length=255)),
                ('verbose_name_plural', models.CharField(verbose_name='Verbose name plural', max_length=255)),
                ('metaclass_code', models.TextField(editable=False, verbose_name='Metaclass code', null=True, blank=True)),
                ('table_code', models.TextField(editable=False, verbose_name='Table code', null=True, blank=True)),
                ('doc', models.TextField(editable=False, verbose_name='Doc', null=True, blank=True)),
                ('generic', models.BooleanField(verbose_name='Generic', default=False)),
                ('url_params', models.CharField(verbose_name='Url params', null=True, max_length=255, blank=True)),
                ('proxy_model', models.CharField(verbose_name='Proxy model', null=True, max_length=255, blank=True)),
                ('parent', schserw.schsys.initdjango.HiddenForeignKey(verbose_name='Parent', to='schbuilder.SChApp')),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name': 'SChTable',
                'verbose_name_plural': 'SChTable',
            },
        ),
        migrations.CreateModel(
            name='SChTask',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Name', max_length=255)),
                ('code', models.TextField(verbose_name='Code', null=True, blank=True)),
                ('doc', models.TextField(verbose_name='Doc', null=True, blank=True)),
                ('parent', schserw.schsys.initdjango.HiddenForeignKey(verbose_name='Parent', to='schbuilder.SChApp')),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name': 'SChTask',
                'verbose_name_plural': 'SChTask',
            },
        ),
        migrations.CreateModel(
            name='SChTemplate',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Name', max_length=255)),
                ('direct_to_template', models.NullBooleanField(verbose_name='Direct to template')),
                ('url', models.CharField(verbose_name='Url', null=True, max_length=64, blank=True)),
                ('url_parm', models.CharField(verbose_name='Parameters passed to the template', null=True, max_length=128, blank=True)),
                ('template_code', models.TextField(editable=False, verbose_name='Template code', null=True, blank=True)),
                ('parent', schserw.schsys.initdjango.HiddenForeignKey(verbose_name='Parent', to='schbuilder.SChApp')),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name': 'SChTemplate',
                'verbose_name_plural': 'SChTemplate',
            },
        ),
        migrations.CreateModel(
            name='SChUrl',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('reg_expr', models.CharField(verbose_name='Regular expression', max_length=255)),
                ('callback_fun', models.CharField(verbose_name='Callback function', max_length=64)),
                ('dictionary', models.CharField(verbose_name='Dictionary', null=True, max_length=255, blank=True)),
                ('name', models.CharField(verbose_name='Name', null=True, max_length=64, blank=True)),
                ('parent', schserw.schsys.initdjango.HiddenForeignKey(verbose_name='Parent', to='schbuilder.SChApp')),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name': 'SChUrl',
                'verbose_name_plural': 'SChUrl',
            },
        ),
        migrations.CreateModel(
            name='SChView',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Name', max_length=255)),
                ('view_type', models.CharField(verbose_name='View type', max_length=1, choices=[('t', 'Table action'), ('r', 'Row action'), ('u', 'View')])),
                ('param', models.CharField(verbose_name='Param', null=True, max_length=255, blank=True)),
                ('url', models.CharField(verbose_name='Url', null=True, max_length=255, blank=True)),
                ('view_code', models.TextField(editable=False, verbose_name='View code', null=True, blank=True)),
                ('doc', models.TextField(editable=False, verbose_name='Doc', null=True, blank=True)),
                ('url_params', models.CharField(verbose_name='Url params', null=True, max_length=255, blank=True)),
                ('ret_type', models.CharField(verbose_name='Return value type', default='U', max_length=1, choices=[('T', 'Template'), ('O', 'Odf'), ('P', 'Pdf'), ('J', 'Json'), ('X', 'Xml'), ('U', 'User defined')])),
                ('parent', schserw.schsys.initdjango.HiddenForeignKey(verbose_name='Parent', to='schbuilder.SChApp')),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name': 'SChView',
                'verbose_name_plural': 'SChView',
            },
        ),
        migrations.AddField(
            model_name='schfield',
            name='parent',
            field=schserw.schsys.initdjango.HiddenForeignKey(verbose_name='Parent', to='schbuilder.SChTable'),
        ),
        migrations.AddField(
            model_name='schapp',
            name='parent',
            field=models.ForeignKey(verbose_name='Parent', to='schbuilder.SChAppSet'),
        ),
    ]
