# -*- coding: utf-8 -*-

import django
from django.db import models

from pytigon_lib.schdjangoext.fields import *
from pytigon_lib.schdjangoext.models import *

import pytigon_lib.schdjangoext.fields as ext_models

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

import os, os.path
import sys
from pytigon_lib.schhtml.htmltools import superstrip


from schauth.models import *

from standard_components.models import *



import os.path
from pytigon_lib.schhtml.htmltools import superstrip
import inspect
from pytigon_lib.schfs.vfstools import norm_path
from django.template import engines
import pytigon

field_default = {'null':False,'blank':False,'editable':True,}
field_defaults = {
    'AutoField': { },
    'BooleanField': { "default": False },
    'CharField': {"param":"max_length=64", "unique": False,},
    'CommaSeparatedIntegerField': {},
    'DateField': {},
    'DateTimeField': {},
    'DecimalField': {},
    'EmailField': {},
    'FileField': { "param": "upload_to='upload/'", },
    'FilePathField': {},
    'FloatField': {},
    'ImageField': {},
    'IntegerField': {},
    'GenericIPAddressField': {},
    'NullBooleanField': {},
    'PositiveIntegerField': {},
    'PositiveSmallIntegerField': {},
    'SlugField': {},
    'SmallIntegerField': {},
    'TextField': { 'editable': False, },
    'TimeField': {},
    'URLField': {},
    'XMLField': {},
    'ForeignKey': { 'name': 'parent', 'description': 'Parent'},
    'ManyToManyField': { },
    'HiddenForeignKey': { 'name': 'parent', 'description': 'Parent' },
    'GForeignKey': { 'name': 'parent', 'description': 'Parent' },
    'GManyToManyField': {},
    'GHiddenForeignKey': { 'name': 'parent', 'description': 'Parent', },
}

formfield_default = {'required':True, }

formfield_defaults = {
    'CharField': { 'param': "max_length=None, min_length=None", },
    'ChoiceField': { 'param': "choices=models.[[choice_name]]", },
    'TypedChoiceField': { 'param': "coerce=,empty_value=''", },
    'DecimalField': { 'param': "max_value=None, min_value=None, max_digits=None, decimal_places=None", },
    'FilePathField': { 'param': "path=[[path]], match=None, recursive=False, allow_files=True, allow_folders=False", },
    'FloatField': { 'param': "max_value=None, min_value=None", },
    'IntegerField': { 'param': "max_value=None, min_value=None", },
    'GenericIPAddressField': { 'param': "protocol='both', unpack_ipv4=False", },
    'MultipleChoiceField': { 'param': "choices=models.[[choice_name]]", },
    'TypedMultipleChoiceField': { 'param': "coerce=,empty_value=''", },
    'RegexField': {'param': "regex='[[regex]]', max_length=None, min_length=None", },
    'URLField': { 'param': "max_length=None, min_length=None", },
    'ComboField': { 'param': "fields=[[fields]]", },    
}


widgets = [
    "ok_cancel",
    "button '[[url]]' '[[description]]' '[[name]]' '[[target]]'"
    "action_table '[[action]]' '[[description]]' '[[name]]' '[[target]]'",
    "print_table '[[description]]' '[[target]]'",
    "new_row '[[description]]' '[[target]]'",
    "edit_row '[[description]]' '[[target]]'",
    "view_row '[[description]]' '[[dx]]' '[[dy]]' , '[[target]]'",
    "print_row '[[description]]' '[[target]]'",
    "action_row '[[action]]' '[[description]]' '[[name]]' '[[target]]'",
    "delete_row '[[description]]' '[[target]]'",
    "list_field '[[field]]' '[[name]]' '[[description]]' '[[target]]'"
    "edit_field '[[field]]' '[[name]]' '[[description]]' '[[target]]'"
    "action_field '[[field]]' '[[action]]' '[[description]]' '[[name]]' '[[target]]'",
    "jscript_link '[[href]]'",
    "css_link '[[href]]'",
    ]
    
    
def apppack():
    ret = []
    for ff in os.listdir(settings.PRJ_PATH):
        if os.path.isdir(os.path.join(settings.PRJ_PATH, ff)):
            if not ff.startswith('_'):
                ret.append([ff, ff])
    return ret




