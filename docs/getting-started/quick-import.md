# Quick Import Reference

## CLI Entry

```python
from pytigon.pytigon_run import run
run()

# or via console script:
# ptig <command>
```

## Embedded Django

```python
from pytigon.django_min_init import init
init("schscripts", embeded_django=True)
```

## HTTP Client

```python
from pytigon.pytigon_request import init, request

init("myapp", username="admin", password="secret")
resp = request("/api/status/")
```

`request(url, params=None)` performs a GET when `params` is `None`, otherwise
a POST. The embedded Django server listens on `127.0.0.2`.

## Task Scheduler

```python
from pytigon_lib.schhttptools.httpclient import init_embeded_django, HttpClient
from pytigon_lib.schtasks.schschedule import SChScheduler

init_embeded_django()
http = HttpClient("http://127.0.0.2")

# mail_conf is optional; rpc_port enables the XML-RPC control interface
scheduler = SChScheduler(mail_conf=None, rpc_port=7080)
# Register tasks via module.init_schedule(scheduler, cmd, http)
scheduler.run()
```

The scheduler runs on a Twisted reactor. Schedule helpers live in
`pytigon_lib.schtasks.schschedule`: `daily`, `hourly`, `monthly`,
`in_minute_intervals`, `in_second_intervals`.

## Command Dispatcher

```python
from pytigon.commands import CommandDispatcher

dispatcher = CommandDispatcher()
exit_code = dispatcher.dispatch(["ptig", "manage_mydb", "migrate"])
```

## Ptig Installer

```python
from pytigon_lib.schtools.install import Ptig

ptig = Ptig("/path/to/archive.ptig")
if ptig.is_ok():
    ptig.extract_ptig()

# or use as context manager:
with Ptig("/path/to/archive.ptig") as ptig:
    if ptig.is_ok():
        ptig.extract_ptig()
```

## Initialize a New Project

```python
from pytigon.ptig import init

init("my_project_name")
```

This is equivalent to running `ptig init_my_project_name` from the shell.

## pytigon_lib — Core Library

```python
# iHTML → HTML templating
from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html

# Document rendering contexts (PDF, DOCX, XLSX, HTML)
from pytigon_lib.schhtml.basedc import BaseDc, NullDc, SubDc
from pytigon_lib.schhtml.pdfdc import PdfDc, PdfDcInfo
from pytigon_lib.schhtml.docxdc import DocxDc, DocxDcinfo
from pytigon_lib.schhtml.xlsxdc import XlsxDc, XlsxDcinfo
from pytigon_lib.schhtml.htmlviewer import HtmlViewerParser, stream_from_html

# Table abstraction (database, virtual file system, proxy)
from pytigon_lib.schtable.table import Table, CMD_INFO, CMD_PAGE, CMD_COUNT
from pytigon_lib.schtable.dbtable import DbTable

# HTTP client + REST helpers
from pytigon_lib.schhttptools.httpclient import HttpClient, RetHttp, AppHttp
from pytigon_lib.schhttptools.rest_client import get_rest_client

# HTML/XML parsing
from pytigon_lib.schparser.parser import Parser, Elem
from pytigon_lib.schparser.html_parsers import (
    SimpleTabParser, TreeParser, ShtmlParser
)

# OOXML / ODF spreadsheet generation
from pytigon_lib.schspreadsheet.ooxml_process import OOXmlDocTransform
from pytigon_lib.schspreadsheet.odf_process import OdfDocTransform

# Virtual file system tools
from pytigon_lib.schfs.vfstools import (
    open_file, get_unique_filename, norm_path, extractall
)

# Extended Django fields + forms
from pytigon_lib.schdjangoext.fields import (
    ForeignKey, ManyToManyField, PtigHiddenForeignKey
)
from pytigon_lib.schdjangoext.fastform import form_from_str

# Generic table/row views + view helpers
from pytigon_lib.schviews import (
    GenericTable, GenericRows, make_path, gen_tab_action, gen_row_action,
    VIEWS_REGISTER, extend_generic_view
)
from pytigon_lib.schviews.viewtools import (
    ExtTemplateResponse, render_to_response_ext
)
from pytigon_lib.schviews.actions import (
    ok_response, cancel_response, error_response
)
```

## pytigon_gui — wxPython Client

The desktop client is optional. Import lazily so that headless deployments
do not require wxPython:

```python
# Native HTML widget (wx.html2 based, with CEF/WebKit backends)
from pytigon_gui.guictrl.ctrl import HTML2

# Grid control + table models
from pytigon_gui.guictrl.grid.grid import SchGrid
from pytigon_gui.guictrl.grid.gridtable_from_proxy import GridTableFromProxy

# Top-level app + frame
from pytigon_gui.pytigon import main
from pytigon_gui.guiframe.appframe import SchAppFrame

# Toolbar variants
from pytigon_gui.toolbar.standardtoolbar import StandardToolBar
from pytigon_gui.toolbar.treetoolbar import TreeToolBar
```
