#! /usr/bin/python3
import subprocess
import os
import sys
from os import environ

BASE_APPS_PATH = "/var/www/pytigon/app_pack"
sys.path.append(BASE_APPS_PATH)

VIRTUAL_HOST = "localhost"

if 'VIRTUAL_PORT' in environ:
    VIRTUAL_PORT = environ['VIRTUAL_PORT']
else:
    VIRTUAL_PORT = 8080

START_CLIENT_PORT = 8000

APP_PACKS = []
APP_PACK_FOLDERS = []
MAIN_APP_PACK = None

CFG_START = """server
{   
    listen %s;
    client_max_body_size 20M;
    server_name %s;

    location ^~ /static/ {
        alias /var/www/pytigon/static/;
    }
    
    location ^~ /schdevtools/static/ {
        alias /var/www/pytigon/static/;
    }
"""

CFG_ELEM = """
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

for ff in os.listdir(BASE_APPS_PATH):
    if os.path.isdir( os.path.join(BASE_APPS_PATH,ff)):
        if not ff.startswith('_'):
            APP_PACK_FOLDERS.append(ff)

for app_pack in APP_PACK_FOLDERS:
    base_apps_pack2 = os.path.join(BASE_APPS_PATH, app_pack)
    x = __import__(app_pack+".apps")
    if hasattr(x.apps, 'PUBLIC') and x.apps.PUBLIC:
        if hasattr(x.apps, 'MAIN_APP_PACK') and x.apps.MAIN_APP_PACK:
            MAIN_APP_PACK = app_pack
        else:
            APP_PACKS.append(app_pack)

if not MAIN_APP_PACK and len(APP_PACKS)==1:
    MAIN_APP_PACK = APP_PACKS[0]
    APP_PACKS = []

with open("/etc/nginx/sites-available/pytigon", "wt") as conf:
    conf.write(CFG_START % ( VIRTUAL_PORT, VIRTUAL_HOST))
    port = START_CLIENT_PORT
    for app_pack in APP_PACKS:
        conf.write(CFG_ELEM % (app_pack, "http://127.0.0.1", port, app_pack))
        port += 1
    if MAIN_APP_PACK:
        conf.write(CFG_END % ("http://127.0.0.1", port))

if MAIN_APP_PACK:
    APP_PACKS.append(MAIN_APP_PACK)

port = START_CLIENT_PORT

ret_tab = []
for app_pack in APP_PACKS:
    cmd = "cd /var/www/pytigon/app_pack/%s && exec daphne -b 0.0.0.0 -p %d --access-log /var/log/pytigon-access.log asgi:application" % (app_pack, port)
    port += 1
    print(cmd)
    ret_tab.append(subprocess.Popen(cmd, shell=True))

restart = subprocess.Popen("nginx -g 'daemon off;'", shell=True)
restart.wait()

for pos in ret_tab:
    pos.wait()