Field_CHOICES = (
    ("AutoField","AutoField"),
    ("BooleanField","BooleanField"),
    ("CharField","CharField"),
    ("CommaSeparatedIntegerField","CommaSeparatedIntegerField"),
    ("DateField","DateField"),
    ("DateTimeField","DateTimeField"),
    ("DecimalField","DecimalField"),
    ("EmailField","EmailField"),
    ("FileField","FileField"),
    ("FilePathField","FilePathField"),
    ("FloatField","FloatField"),
    ("ImageField","ImageField"),
    ("IntegerField","IntegerField"),
    ("GenericIPAddressField","GenericIPAddressField"),
    ("NullBooleanField","NullBooleanField!"),
    ("PositiveIntegerField","PositiveIntegerField"),
    ("PositiveSmallIntegerField","PositiveSmallIntegerField"),
    ("SlugField","SlugField"),
    ("SmallIntegerField","SmallIntegerField"),
    ("TextField","TextField"),
    ("TimeField","TimeField"),
    ("URLField","URLField"),
    ("XMLField","XMLField"),
    ("ForeignKey","ForeignKey"),
    ("GForeignKey","GenericForeignKey!"),
    ("ManyToManyField","ManyToManyField"),
    ("GManyToManyField","GenericManyToManyField!"),
    ("HiddenForeignKey","HiddenForeignKey"),
    ("GHiddenForeignKey","GenericHiddenForeignKey!"),
    ("UserField","UserField"),
    ("ForeignKeyWidthIcon","ForeignKeyWidthIcon!"),
    ("ManyToManyFieldWidthIcon","ManyToManyFieldWidthIcon!"),
    ("AutocompleteTextField","AutocompleteTextField!"),
    ("ForeignKeyExt","ForeignKeyExt!"),
    ("TreeForeignKey","TreeForeignKey!"),
    ("GTreeForeignKey","GTreeForeignKey!"),
    
    )

Gui_CHOICES = (
    ("standard","standard"),
    ("modern","modern"),
    ("tree","tree"),
    ("tray","tray"),
    ("dialog","dialog"),
    ("one_form","one_form"),
    
    )

IconSize_CHOICES = (
    ("0","small"),
    ("1","medium"),
    ("2","large"),
    
    )

View_CHOICES = (
    ("t","Table action"),
    ("r","Row action"),
    ("u","View"),
    
    )

Url_CHOICES = (
    ("Default","-"),
    ("desktop","desktop"),
    ("panel","panel"),
    ("header","header"),
    ("footer","footer"),
    ("script","script"),
    ("pscript","pscript"),
    ("browser","browser"),
    ("browser_panel","prowser_panel"),
    ("browser_header","browser_header"),
    ("browser_footer","browser_footer"),
    
    )

FormField_CHOICES = (
    ("BooleanField","BooleanField"),
    ("CharField","CharField"),
    ("ChoiceField","ChoiceField"),
    ("TypedChoiceField","TypedChoiceField"),
    ("DateField","DateField"),
    ("DateTimeField","DateTimeField"),
    ("DecimalField","DecimalField"),
    ("EmailField","EmailField"),
    ("FileField","FileField"),
    ("FilePathField","FilePathField"),
    ("FloatField","FloatField"),
    ("ImageField","ImageField"),
    ("IntegerField","IntegerField"),
    ("IPAddressField","IPAddressField"),
    ("GenericIPAddressField","GenericIPAddressField"),
    ("MultipleChoiceField","MultipleChoiceField"),
    ("TypedMultipleChoiceField","TypedMultipleChoiceField"),
    ("NullBooleanField","NullBooleanField"),
    ("RegexField","RegexField"),
    ("TimeField","TimeField"),
    ("URLField","URLField"),
    ("UserField","UserField"),
    
    )

ViewRetType_CHOICES = (
    ("T","Template"),
    ("O","Odf"),
    ("P","Pdf"),
    ("J","Json"),
    ("X","Xml"),
    ("U","User defined"),
    
    )

HtmlGui_CHOICES = (
    ("auto","auto"),
    ("desktop_standard","desktop_standard"),
    ("desktop_modern","desktop_modern"),
    ("desktop_traditional","desktop_traditional"),
    ("tablet_standard","tablet_standard"),
    ("tablet_modern","tablet_modern"),
    ("tablet_traditional","tablet_traditional"),
    ("smartfon_standard","smartfon_standard"),
    ("smartfon_modern","smartfon_modern"),
    ("smartfon_traditional","smartfon_traditional"),
    
    )

ContentType_CHOICES = (
    ("pythonjs","pythonjs"),
    ("react_pjsx","react_pjsx"),
    ("css","css"),
    ("js","js"),
    
    )

Static_CHOICES = (
    ("C","css (included in desktop.html)"),
    ("J","javascript (included in desktop.html)"),
    ("P","python to javascript (included in desktop.html)"),
    ("R","vue.js component (included in desktop.html)"),
    ("I","sass to css (included in desktop.html)"),
    ("U","custom file (embeded translation for .pyj, .vue, .sass)"),
    ("G","Vue globals"),
    
    )

FileType_CHOICES = (
    ("f","TemplateFilters"),
    ("t","TemplateTags"),
    ("c","Custom file"),
    ("m","Management command"),
    ("p","Plugin code"),
    ("i","Plugin template"),
    ("l","Library code"),
    ("C","Library c code"),
    ("x","Library cython code"),
    ("s","GraphQL schema"),
    
    )

Consumer_CHOICES = (
    ("WebsocketConsumer","WebsocketConsumer"),
    ("AsyncWebsocketConsumer","AsyncWebsocketConsumer"),
    ("JsonWebsocketConsumer","JsonWebsocketConsumer"),
    ("AsyncJsonWebsocketConsumer","AsyncJsonWebsocketConsumer"),
    ("AsyncHttpConsumer","AsyncHttpConsumer"),
    ("AsyncConsumer","AsyncConsumer"),
    ("SyncConsumer","SyncConsumer"),
    
    )




