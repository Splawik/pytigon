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
# copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
# license: "LGPL 3.0"
# version: "0.1a"


class ViewRequests(object):
    def process_request(self, request):
        print(request.method, request.path)


def view_post(get_response):
    def middleware(request):
        try:
            if request.method == "POST":
                print("=================== POST ======================")
                print(request.path)
                print(request.POST)
                print("===============================================")
        except:
            pass
        response = get_response(request)
        return response

    return middleware


class ViewPost(object):
    def process_request(self, request):
        try:
            if request.method == "POST":
                print("=================== POST ======================")
                print(request.path)
                print(request.POST)
                print("===============================================")
        except:
            pass


class BeautyHtml:
    def process_response(self, request, response):
        if not response.streaming:
            if type(response.content) == str:
                response.content = "\n".join(
                    [line for line in response.content.split("\n") if line.strip()]
                )
            elif type(response.content) == bytes:
                response.content = "\n".join(
                    [
                        line
                        for line in response.content.decode("utf-8").split("\n")
                        if line.strip()
                    ]
                )
        return response
