#!/usr/bin/python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

# Pytigon - wxpython and django application framework

# author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
# copyright: "Copyright (C) ????/2020 Slawomir Cholaj"
# license: "LGPL 3.0"
# version: "0.108"

from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from django.utils.functional import SimpleLazyObject
from graphql_jwt.utils import get_http_authorization, get_payload


def get_user(request, username):
    if (not hasattr(request, "_cached_user")) or request._cached_user.is_anonymous:
        users = get_user_model().objects.filter(username=username)
        request._cached_user = users[0] if len(users) > 0 else None
    return request._cached_user


class JWTUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = get_http_authorization(request)
        try:
            payload = get_payload(token)
            username = payload["username"]
            request.user = SimpleLazyObject(lambda: get_user(request, username))
        except:
            pass
