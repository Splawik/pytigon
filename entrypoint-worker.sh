#!/bin/bash
cd /var/www/pytigon/app_pack/${app_pack} && python3.6 manage.py runworker
