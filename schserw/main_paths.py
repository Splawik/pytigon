import sys
import tempfile
import os
from os import environ

def get_main_paths():
    ret = {}
    ret['SERW_PATH'] = os.path.dirname(os.path.abspath(__file__))
    ret['ROOT_PATH'] = os.path.abspath(os.path.join(ret['SERW_PATH'], '..'))

    sys.path.append(ret['SERW_PATH'])
    sys.path.append(ret['ROOT_PATH'])
    sys.path.append(os.path.join(ret['ROOT_PATH'], 'ext_lib'))
    sys.path.append(os.path.join(ret['ROOT_PATH'], 'schappdata/schplugins'))

    from schlib.schtools.platform_info import platform_name

    if platform_name()=='Android':
        p1 = p2 = None
        if 'SECONDARY_STORAGE' in environ:
            p1 = os.path.join(environ['SECONDARY_STORAGE'], "pytigon_data")
        if 'EXTERNAL_STORAGE' in environ:
            p2 = os.path.join(environ['EXTERNAL_STORAGE'], "pytigon_data")
        if p1:
            if os.path.exists(p2):
                ret['DATA_PATH'] = p2
            else:
                ret['DATA_PATH'] = p1
        else:
            ret['DATA_PATH'] = p2
        ret['LOG_PATH'] = ret['DATA_PATH']
    else:
        if ret['ROOT_PATH'].startswith('/var/www'):
            ret['DATA_PATH'] = "/home/www-data/.pytigon"
            ret['LOG_PATH'] = "/var/log"
        else:
            ret['DATA_PATH'] = os.path.join(os.path.expanduser("~"), ".pytigon")
            ret['LOG_PATH'] = ret['DATA_PATH']

    ret['TEMP_PATH'] = tempfile.gettempdir()

    if platform_name()=='Android' or 'PYTIGON_APP_IMAGE' in environ:
        ret['APP_PACK_PATH'] = os.path.join(os.path.join(os.path.join(ret['DATA_PATH'], '..'), 'pytigon'), 'app_pack')
    else:
        ret['APP_PACK_PATH'] = os.path.join(ret['ROOT_PATH'], 'app_pack')

    return ret