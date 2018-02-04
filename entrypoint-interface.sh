#!/bin/bash
cd /var/www/pytigon/app_pack/${app_pack} && exec daphne -b 0.0.0.0 -p 8000 asgi:channel_layer
