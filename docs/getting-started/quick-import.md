# Quick Import Reference

## CLI Entry

```python
from pytigon.pytigon_run import run
run()
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
from pytigon_lib.schtasks.schschedule import SChScheduler

scheduler = SChScheduler(mail_conf, xmlrpc_port)
# Register tasks via module.init_schedule(scheduler, cmd, http)
scheduler.run()
```

## Command Dispatcher

```python
from pytigon.commands import CommandDispatcher

dispatcher = CommandDispatcher()
exit_code = dispatcher.dispatch(["pytigon", "manage_mydb", "migrate"])
```

## Ptig Installer

```python
from pytigon.ptig import PtigExtract

extractor = PtigExtract()
extractor.extract("/path/to/archive.ptig")
```
