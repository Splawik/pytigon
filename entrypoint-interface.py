#! /usr/bin/python3
import subprocess
import os
import sys
from os import environ

from schlib.schtools.tools import get_executable

BASE_APPS_PATH = "/var/www/pytigon/app_pack"
sys.path.append(BASE_APPS_PATH)

VIRTUAL_HOST = "localhost"

if 'VIRTUAL_PORT' in environ:
    VIRTUAL_PORT = str(environ['VIRTUAL_PORT'])
else:
    VIRTUAL_PORT = '443'

if 'VIRTUAL_PORT_80' in environ:
    VIRTUAL_PORT_80 = str(environ['VIRTUAL_PORT_80'])
else:
    VIRTUAL_PORT_80 = '80'

if 'PORT_80_REDIRECT' in environ:
    PORT_80_REDIRECT = environ['PORT_80_REDIRECT']
else:
    PORT_80_REDIRECT = None

if 'CERT' in environ:
    x = environ['CERT'].split(';')
    CRT = "ssl_certificate " + x[0] + ";"
    KEY = "ssl_certificate_key " + x[1] + ";"
    VIRTUAL_PORT += " ssl http2"
else:
    CRT = ""
    KEY = ""

START_CLIENT_PORT = 8000

APP_PACKS = []
APP_PACK_FOLDERS = []
MAIN_APP_PACK = None

CFG_OLD = """server {
       listen         %s;
       server_name    %s;
       return         301 %s;
}

"""

CFG_START = """server
{
    listen %s;
    client_max_body_size 20M;
    server_name %s;
    charset utf-8;

    %s
    %s

    location ^~ /static/ {
        alias /var/www/pytigon/static/;
    }
"""

CFG_ELEM = """
    location ^~ /%s/static/ {
        alias /var/www/pytigon/static/;
    }
    location ~ /%s(.*)/socket.io/$ {
        proxy_http_version 1.1;
    
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_pass %s:%d/%s$1/socket.io/;
    }    
    location ~ /%s(.*)$ {
        proxy_pass %s:%d/%s$1$is_args$args;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr$is_args$args;
        proxy_set_header X-Forwarded-For $remote_addr$is_args$args;
    }
"""


CFG_END = """
    location ~ (.*)$ {
        proxy_pass %s:%d$1$is_args$args;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr$is_args$args;
        proxy_set_header X-Forwarded-For $remote_addr$is_args$args;
    }   
}
"""

if not os.path.exists("/var/www/pytigon/app_pack/_schtools"):
    unzip = subprocess.Popen("unzip /var/www/pytigon/install/app_pack.zip -d /var/www/pytigon/app_pack/", shell=True)
    unzip.wait()

def create_sym_links(source_path, dest_path):
    if os.path.exists(source_path) and os.path.exists(dest_path):
        x = os.listdir(source_path)
        for pos in x:
            s_path = os.path.join(source_path, pos)
            d_path = os.path.join(dest_path, pos)
            if not os.path.exists(d_path):
                os.symlink(s_path, d_path)

create_sym_links("/pytigon/app_pack/", "/var/www/pytigon/app_pack/")
create_sym_links("/pytigon/static/app/", "/var/www/pytigon/static/app/")

for ff in os.listdir(BASE_APPS_PATH):
    if os.path.isdir( os.path.join(BASE_APPS_PATH,ff)):
        if not ff.startswith('_'):
            APP_PACK_FOLDERS.append(ff)

for app_pack in APP_PACK_FOLDERS:
    base_apps_pack2 = os.path.join(BASE_APPS_PATH, app_pack)
    try:
        x = __import__(app_pack+".apps")
    except:
        continue
    if hasattr(x.apps, 'PUBLIC') and x.apps.PUBLIC:
        if hasattr(x.apps, 'MAIN_APP_PACK') and x.apps.MAIN_APP_PACK:
            MAIN_APP_PACK = app_pack
        else:
            APP_PACKS.append(app_pack)

if not MAIN_APP_PACK and len(APP_PACKS)==1:
    MAIN_APP_PACK = APP_PACKS[0]
    APP_PACKS = []

with open("/etc/nginx/sites-available/pytigon", "wt") as conf:
    if PORT_80_REDIRECT:
       conf.write(CFG_OLD % (VIRTUAL_PORT_80, VIRTUAL_HOST, PORT_80_REDIRECT))

    conf.write(CFG_START % ( VIRTUAL_PORT, VIRTUAL_HOST, CRT, KEY))
    port = START_CLIENT_PORT
    for app_pack in APP_PACKS:
        conf.write(CFG_ELEM % (app_pack, app_pack, "http://127.0.0.1", port, app_pack, app_pack, "http://127.0.0.1", port, app_pack))
        port += 1
    if MAIN_APP_PACK:
        conf.write(CFG_END % ("http://127.0.0.1", port))

    if MAIN_APP_PACK:
        APP_PACKS.append(MAIN_APP_PACK)

port = START_CLIENT_PORT

ret_tab = []
for app_pack in APP_PACKS:
    #server = f"daphne -b 0.0.0.0 -p {port} --proxy-headers --access-log /var/log/pytigon-access.log asgi:application"

    count = 4 if app_pack == MAIN_APP_PACK else 1

    server = f"gunicorn -b 0.0.0.0:{port} -w {count} -k uvicorn.workers.UvicornWorker --access-logfile /var/log/pytigon-access.log --log-file /var/log/pytigon-err.log asgi:application"
    path = f"/var/www/pytigon/app_pack/{app_pack}"

    cmd = f"cd {path} && exec {server}"

    port += 1
    print(cmd)
    ret_tab.append(subprocess.Popen(cmd, shell=True))

for app_pack in APP_PACKS:
    cmd = "cd /var/www/pytigon && exec %s pytigon_task.py %s" % (get_executable(), app_pack)
    print(cmd)
    ret_tab.append(subprocess.Popen(cmd, shell=True))

restart = subprocess.Popen("nginx -g 'daemon off;'", shell=True)
restart.wait()

for pos in ret_tab:
    pos.wait()

