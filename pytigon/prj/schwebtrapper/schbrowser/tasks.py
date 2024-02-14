from django.utils.translation import gettext_lazy as _

import os
import sys
import datetime
import time
from queue import Empty
from pytigon_lib.schtasks.publish import publish


from pytigon_lib.schhttptools import httpclient
from html.parser import HTMLParser
from pytigon_lib.schhtml.parser import Parser
import re
from pytigon_lib.schtools.schjson import json_dumps
import urllib.parse
import httpx


def download_task(cproxy=None, **kwargs):

    base_address, url = kwargs["user_parm"]
    path = urllib.parse.urljoin(base_address, url)
    if cproxy:
        cproxy.log(url)
    r = httpx.get(path)
    file_name = url.split("?")[0].split("/")[-1]
    with open("/tmp/" + file_name, "wb") as f:
        f.write(r.content)
    if cproxy:
        cproxy.log("finish")


def scan_html(cproxy=None, **kwargs):

    parm = kwargs["user_parm"]
    base_address = parm["base_address"]
    source_page = parm["source_page"]
    subpage_href = parm["subpage_href"]
    download_mask = parm["download_mask"]
    levels = parm["levels"]
    test_only = parm["test_only"]

    def msg(s):
        cproxy.log(s)

    def process_url(url):
        cproxy.add_task(
            "system",
            "Download",
            "@schbrowser:download_task",
            user_parm=[base_address, url],
        )
        msg("download: " + url)

    http = httpclient.HttpClient("")

    def _process(href, href_list=[], download_list=[], history_list=[]):
        class _DownloadHTMLParser(Parser):
            def __init__(self, href_list=[], download_list=[], history_list=[]):
                self.href_list = href_list
                self.download_list = download_list
                self.history_list = history_list
                super().__init__()

            def handle_starttag(self, tag, attrs):
                dattrs = dict(attrs)
                if "href" in dattrs:
                    if subpage_href:
                        for pos in subpage_href.split(";"):
                            if pos.startswith("@"):
                                pos = pos[1:]
                                end = True
                            else:
                                end = False
                            matchObj = re.match(pos, dattrs["href"], re.M | re.I)
                            if matchObj:
                                if not dattrs["href"] in self.history_list:
                                    if end:
                                        self.href_list.append("@" + dattrs["href"])
                                        self.history_list.append(dattrs["href"])
                                    else:
                                        self.href_list.append(dattrs["href"])
                                        self.history_list.append(dattrs["href"])
                                return
                    for pos in download_mask.split(";"):
                        matchObj = re.match(pos, dattrs["href"], re.M | re.I)
                        if matchObj:
                            href = dattrs["href"].split("?")[0]
                            if not href in self.download_list:
                                self.download_list.append(href)
                                process_url(href)

        try:
            txt = cproxy.input_queue.get_nowait()
            if txt == "^C":
                return
        except Empty:
            pass

        path = urllib.parse.urljoin(base_address, href)
        r = httpx.get(path)
        p = r.text
        parser = _DownloadHTMLParser(href_list, download_list, history_list)
        msg("SCAN: " + path)
        parser.feed(p)
        return (parser.href_list, parser.download_list, parser.history_list)

    href_list, download_list, history_list = _process(source_page)
    msg("INFO:" + source_page)
    x = 0
    while x < levels:
        href_list2 = []
        for pos in href_list:
            if pos.startswith("@"):
                _process(pos[1:], [], download_list, history_list)
            else:
                _process(pos, href_list2, download_list, history_list)
        href_list = href_list2
        x += 1
    msg("INFO:END!")
