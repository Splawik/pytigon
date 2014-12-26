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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('module_title', models.CharField(blank=True, null=True, verbose_name='Module title', max_length=32)),
                ('title', models.CharField(blank=True, null=True, verbose_name='Title', max_length=255)),
                ('perms', models.BooleanField(verbose_name='Perms', default=False)),
                ('index', models.CharField(blank=True, null=True, verbose_name='Index', max_length=255)),
                ('model_code', models.TextField(editable=False, blank=True, null=True, verbose_name='Model code')),
                ('view_code', models.TextField(editable=False, blank=True, null=True, verbose_name='View code')),
                ('urls_code', models.TextField(editable=False, blank=True, null=True, verbose_name='Urls code')),
                ('doc', models.TextField(editable=False, blank=True, null=True, verbose_name='Doc')),
            ],
            options={
                'verbose_name_plural': 'SChApp',
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name': 'SChApp',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SChAppMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('url', models.CharField(max_length=255, verbose_name='Url')),
                ('url_type', models.CharField(default='-', null=True, verbose_name='Url type', choices=[('Default', '-'), ('shtml', 'shtml'), ('panel', 'panel')], blank=True, max_length=16)),
                ('perms', models.CharField(blank=True, null=True, verbose_name='Perms', max_length=255)),
                ('icon', models.CharField(max_length=255, verbose_name='Icon')),
                ('icon_size', models.CharField(default='1', max_length=1, verbose_name='Icon size', choices=[('0', 'small'), ('1', 'medium'), ('2', 'large')])),
                ('parent', schserw.schsys.initdjango.HiddenForeignKey(verbose_name='Parent', to='schbuilder.SChApp')),
            ],
            options={
                'verbose_name_plural': 'SChAppMenu',
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name': 'SChAppMenu',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SChAppSet',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('ext_apps', models.CharField(blank=True, null=True, verbose_name='Extern applications', max_length=255)),
                ('plugins', models.CharField(blank=True, null=True, verbose_name='Plugins', max_length=255)),
                ('gui_type', models.CharField(max_length=32, verbose_name='Gui type', choices=[('standard', 'standard'), ('modern', 'modern'), ('tree', 'tree'), ('tray', 'tray'), ('dialog', 'dialog'), ('one_form', 'one_form')])),
                ('gui_elements', models.CharField(blank=True, null=True, verbose_name='Gui elements', max_length=255)),
                ('is_hybrid', models.BooleanField(verbose_name='Is hybrid', default=False)),
                ('start_page', models.CharField(blank=True, null=True, verbose_name='Start page', max_length=255)),
                ('user_app_template', models.TextField(editable=False, blank=True, null=True, verbose_name='User application template')),
                ('doc', models.TextField(editable=False, blank=True, null=True, verbose_name='Doc')),
            ],
            options={
                'verbose_name_plural': 'SChAppSet',
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name': 'SChAppSet',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SChChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('verbose_name', models.CharField(max_length=255, verbose_name='Verbose name')),
                ('parent', schserw.schsys.initdjango.HiddenForeignKey(verbose_name='Parent', to='schbuilder.SChApp')),
            ],
            options={
                'verbose_name_plural': 'SChChoice',
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name': 'SChChoice',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SChChoiceItem',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('value', models.CharField(max_length=255, verbose_name='Value')),
                ('parent', schserw.schsys.initdjango.HiddenForeignKey(verbose_name='Parent', to='schbuilder.SChChoice')),
            ],
            options={
                'verbose_name_plural': 'SChChoiceItem',
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name': 'SChChoiceItem',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SChField',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, null=True, verbose_name='Name', max_length=255)),
                ('description', models.CharField(blank=True, null=True, verbose_name='Description', max_length=255)),
                ('type', models.CharField(max_length=64, verbose_name='Type', choices=[('AutoField', 'AutoField'), ('BooleanField', 'BooleanField'), ('CharField', 'CharField'), ('CommaSeparatedIntegerField', 'CommaSeparatedIntegerField'), ('DateField', 'DateField'), ('DateTimeField', 'DateTimeField'), ('DecimalField', 'DecimalField'), ('EmailField', 'EmailField'), ('FileField', 'FileField'), ('FilePathField', 'FilePathField'), ('FloatField', 'FloatField'), ('ImageField', 'ImageField'), ('IntegerField', 'IntegerField'), ('IPAddressField', 'IPAddressField'), ('NullBooleanField', 'NullBooleanField'), ('PositiveIntegerField', 'PositiveIntegerField'), ('PositiveSmallIntegerField', 'PositiveSmallIntegerField'), ('SlugField', 'SlugField'), ('SmallIntegerField', 'SmallIntegerField'), ('TextField', 'TextField'), ('TimeField', 'TimeField'), ('URLField', 'URLField'), ('XMLField', 'XMLField'), ('ForeignKey', 'ForeignKey'), ('GForeignKey', 'GenericForeignKey'), ('ManyToManyField', 'ManyToManyField'), ('GManyToManyField', 'GenericManyToManyField'), ('HiddenForeignKey', 'HiddenForeignKey'), ('GHiddenForeignKey', 'GenericHiddenForeignKey'), ('UserField', 'UserField'), ('ForeignKeyWidthIcon', 'ForeignKeyWidthIcon'), ('ManyToManyFieldWidthIcon', 'ManyToManyFieldWidthIcon'), ('AutocompleteTextField', 'AutocompleteTextField'), ('ForeignKeyExt', 'ForeignKeyExt'), ('TreeForeignKey', 'TreeForeignKey'), ('GTreeForeignKey', 'GTreeForeignKey')])),
                ('null', models.BooleanField(verbose_name='Null', default=False)),
                ('blank', models.BooleanField(verbose_name='Blank', default=False)),
                ('editable', models.BooleanField(verbose_name='Editable', default=False)),
                ('unique', models.BooleanField(verbose_name='Unique', default=False)),
                ('db_index', models.BooleanField(verbose_name='DB index', default=False)),
                ('default', models.CharField(blank=True, null=True, verbose_name='Default', max_length=255)),
                ('help_text', models.CharField(blank=True, null=True, verbose_name='Help text', max_length=255)),
                ('choices', models.CharField(blank=True, null=True, verbose_name='Choices', max_length=255)),
                ('rel_to', models.CharField(blank=True, null=True, verbose_name='Relation to', max_length=255)),
                ('param', models.CharField(blank=True, null=True, verbose_name='Param', max_length=255)),
                ('url_params', models.CharField(blank=True, null=True, verbose_name='Url params', max_length=255)),
            ],
            options={
                'verbose_name_plural': 'SChField',
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name': 'SChField',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SChForm',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('module', models.CharField(blank=True, null=True, verbose_name='Module', max_length=64)),
                ('process_code', models.TextField(blank=True, null=True, verbose_name='Process code')),
                ('end_class_code', models.TextField(blank=True, null=True, verbose_name='End class code')),
                ('end_code', models.TextField(blank=True, null=True, verbose_name='End code')),
                ('doc', models.TextField(blank=True, null=True, verbose_name='Doc')),
                ('parent', schserw.schsys.initdjango.HiddenForeignKey(verbose_name='Parent', to='schbuilder.SChApp')),
            ],
            options={
                'verbose_name_plural': 'Form',
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name': 'Form',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SChFormField',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('type', models.CharField(max_length=64, verbose_name='Type', choices=[('BooleanField', 'BooleanField'), ('CharField', 'CharField'), ('ChoiceField', 'ChoiceField'), ('TypedChoiceField', 'TypedChoiceField'), ('DateField', 'DateField'), ('DateTimeField', 'DateTimeField'), ('DecimalField', 'DecimalField'), ('EmailField', 'EmailField'), ('FileField', 'FileField'), ('FilePathField', 'FilePathField'), ('FloatField', 'FloatField'), ('ImageField', 'ImageField'), ('IntegerField', 'IntegerField'), ('IPAddressField', 'IPAddressField'), ('GenericIPAddressField', 'GenericIPAddressField'), ('MultipleChoiceField', 'MultipleChoiceField'), ('TypedMultipleChoiceField', 'TypedMultipleChoiceField'), ('NullBooleanField', 'NullBooleanField'), ('RegexField', 'RegexField'), ('SlugField', 'SlugField'), ('TimeField', 'TimeField'), ('URLField', 'URLField'), ('UserField', 'UserField')])),
                ('required', models.NullBooleanField(verbose_name='Required')),
                ('label', models.CharField(max_length=64, verbose_name='Label')),
                ('initial', models.CharField(blank=True, null=True, verbose_name='Initial', max_length=64)),
                ('widget', models.CharField(blank=True, null=True, verbose_name='Widget', max_length=64)),
                ('help_text', models.CharField(blank=True, null=True, verbose_name='Help text', max_length=64)),
                ('error_messages', models.CharField(blank=True, null=True, verbose_name='Error messages', max_length=64)),
                ('param', models.CharField(blank=True, null=True, verbose_name='Param', max_length=64)),
                ('parent', schserw.schsys.initdjango.HiddenForeignKey(verbose_name='Parent', to='schbuilder.SChForm')),
            ],
            options={
                'verbose_name_plural': 'Form field',
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name': 'Form field',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SChTable',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('base_table', models.CharField(blank=True, null=True, verbose_name='Base table', max_length=255)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('verbose_name', models.CharField(max_length=255, verbose_name='Verbose name')),
                ('verbose_name_plural', models.CharField(max_length=255, verbose_name='Verbose name plural')),
                ('metaclass_code', models.TextField(editable=False, blank=True, null=True, verbose_name='Metaclass code')),
                ('table_code', models.TextField(editable=False, blank=True, null=True, verbose_name='Table code')),
                ('doc', models.TextField(editable=False, blank=True, null=True, verbose_name='Doc')),
                ('generic', models.BooleanField(verbose_name='Generic', default=False)),
                ('url_params', models.CharField(blank=True, null=True, verbose_name='Url params', max_length=255)),
                ('parent', schserw.schsys.initdjango.HiddenForeignKey(verbose_name='Parent', to='schbuilder.SChApp')),
            ],
            options={
                'verbose_name_plural': 'SChTable',
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name': 'SChTable',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SChTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('direct_to_template', models.NullBooleanField(verbose_name='Direct to template')),
                ('url', models.CharField(blank=True, null=True, verbose_name='Url', max_length=64)),
                ('url_parm', models.CharField(blank=True, null=True, verbose_name='Parameters passed to the template', max_length=128)),
                ('template_code', models.TextField(editable=False, blank=True, null=True, verbose_name='Template code')),
                ('parent', schserw.schsys.initdjango.HiddenForeignKey(verbose_name='Parent', to='schbuilder.SChApp')),
            ],
            options={
                'verbose_name_plural': 'SChTemplate',
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name': 'SChTemplate',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SChUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('reg_expr', models.CharField(max_length=255, verbose_name='Regular expression')),
                ('callback_fun', models.CharField(max_length=64, verbose_name='Callback function')),
                ('dictionary', models.CharField(blank=True, null=True, verbose_name='Dictionary', max_length=255)),
                ('name', models.CharField(blank=True, null=True, verbose_name='Name', max_length=64)),
                ('parent', schserw.schsys.initdjango.HiddenForeignKey(verbose_name='Parent', to='schbuilder.SChApp')),
            ],
            options={
                'verbose_name_plural': 'SChUrl',
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name': 'SChUrl',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SChView',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('view_type', models.CharField(max_length=1, verbose_name='View type', choices=[('t', 'Table action'), ('r', 'Row action'), ('u', 'View')])),
                ('param', models.CharField(blank=True, null=True, verbose_name='Param', max_length=255)),
                ('url', models.CharField(blank=True, null=True, verbose_name='Url', max_length=255)),
                ('view_code', models.TextField(editable=False, blank=True, null=True, verbose_name='View code')),
                ('doc', models.TextField(editable=False, blank=True, null=True, verbose_name='Doc')),
                ('url_params', models.CharField(blank=True, null=True, verbose_name='Url params', max_length=255)),
                ('ret_type', models.CharField(default='U', max_length=1, verbose_name='Return value type', choices=[('T', 'Template'), ('O', 'Odf'), ('P', 'Pdf'), ('J', 'Json'), ('X', 'Xml'), ('U', 'User defined')])),
                ('parent', schserw.schsys.initdjango.HiddenForeignKey(verbose_name='Parent', to='schbuilder.SChApp')),
            ],
            options={
                'verbose_name_plural': 'SChView',
                'default_permissions': ('add', 'change', 'delete', 'list'),
                'verbose_name': 'SChView',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='schfield',
            name='parent',
            field=schserw.schsys.initdjango.HiddenForeignKey(verbose_name='Parent', to='schbuilder.SChTable'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='schapp',
            name='parent',
            field=models.ForeignKey(verbose_name='Parent', to='schbuilder.SChAppSet'),
            preserve_default=True,
        ),
    ]