class SChAppSet( models.Model):
    
    class Meta:
        verbose_name = _("Application package")
        verbose_name_plural = _("Application packages")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schbuilder'


        ordering = ['id']
        
        
    

    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=64)
    title = models.CharField('Title', null=False, blank=False, editable=True, max_length=255)
    ext_apps = models.CharField('Extern applications', null=True, blank=True, editable=True, max_length=4096)
    plugins = models.CharField('Plugins', null=True, blank=True, editable=True, max_length=4096)
    gui_type = models.CharField('Gui type', null=False, blank=False, editable=True, choices=Gui_CHOICES,max_length=32)
    gui_elements = models.CharField('Gui elements', null=True, blank=True, editable=True, max_length=1024)
    login_required = ext_models.NullBooleanField('Login required', null=True, blank=True, editable=True, default=False,)
    public = ext_models.NullBooleanField('Public', null=True, blank=True, editable=True, default=False,)
    main = ext_models.NullBooleanField('Main project', null=True, blank=True, editable=True, default=False,)
    start_page = models.CharField('Start page', null=True, blank=True, editable=True, max_length=255)
    user_app_template = models.TextField('User application template', null=True, blank=True, editable=False, )
    app_main = models.TextField('Main application entrypoint', null=True, blank=True, editable=False, )
    doc = models.TextField('Doc', null=True, blank=True, editable=False, )
    desktop_gui_type = models.CharField('Gui type for pc web browser', null=False, blank=False, editable=True, default='auto',choices=HtmlGui_CHOICES,max_length=32)
    smartfon_gui_type = models.CharField('Gui type for smartfon', null=False, blank=False, editable=True, default='auto',choices=HtmlGui_CHOICES,max_length=32)
    tablet_gui_type = models.CharField('Gui type for tablet', null=False, blank=False, editable=True, default='auto',choices=HtmlGui_CHOICES,max_length=32)
    user_param = models.TextField('User parameter', null=True, blank=True, editable=True, )
    custom_tags = models.TextField('Custom tags', null=True, blank=True, editable=True, )
    readme_file = models.TextField('readme.txt', null=True, blank=True, editable=False, )
    license_file = models.TextField('license.txt', null=True, blank=True, editable=False, )
    install_file = models.TextField('install.ini', null=True, blank=True, editable=False, )
    encoded_zip = models.TextField('Encoded zip file', null=True, blank=True, editable=False, )
    

    def get_ext_apps(self, tab=None):
        if tab:
            ret = tab
        else:
            ret = []
        if self.ext_apps:
            #if self.ext_apps == '*':
            #    appset_list = SChAppSet.objects.all()
            #    for pos in appset_list:
            #        if pos.name == self.name or not pos.public:
            #            continue
            #        app_list = pos.schapp_set.all()
            #        for pos2 in app_list:
            #            name = pos.name+"."+pos2.name
            #            if not name in ret:
            #                ret.append(name)
            #    return ret
            #else:
            l=self.ext_apps.split(',')
        else:
            return ret
        for a in l:
            if a !='':
                if not a in ret:
                    ret.append(a)
        return ret
    
    def get_ext_apps_without_pack(self):
        ret = []
        if self.ext_apps:
            l=self.ext_apps.split(',')
            for a in l:
                if a !='':
                    if '.' in a:
                        ret.append(a.split('.')[1])
                    else:
                        ret.append(a)
        return ret
    
    def get_ext_modules(self):
        ret = []
        if self.ext_apps:
            l=self.ext_apps.split(',')
            for a in l:
                elms=a.split('.')
                if len(elms)>1:
                    module=elms[-2]
                    ret.append(module)
        return ret
    
    
    def __str__(self):
        return self.name
    
    @classmethod
    def table_action(cls, list_view, request, data):
        return standard_table_action(cls, list_view, request, data, ['copy', 'paste'])
    
        
    
admin.site.register(SChAppSet)


