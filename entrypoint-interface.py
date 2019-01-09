#! /usr/bin/python3
import subprocess
import os
import sys
from os import environ

from schlib.schtools.tools import get_executable

BASE_APPS_PATH = "/var/www/pytigon/app_pack"
sys.path.append(BASE_APPS_PATH)

if 'VIRTUAL_HOST' in environ:
    VIRTUAL_HOST = str(environ['VIRTUAL_HOST'])
else:
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

# NUMBER_OF_WORKER_PROCESSES struct:
# 1. NUMBER_FOR_MAIN_APP, for example: 4
# 2. NUMBER_FOR_MAIN_APP:NUMBER_FOR_ADDITIONAL_APP, for example: 4:1
# 3. NAME_OF_SPECIFIC_APP:NUMBER_FOR_SPECIFIC_APP,*, for example:  schportal:4,schdevtools:2

NOWP = {}
if 'NUMBER_OF_WORKER_PROCESSES' in environ:
    nowp = environ['NUMBER_OF_WORKER_PROCESSES']
    if ':' in nowp:
        if ',' in nowp or ';' in nowp:
            for pos in nowp.replace(',', ';').split(';'):
                if ':' in pos:
                    x = pos.split(':')
                    NOWP[x[0]] = x[1]
                else:
                    NOWP[x] = 1
        else:
            x = nowp.split(':')
            NOWP['default-main'] = int(x[0])
            NOWP['default-additional'] = int(x[1])
    else:
        NOWP['default-main'] = int(nowp)
        NOWP['default-additional'] = 1
else:
    NOWP['default-main'] = 4
    NOWP['default-additional'] = 1

if 'TIMEOUT' in environ:
    TIMEOUT = environ['TIMEOUT']
else:
    TIMEOUT = "30"

# ASGI_SERVER_NAME:
# 1. daphne
# 2. gunicorn
# 3. hypercorn
ASGI_SERVER_ID = 0
if 'ASGI_SERVER_NAME' in environ:
    if 'gunicorn' in environ['ASGI_SERVER_NAME']:
        ASGI_SERVER_ID = 1
    elif 'dapne' in environ['ASGI_SERVER_NAME']:
        ASGI_SERVER_ID = 2

START_CLIENT_PORT = 8000

APP_PACKS = []
APP_PACK_FOLDERS = []
MAIN_APP_PACK = None

if PORT_80_REDIRECT:
    CFG_OLD = f"""server {{
       listen         {VIRTUAL_PORT_80};
       server_name    {VIRTUAL_HOST} www.{VIRTUAL_HOST};
       return         301 {PORT_80_REDIRECT};
}}

"""

if CRT:
    CFG_START = f"""
server {{
    listen {VIRTUAL_PORT};
    client_max_body_size 20M;
    server_name www.{VIRTUAL_HOST};
    charset utf-8;

    {CRT}
    {KEY}

    return 301 {PORT_80_REDIRECT}$request_uri;
}}"""
else:
    CFG_START = ""

CFG_START += f"""
server {{
    listen {VIRTUAL_PORT};
    client_max_body_size 20M;
    server_name {VIRTUAL_HOST};
    charset utf-8;

    {CRT}
    {KEY}

    location ^~ /static/ {{
        alias /var/www/pytigon/static/;
    }}
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
        proxy_connect_timeout       $TIMEOUT;
        proxy_send_timeout          $TIMEOUT;
        proxy_read_timeout          $TIMEOUT;
        send_timeout                $TIMEOUT;
    }
""".replace('$TIMEOUT', TIMEOUT)

CFG_END = """
    location ~ (.*)$ {
        proxy_pass %s:%d$1$is_args$args;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr$is_args$args;
        proxy_set_header X-Forwarded-For $remote_addr$is_args$args;
        proxy_connect_timeout       $TIMEOUT;
        proxy_send_timeout          $TIMEOUT;
        proxy_read_timeout          $TIMEOUT;
        send_timeout                $TIMEOUT;
    }   
}
""".replace('$TIMEOUT', TIMEOUT)

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
    if os.path.isdir(os.path.join(BASE_APPS_PATH, ff)):
        if not ff.startswith('_'):
            APP_PACK_FOLDERS.append(ff)

for app_pack in APP_PACK_FOLDERS:
    base_apps_pack2 = os.path.join(BASE_APPS_PATH, app_pack)
    try:
        x = __import__(app_pack + ".apps")
    except:
        continue
    if hasattr(x.apps, 'PUBLIC') and x.apps.PUBLIC:
        if hasattr(x.apps, 'MAIN_APP_PACK') and x.apps.MAIN_APP_PACK:
            MAIN_APP_PACK = app_pack
        else:
            APP_PACKS.append(app_pack)

if not MAIN_APP_PACK and len(APP_PACKS) == 1:
    MAIN_APP_PACK = APP_PACKS[0]
    APP_PACKS = []

with open("/etc/nginx/sites-available/pytigon", "wt") as conf:
    if PORT_80_REDIRECT:
        conf.write(CFG_OLD)

    conf.write(CFG_START)
    port = START_CLIENT_PORT
    for app_pack in APP_PACKS:
        conf.write(CFG_ELEM % (
        app_pack, app_pack, "http://127.0.0.1", port, app_pack, app_pack, "http://127.0.0.1", port, app_pack))
        port += 1
    if MAIN_APP_PACK:
        conf.write(CFG_END % ("http://127.0.0.1", port))

    if MAIN_APP_PACK:
        APP_PACKS.append(MAIN_APP_PACK)

port = START_CLIENT_PORT

ret_tab = []
for app_pack in APP_PACKS:

    if app_pack in NOWP:
        count = NOWP[app_pack]
    else:
        count = NOWP['default-main'] if app_pack == MAIN_APP_PACK else NOWP['default-additional']

    server1 = f"hypercorn -b 0.0.0.0:{port} -w {count} --access-log /var/log/pytigon-access.log --error-log /var/log/pytigon-err.log asgi:application"
    server2 = f"gunicorn -b 0.0.0.0:{port} -w {count} -k uvicorn.workers.UvicornWorker --access-logfile /var/log/pytigon-access.log --log-file /var/log/pytigon-err.log asgi:application"
    server3 = f"daphne -b 0.0.0.0 -p {port} --proxy-headers --access-log /var/log/pytigon-access.log asgi:application"

    server = (server1, server2, server3,)[ASGI_SERVER_ID]

    path = f"/var/www/pytigon/app_pack/{app_pack}"

    cmd = f"cd {path} && exec {server}"

    port += 1
    print(cmd)
    ret_tab.append(subprocess.Popen(cmd, shell=True))

if not 'NO_EXECUTE_TASKS' in environ:
    for app_pack in APP_PACKS:
        cmd = "cd /var/www/pytigon && exec %s pytigon_task.py %s" % (get_executable(), app_pack)
        print(cmd)
        ret_tab.append(subprocess.Popen(cmd, shell=True))

restart = subprocess.Popen("nginx -g 'daemon off;'", shell=True)
restart.wait()

for pos in ret_tab:
    pos.wait()

