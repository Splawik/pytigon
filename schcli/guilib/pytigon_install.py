import wx

try:
    from wx.adv import Wizard, WizardPageSimple
except:
    from wx.wizard import Wizard, WizardPageSimple

import zipfile
import os
import sys
import datetime
from shutil import move
import configparser

from subprocess import call
#, Popen, PIPE

from django.conf import settings

from schlib.schfs.vfstools import extractall
from schcli.guilib.tools import create_desktop_shortcut
_ = wx.GetTranslation

def make_page_title(wiz_pg, title):
    sizer = wx.BoxSizer(wx.VERTICAL)
    wiz_pg.SetSizer(sizer)
    title = wx.StaticText(wiz_pg, -1, title)
    title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
    sizer.Add(title, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
    sizer.Add(wx.StaticLine(wiz_pg, -1), 0, wx.EXPAND | wx.ALL, 5)
    return sizer


class TitledPage(WizardPageSimple):

    def __init__(self,parent,lp,title):
        WizardPageSimple.__init__(self, parent)
        self.sizer = make_page_title(self, title)
        self.lp = lp


class InstallWizard(Wizard):

    def __init__(self,file_name,zip_file,app_name,licence_txt,readme_txt):

        Wizard.__init__(self, None, -1, 'Install app')
        self.Bind(wx.adv.EVT_WIZARD_PAGE_CHANGING, self.on_wiz_page_changing)
        self.zip_file = zip_file
        self.app_name = app_name
        page1 = TitledPage(self, 1, _('Program description'))
        self.page1 = page1
        page2 = TitledPage(self, 2, _('License'))
        page3 = TitledPage(self, 3, _('Run'))

        r_txt = wx.TextCtrl(page1, -1, size=wx.Size(600, 300),
                            style=wx.TE_MULTILINE | wx.TE_READONLY)
        r_txt.SetValue(readme_txt)
        page1.sizer.Add(r_txt)
        self.FitToPage(page1)
        l_txt = wx.TextCtrl(page2, -1, licence_txt, size=wx.Size(600, 300),
                            style=wx.TE_MULTILINE | wx.TE_READONLY)
        page2.sizer.Add(l_txt)
        page2.sizer.AddSpacer(5)
        self.licence = wx.CheckBox(page2, -1, _('Accept'))
        page2.sizer.Add(self.licence)
        page3.sizer.Add(wx.StaticText(page3, -1, _('Run the installed program or cancel')))
        WizardPageSimple.Chain(page1, page2)
        WizardPageSimple.Chain(page2, page3)
        self.GetPageAreaSizer().Add(page1)

    def run(self):
        ret = self.RunWizard(self.page1)
        wx.CallAfter(self.Destroy)
        return ret

    def on_wiz_page_changing(self, event):
        if event.GetPage().lp == 2 and event.GetDirection():
            value = self.licence.GetValue()
            if not value:
                wx.MessageBox(_('You must accept the license or cancel the installation!')
                              , _('Installation'))
                event.Veto()
                return
            else:
                if self.install():
                    return
                else:
                    wx.MessageBox(_('Installation error!'), _('Installation'))
                    event.Veto()
                    return
        if event.GetPage().lp == 3 and not event.GetDirection():
            wx.MessageBox(_('Program installed, use the uninstaller!')
                          , _('Installation'))
            event.Veto()
            return
        event.Skip()

    def install(self):
        test_update = True

        extract_to = os.path.join(settings.APP_PACK_PATH, self.app_name)

        if not os.path.exists(settings.APP_PACK_PATH):
            os.mkdir(settings.APP_PACK_PATH)
        if not os.path.exists(extract_to):
            os.mkdir(extract_to)
            test_update = False

        zipname = datetime.datetime.now().isoformat('_')[:19].replace(':','').replace('-','')
        zipname2 = os.path.join(extract_to, zipname+".zip")
        if test_update:
            backup_zip = zipfile.ZipFile(zipname2, 'a')
            exclude = ['.*settings_local.py.*',]
        else:
            backup_zip = None
            exclude = None
        extractall(self.zip_file, extract_to, backup_zip=backup_zip, exclude=exclude, backup_exts=['py', 'txt', 'wsgi', 'ihtml', 'htlm', 'css', 'js',])
        if backup_zip:
            backup_zip.close()
        self.zip_file.close()


        src_db = os.path.join(extract_to, self.app_name+".db")
        if os.path.exists(src_db):
            dest_path_db = os.path.join(settings.DATA_PATH, self.app_name)

            if not os.path.exists(settings.DATA_PATH):
                os.mkdir(settings.DATA_PATH)
            if not os.path.exists(dest_path_db):
                os.mkdir(dest_path_db)
            dest_db = os.path.join(dest_path_db,self.app_name+".db")
            if not os.path.exists(dest_db):
                move(src_db, os.path.join(dest_path_db,self.app_name+".new") )
            else:
                os.rename(dest_db, os.path.join(dest_path_db,self.app_name+".old"))

            call([sys.executable, os.path.join(extract_to, 'manage.py'), 'install'])

        ini_file = os.path.join(extract_to, "install.ini")
        created = False
        if os.path.exists(ini_file):
            config = configparser.ConfigParser()
            config.read(ini_file)
            if 'INSTALL' in config.sections():
                install = config['INSTALL']
                title = install.get('Title', self.app_name)
                parameters = install.get('Parameters', '')
                create_desktop_shortcut(self.app_name, title, parameters)

        if not created:
            create_desktop_shortcut(self.app_name, self.app_name)

        return True


def install(pti, app_name):
    try:
        zip_file = zipfile.ZipFile(str(pti))
        l = zip_file.open('LICENSE.txt')
        licence_txt = l.read().decode('utf-8')
        l.close()
        r = zip_file.open('README.txt')
        readme_txt = r.read().decode('utf-8')
        r.close()
        wizard2 = InstallWizard(pti, zip_file, app_name, licence_txt, readme_txt)
        if wizard2.run():
            return True
        else:
            return False
    except:
        wx.MessageBox(_('Installation error!'), _('Installation'))
        return False