class SChApp( models.Model):
    
    class Meta:
        verbose_name = _("SChApp")
        verbose_name_plural = _("SChApp")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schbuilder'


        ordering = ['id']
        
        
    

    parent = ext_models.ForeignKey(SChAppSet, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=255)
    module_title = models.CharField('Module title', null=True, blank=True, editable=True, max_length=32)
    title = models.CharField('Title', null=True, blank=True, editable=True, max_length=255)
    perms = models.BooleanField('Perms', null=False, blank=False, editable=True, default=False,)
    index = models.CharField('Index', null=True, blank=True, editable=True, max_length=255)
    model_code = models.TextField('Model code', null=True, blank=True, editable=False, )
    view_code = models.TextField('View code', null=True, blank=True, editable=False, )
    urls_code = models.TextField('Urls code', null=True, blank=True, editable=False, )
    tasks_code = models.TextField('Tasks code', null=True, blank=True, editable=True, )
    consumer_code = models.TextField('Consumer code', null=True, blank=True, editable=True, )
    doc = models.TextField('Doc', null=True, blank=True, editable=False, )
    user_param = models.TextField('Urser parameter', null=True, blank=True, editable=True, )
    

    def get_models(self):
        ret = ["'self'", ]
        for app in self.parent.schapp_set.all():
            for tab in app.schtable_set.all():
                if app.name == self.name:
                    ret.append(tab.name)
                else:
                    ret.append(app.name+"."+tab.name)
        if self.parent.ext_apps:
            ext_apps = self.parent.ext_apps.split(',')
        else:
            ext_apps = []
        if len(ext_apps)>0:
            for ext_app in ext_apps:
                if 'schserw.' in ext_app:
                    try:
                        module = __import__(ext_app+'.models')
                        app = getattr(module,ext_app.split('.')[1])
                        models = getattr(app,'models')
                        for name in dir(models):
                            obj = getattr(models, name)
                            if inspect.isclass(obj):
                                ret.append(ext_app+"."+name)
                    except:
                        pass
            for ext_app in ext_apps:
                if not 'schserw.' in ext_app:
                    try:
                        appset = ext_app.split('.')[0]
                        appname = ext_app.split('.')[1]
                        appsetpath = norm_path(os.path.dirname(__file__)+"/../../"+appset)
                        if not appsetpath in sys.path:
                            sys.path.append(appsetpath)
                        module = __import__(appname+'.models')
                        models = getattr(module,'models')
                        for name in dir(models):
                            obj = getattr(models, name)
                            if inspect.isclass(obj):
                                ret.append(appname+"."+name)
                    except:
                        pass
        return ret
    
    def get_urls(self, main=False):
        ret = []
        for table in self.schtable_set.all():
            if table.generic:
                ret.append('table/' + table.name +"/-/form/list/")
            for field in table.schfield_set.all():
                if field.is_rel():
                    if field.type[0]=='G':
                        if field.name == 'parent' and field.rel_to == "'self'":
                            ret.append('table/'+table.name+"/0/form/tree/")
        for view in self.schview_set.all():
            if view.url and view.url != "":
                if not main:
                    if view.view_type=='r':
                        url = 'table/' +  view.url + "/<<pk>>/action/"+view.name+"/"
                        ret.append(url)
                if view.view_type=='t':
                    url = 'table/' +  view.url + "/action/"+view.name+"/"
                    ret.append(url)
                if view.view_type=='u':
                    if not (main and '?P' in view.url):
                        ret.append(view.url)
        for template in self.schtemplate_set.all():
            if template.direct_to_template:
                ret.append(template.get_url_name())
        #for wiki in Page.objects.all(): 
         #   url = 'schwiki/{{%s}}/{{%s}}/view/' % (wiki.subject, wiki.name)
         #   ret.append(url)             
        for form in self.schform_set.all():
            if not form.name.startswith('_'):
                ret.append('form/' + form.name +"/")
        return ret
    
    def model_code_start(self):
        if self.model_code:
            return self.model_code.split('[[[GEN]]]')[0]
        else:
            return ""
        
    def model_code_end(self):
        if self.model_code:
            x = self.model_code.split('[[[GEN]]]')
            if len(x)>1:
                return x[1]
        return ""
    
    def __str__(self):
        return self.name
    
admin.site.register(SChApp)


class SChChoice( models.Model):
    
    class Meta:
        verbose_name = _("SChChoice")
        verbose_name_plural = _("SChChoice")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schbuilder'


        ordering = ['id']
        
        
    

    parent = ext_models.HiddenForeignKey(SChApp, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=255)
    verbose_name = models.CharField('Verbose name', null=False, blank=False, editable=True, max_length=255)
    

    def __str__(self):
        return self.name
    
admin.site.register(SChChoice)


class SChChoiceItem( models.Model):
    
    class Meta:
        verbose_name = _("SChChoiceItem")
        verbose_name_plural = _("SChChoiceItem")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schbuilder'


        ordering = ['id']
        
        
    

    parent = ext_models.HiddenForeignKey(SChChoice, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=255)
    value = models.CharField('Value', null=False, blank=False, editable=True, max_length=255)
    

    def __str__(self):
        return self.name
    
admin.site.register(SChChoiceItem)


class SChTable( models.Model):
    
    class Meta:
        verbose_name = _("SChTable")
        verbose_name_plural = _("SChTable")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schbuilder'


        ordering = ['id']
        
        
    

    parent = ext_models.HiddenForeignKey(SChApp, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    base_table = models.CharField('Base table', null=True, blank=True, editable=True, max_length=255)
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=255)
    verbose_name = models.CharField('Verbose name', null=False, blank=False, editable=True, max_length=255)
    verbose_name_plural = models.CharField('Verbose name plural', null=False, blank=False, editable=True, max_length=255)
    metaclass_code = models.TextField('Metaclass code', null=True, blank=True, editable=False, )
    table_code = models.TextField('Table code', null=True, blank=True, editable=False, )
    ordering = models.CharField('Ordering', null=True, blank=True, editable=True, default="['id']",max_length=255)
    doc = models.TextField('Doc', null=True, blank=True, editable=False, )
    generic = models.BooleanField('Generic', null=False, blank=False, editable=True, default=False,)
    url_params = models.CharField('Url params', null=True, blank=True, editable=True, max_length=255)
    proxy_model = models.CharField('Proxy model', null=True, blank=True, editable=True, max_length=255)
    

    def get_models(self):
        return self.parent.get_models()
    
    def get_base_table(self):
        l = self.base_table.split('.')
        if len(l)>1 and l[-2]!='models':
            return l[-1]
        else:
            return self.base_table
    
    def __str__(self):
        return self.name
    
