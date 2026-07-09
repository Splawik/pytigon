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

## Task Scheduler

```python
from pytigon_lib.schhttptools.httpclient import init_embeded_django, HttpClient
from pytigon_lib.schtasks.schschedule import SChScheduler

init_embeded_django()
http = HttpClient("http://127.0.0.2")

scheduler = SChScheduler(mail_conf, xmlrpc_port)
# Register tasks via module.init_schedule(scheduler, cmd, http)
scheduler.run()
```

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