admin.site.register(SChTable)


class SChField( models.Model):
    
    class Meta:
        verbose_name = _("SChField")
        verbose_name_plural = _("SChField")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schbuilder'


        ordering = ['id']
        
        
    

    parent = ext_models.HiddenForeignKey(SChTable, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    name = models.CharField('Name', null=True, blank=True, editable=True, max_length=255)
    description = models.CharField('Description', null=True, blank=True, editable=True, max_length=255)
    type = models.CharField('Type', null=False, blank=False, editable=True, choices=Field_CHOICES,max_length=64)
    null = models.BooleanField('Null', null=False, blank=False, editable=True, default=False,)
    blank = models.BooleanField('Blank', null=False, blank=False, editable=True, default=False,)
    editable = models.BooleanField('Editable', null=False, blank=False, editable=True, default=False,)
    unique = models.BooleanField('Unique', null=False, blank=False, editable=True, default=False,)
    db_index = models.BooleanField('DB index', null=False, blank=False, editable=True, default=False,)
    default = models.CharField('Default', null=True, blank=True, editable=True, max_length=255)
    help_text = models.CharField('Help text', null=True, blank=True, editable=True, max_length=255)
    choices = models.CharField('Choices', null=True, blank=True, editable=True, max_length=255)
    rel_to = models.CharField('Relation to', null=True, blank=True, editable=True, max_length=255)
    param = models.CharField('Param', null=True, blank=True, editable=True, max_length=255)
    url_params = models.CharField('Url params', null=True, blank=True, editable=True, max_length=255)
    

    def init_new(self, request, view, param=None):
        if param:
            self.type=param
    
            defaults=self.get_field_defaults()
            defaults['type'] = param
    
            for key in defaults:
                value = getattr(self, key)
                if not value:
                    setattr(self, key, defaults[key])
            return defaults
        else:
            return None
    
    def save(self, force_insert=False, force_update=False):
        super(SChField, self).save(force_insert, force_update)
    
    def __str__(self):
        return self.name
    
    def is_rel(self):
        if 'Key' in self.type or 'Many' in self.type:
            return True
        else:
            return False
    
    def is_generic_rel(self):
        if self.is_rel() and self.type[0]=='G':
            return True
        else:
            return False
     
    def has_choices(self):
        if self.type in ('CharField',):
            return True
        else:
            return False
    
    def get_models(self):
        return self.parent.get_models()
    
    def as_declaration(self):
        #if 'TreeForeignKey' in self.type:
        #    if not self.parent.base_table in ("", "models.Model"):
        #        return ""
        
        if self.type == 'UserField':
            return self.param
        type_desc = dict(Field_CHOICES)[self.type]
        if type_desc.endswith('!'):
            module = "ext_models."
        else:
            module = 'models.'
        if self.is_rel():
            rel_model =self.rel_to.split('.')[-1]
    
            if self.type[0]=='G':
                if 'ForeignKey' in self.type:
                    ret = "%s = %s%s(%s, on_delete=models.CASCADE, null=%s, blank=%s, editable=%s, verbose_name='%s', " % \
                        (self.name, module, self.type[1:], rel_model, self.null, self.blank, self.editable, self.description)
                else:
                    ret = "%s = %s%s(%s, null=%s, blank=%s, editable=%s, verbose_name='%s', " % \
                        (self.name, module, self.type[1:], rel_model, self.null, self.blank, self.editable, self.description)
            else:
                if 'ForeignKey' in self.type:
                    ret = "%s = %s%s(%s, on_delete=models.CASCADE, null=%s, blank=%s, editable=%s, verbose_name='%s', " % \
                        (self.name, module, self.type, rel_model, self.null, self.blank, self.editable, self.description)
                else:
                    ret = "%s = %s%s(%s, null=%s, blank=%s, editable=%s, verbose_name='%s', " % \
                        (self.name, module, self.type, rel_model, self.null, self.blank, self.editable, self.description)
        else:
            ret = "%s = %s%s('%s', null=%s, blank=%s, editable=%s, " % \
                (self.name, module, self.type, self.description, self.null, self.blank, self.editable)
        if self.unique:
            ret+= "unique=%s," % self.unique
        if self.default and len(self.default)>0:
            ret+= "default=%s," % self.default
        if self.help_text and len(self.help_text)>0:
            ret+= "help_text=%s," % self.help_text
        if self.choices:
            ret+="choices=%s," % self.choices
        if self.param and len(self.param)>0:
            ret+= self.param
            #.replace(':','=')
        ret += ")"
        return ret
    
    def get_field_defaults(self):
        ret = field_default.copy()
        if self.type in field_defaults:
            for key, value in field_defaults[self.type].items():
                ret[key]=value
        return ret
    
    def get_rel_to(self):
        if self.rel_to == "'self'":
            return self.parent.name
        else:
            return self.rel_to
            
    def get_relate_set_name(self):
        if self.param and 'related_name' in self.param:
            for pos in self.param.split(','):
                rec=pos.split('=')
                if rec[0].strip()=='related_name':
                    return rec[1].replace("'","").replace("\"","").strip()
        return self.parent.name.lower()+'_set'
        
    @classmethod
    def table_action(cls, list_view, request, data):
        return standard_table_action(cls, list_view, request, data, ['copy', 'paste'])
    
admin.site.register(SChField)


class SChView( models.Model):
    
    class Meta:
        verbose_name = _("SChView")
        verbose_name_plural = _("SChView")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schbuilder'


        ordering = ['id']
        
        
    

    parent = ext_models.HiddenForeignKey(SChApp, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=255)
    view_type = models.CharField('View type', null=False, blank=False, editable=True, choices=View_CHOICES,max_length=1)
    param = models.CharField('Param', null=True, blank=True, editable=True, max_length=255)
    url = models.CharField('Url', null=True, blank=True, editable=True, max_length=255)
    view_code = models.TextField('View code', null=True, blank=True, editable=False, )
    doc = models.TextField('Doc', null=True, blank=True, editable=False, )
    url_params = models.CharField('Url params', null=True, blank=True, editable=True, max_length=255)
    ret_type = models.CharField('Return value type', null=False, blank=False, editable=True, default='U',choices=ViewRetType_CHOICES,max_length=1)
    

    def init_new(self, request, view, param=None):
        if param:
            self.view_type=param
            defaults={}
            defaults['view_type'] = param
            if param=='r':
                self.param = 'pk'
                defaults['param'] = self.param
            if param=='t':
                pass
            if param=='u':
                defaults['param'] = '**argv'
                defaults['url_params'] = '{}'
                defaults['url'] = 'fun/(?P<parm>\d+)/$'
            return defaults
        else:
            return None
    
    def get_name(self):
        if '/' in self.name:
            return self.name.split('/')[-1]
        else:
            return self.name
    
    def get_url(self):
        name = self.get_name()
        if self.view_type == 'u':
            if self.url_params and self.url_params!="":
                return "url('%s', views.%s, %s)" % (self.url, name, self.url_params)
            else:
                return "url('%s', views.%s)" % (self.url, name)
        else:
            if self.view_type == 'r':
                bname='gen_row_action'
            else:
                bname='gen_tab_action'
        
            if self.url_params and self.url_params!="":
                if '#' in self.name:
                    x = self.name.split('#')
                    return "%s('%s', '%s', views.%s, %s)" % (bname, self.url, x[0], x[1], self.url_params)
                else:
                    return "%s('%s', '%s', views.%s, %s)" % (bname, self.url, self.name, name,self.url_params)
            else:
                if '#' in self.name:
                    x = self.name.split('#')
                    return "%s('%s', '%s', views.%s)" % (bname, self.url, x[0], x[1])
                else:
                    return "%s('%s', '%s', views.%s)" % (bname, self.url, self.name, name)
    
    def __str__(self):
        return self.name
    
    def transform_template_name(self, request, template_name):
        if '/view_code/py/editor' in request.path:
            if template_name == 'schsys/db_field_edt.html':
                return 'schbuilder/db_field_edt_mod.html'
        return template_name
    
    def get_models(self):
        return self.parent.get_models()
    
    def clean_url(self):
        return self.url.replace('$', '')
    
admin.site.register(SChView)


class SChStatic( models.Model):
    
    class Meta:
        verbose_name = _("Static file")
        verbose_name_plural = _("Static files")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schbuilder'


        ordering = ['id']
        
        
    

    parent = ext_models.HiddenForeignKey(SChAppSet, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    type = models.CharField('Type', null=False, blank=False, editable=True, choices=Static_CHOICES,max_length=1)
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=64)
    code = models.TextField('Code', null=True, blank=True, editable=False, )
    doc = models.TextField('Doc', null=True, blank=True, editable=False, )
    

    def __str__(self):
        return self.get_type_display() + "/" + self.name
    
admin.site.register(SChStatic)


class SChTemplate( models.Model):
    
    class Meta:
        verbose_name = _("SChTemplate")
        verbose_name_plural = _("SChTemplate")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schbuilder'


        ordering = ['id']
        
        
    

    parent = ext_models.HiddenForeignKey(SChApp, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=255)
    direct_to_template = ext_models.NullBooleanField('Direct to template', null=True, blank=True, editable=True, )
    url = models.CharField('Url', null=True, blank=True, editable=True, max_length=64)
    url_parm = models.CharField('Parameters passed to the template', null=True, blank=True, editable=True, max_length=128)
    template_code = models.TextField('Template code', null=True, blank=True, editable=False, )
    static_files = models.ManyToManyField(SChStatic, null=True, blank=True, editable=True, verbose_name='Static files', )
    tags_mount = models.CharField('Mount component tags', null=True, blank=True, editable=True, max_length=256)
    

    def get_url_name(self):
        if self.url and self.url!="":
            return self.url
        else:
            return self.name
    
    def get_url(self):
        if self.direct_to_template:
            url_name = self.get_url_name()
            app_name = self.parent.name
            template_name = self.name.lower().replace(' ','_')+".html"
            if self.url_parm:
                param = self.url_parm
            else:
                param = ""
            return "url(r'^%s', TemplateView.as_view(template_name='%s/%s'), {%s})" % (url_name, app_name, template_name, param )
        else:
            return None
                
    def _get_table_fields(self, tables):
        ret=[]
        if len(tables)==1:
            table = tables[0]
            for pos in table.schfield_set.all():
                ret.append(pos.name)
            if table.base_table and table.base_table != None:
                ret2 = self._get_table_fields(SChTable.objects.filter(name=table.base_table))
                for pos in ret2:
                    ret.append(pos)
        return ret
    
    def get_table_fields(self):
        return self._get_table_fields(self.parent.schtable_set.filter(parent=self.parent).filter(name=self.name))
    
    def get_table_methods(self):
        ret=[]
        tables = self.parent.schtable_set.filter(parent=self.parent).filter(name=self.name)
        if len(tables)==1:
            table = tables[0]
            if table.table_code:
                for line in table.table_code.split('\n'):
                    if line.startswith('def'):
                        ret.append(line[4:])
        return ret
    
    def get_django_filters(self):
        ret = []
        django_engine = engines['django'].engine
        for pos in django_engine.template_builtins:
            for f in pos.filters:
                ret.append(f)
        return ret
    
    def get_django_tags(self):
        ret = []
        django_engine = engines['django'].engine
        for pos in django_engine.template_builtins:
            for f in pos.tags:
                ret.append(f)
        return ret
    
    def get_blocks(self):
        ret=[]
        form_path = os.path.join(os.path.dirname(pytigon.__file__),"templates", "base0.html")
        f = open(form_path, "rt")
        buf = f.read()
        f.close()
        for line in buf.split('\n'):
            line2 = line.strip()
            if line2.startswith('{% block'):
                ret.append(line2.split(' ',3)[2])
        return ret
    
    def get_template_widgets(self):
        return widgets
    
    def transform_template_name(self, request, template_name):
        if 'template_code/py/editor' in request.path:
            if template_name == 'schsys/db_field_edt.html':
                return 'schbuilder/db_field_edt_template.html'
        return template_name
    
    def __str__(self):
        return self.name
        
    
admin.site.register(SChTemplate)


class SChAppMenu( models.Model):
    
    class Meta:
        verbose_name = _("SChAppMenu")
        verbose_name_plural = _("SChAppMenu")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schbuilder'


        ordering = ['id']
        
        
    

    parent = ext_models.HiddenForeignKey(SChApp, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=255)
    url = models.CharField('Url', null=False, blank=False, editable=True, max_length=255)
    url_type = models.CharField('Url type', null=True, blank=True, editable=True, default='-',choices=Url_CHOICES,max_length=16)
    perms = models.CharField('Perms', null=True, blank=True, editable=True, max_length=255)
    icon = models.CharField('Icon', null=False, blank=False, editable=True, max_length=255)
    icon_size = models.CharField('Icon size', null=False, blank=False, editable=True, default='1',choices=IconSize_CHOICES,max_length=1)
    

    def not_standard_icon_size(self):
        if self.icon_size=='1':
            return False
        else:
            return True
    
    def get_perms(self):
        if self.perms and self.perms!=" ":
            return "'%s'" % self.perms
        else:
            return "None"
    
    def get_main_urls(self):
        return self.parent.get_urls(main=True)
    
    def get_urls(self):
        return self.parent.get_urls(main=False)
    
    def get_url_type_ext(self):
        if self.url_type in [None, '-']:
            return "?schtml=desktop"
        elif self.url_type == 'browser':
            return ''
        else:
            return '?schtml='+self.url_type
    
    def clean_url(self):
        return self.url.replace('$', '')
    
    def __str__(self):
        return self.name
    
admin.site.register(SChAppMenu)


class SChForm( models.Model):
    
    class Meta:
        verbose_name = _("Form")
        verbose_name_plural = _("Form")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schbuilder'


        ordering = ['id']
        
        
    

    parent = ext_models.HiddenForeignKey(SChApp, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=64)
    module = models.CharField('Module', null=True, blank=True, editable=True, max_length=64)
    process_code = models.TextField('Process code', null=True, blank=True, editable=True, )
    end_class_code = models.TextField('End class code', null=True, blank=True, editable=True, )
    end_code = models.TextField('End code', null=True, blank=True, editable=True, )
    doc = models.TextField('Doc', null=True, blank=True, editable=True, )
    

    
admin.site.register(SChForm)


class SChFormField( models.Model):
    
    class Meta:
        verbose_name = _("Form field")
        verbose_name_plural = _("Form field")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schbuilder'


        ordering = ['id']
        
        
    

    parent = ext_models.HiddenForeignKey(SChForm, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=64)
    type = models.CharField('Type', null=False, blank=False, editable=True, choices=FormField_CHOICES,max_length=64)
    required = ext_models.NullBooleanField('Required', null=True, blank=True, editable=True, )
    label = models.CharField('Label', null=False, blank=False, editable=True, max_length=64)
    initial = models.CharField('Initial', null=True, blank=True, editable=True, max_length=256)
    widget = models.CharField('Widget', null=True, blank=True, editable=True, max_length=64)
    help_text = models.CharField('Help text', null=True, blank=True, editable=True, max_length=256)
    error_messages = models.CharField('Error messages', null=True, blank=True, editable=True, max_length=64)
    param = models.CharField('Param', null=True, blank=True, editable=True, max_length=64)
    

    def init_new(self, request, view, param=None):
        if param:
            self.type=param
    
            defaults=self.get_field_defaults()
            defaults['type'] = param
    
            for key in defaults:
                setattr(self, key, defaults[key])
            return defaults
        else:
            return None
    
    def as_declaration(self):
        if self.type == 'UserField':
            return self.param        
        ret = "%s = forms.%s(label=_('%s'), required=%s, " % \
                (self.name, self.type, self.label, self.required)
        if self.initial:
            ret+= "initial=%s," % self.initial
        if self.widget and len(self.widget)>0:
            ret+= "widget=%s," % self.widget
        if self.help_text and len(self.help_text)>0:
            ret+= "help_text=%s," % self.help_text
        if self.error_messages:
            ret+="error_messages=%s," % self.error_messages
        if self.param and len(self.param)>0:
            ret+= self.param
        ret += ")"
        return ret
    
    def get_field_defaults(self):
        ret = formfield_default.copy()
        if self.type in formfield_defaults:
            for key, value in formfield_defaults[self.type].items():
                ret[key]=value
        return ret
    
admin.site.register(SChFormField)


class SChTask( models.Model):
    
    class Meta:
        verbose_name = _("SChTask")
        verbose_name_plural = _("SChTask")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schbuilder'


        ordering = ['id']
        
        
    

    parent = ext_models.HiddenForeignKey(SChApp, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=255)
    code = models.TextField('Code', null=True, blank=True, editable=True, )
    doc = models.TextField('Doc', null=True, blank=True, editable=True, )
    

    def transform_template_name(self, request, template_name):
        if '/code/py/editor' in request.path:
            if template_name == 'schsys/db_field_edt.html':
                return 'schbuilder/db_field_edt_task.html'
        return template_name
    
admin.site.register(SChTask)


class SChFiles( models.Model):
    
    class Meta:
        verbose_name = _("SChFiles")
        verbose_name_plural = _("SChFiles")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schbuilder'


        ordering = ['id']
        
        
    

    parent = ext_models.HiddenForeignKey(SChApp, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    file_type = models.CharField('File  type', null=False, blank=False, editable=True, choices=FileType_CHOICES,max_length=3)
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=256)
    content = models.TextField('Content', null=True, blank=True, editable=False, )
    

    
admin.site.register(SChFiles)


class SChLocale( models.Model):
    
    class Meta:
        verbose_name = _("Locale")
        verbose_name_plural = _("Locales")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schbuilder'


        ordering = ['id']
        
        
    

    parent = ext_models.HiddenForeignKey(SChAppSet, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=16)
    

    
admin.site.register(SChLocale)


class SChTranslate( models.Model):
    
    class Meta:
        verbose_name = _("Translate")
        verbose_name_plural = _("Translate")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schbuilder'


        ordering = ['id']
        
        
    

    parent = ext_models.HiddenForeignKey(SChLocale, on_delete=models.CASCADE, null=False, blank=False, editable=False, verbose_name='Parent', )
    description = models.CharField('Description', null=False, blank=False, editable=True, max_length=1024)
    translation = models.CharField('Translation', null=True, blank=True, editable=True, max_length=1024)
    status = models.CharField('Status', null=True, blank=True, editable=False, max_length=16)
    

    
admin.site.register(SChTranslate)


class SChChannelConsumer( models.Model):
    
    class Meta:
        verbose_name = _("Channel consumer")
        verbose_name_plural = _("Channel consumers")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schbuilder'


        ordering = ['id']
        
        
    

    parent = ext_models.HiddenForeignKey(SChApp, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=255)
    consumer_type = models.CharField('Consumer type', null=False, blank=False, editable=True, choices=Consumer_CHOICES,max_length=64)
    url = models.CharField('Url', null=True, blank=True, editable=True, max_length=255)
    consumer_code = models.TextField('Consumer code', null=True, blank=True, editable=False, )
    doc = models.TextField('Doc', null=True, blank=True, editable=False, )
    

    def init_new(self, request, view, param=None):
        if param:
            self.view_type=param
            defaults={}
            defaults['consumer_type'] = param
            return defaults
        else:
            return None
    
admin.site.register(SChChannelConsumer)




