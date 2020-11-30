# Pytigon tasks

Zadania uruchamiane w tle dla aplikacji Pytigon bazują na bibliotece Django Q ( https://django-q.readthedocs.io/en/latest/# ). Pytigon wprowadza kilka dodatkowych funkcjonalności, ale w najprostszym nie musisz ich wogóle używać.

### Przykład 1 - integracja wyłącznie przy użyciu mechanizmów Django Q

plik tasks.py:

```python
import time

def long_running_process():
    print("start")
    time.sleep(100)
    print("end")
    return 1
```

plik views.py:

```python

from django_q.tasks import async_task, result

def v(request):
    task_id = async_task("tasks.long_running_process")
    return { "ret": task_id }
```

---

Pytigon posiada dodatkowe mechanizmy, które pozwalają na komunikację pomiędzy frontend'em aplikacji a zadaniem w tle. Aby je wdrożyć należy odowiednio zdefiniować funkcję uruchamiającą zadanie w tle. Tym razem musi być ono zdefiniowane jak w przykładzie:

### Przykład 2 - integracja z możliwością komunikacji z frontendem aplikacji

```python

import time
from pytigon_lib.schtasks.publish import publish

@publish("demo")
def test_task(cproxy=None, **kwargs):
    if 'param' in kwargs:
        print(kwargs['param'])
    if cproxy:
        cproxy.send_event("<ul class='data'></ul><div name='task_end_info' style='display: none;'>Finish</div>")
    for i in range(0,30):
        if cproxy:
            cproxy.send_event("<li>item %d</li>===>>.data" % i)
        time.sleep(1)
    return True
```

Głowna różnica w stosunku do przykładu 1 jest użycie dekoratora @publish. Dekorator posiada jeden argument: task_publish_group. Argument ten definiuje nazwę grupy zadań, która umożliwi wyszukanie zadania przez frontend.

Argumenty funkcji definiującej zadanie w tle także muszą podlegać pewnym regułow. Pierwszym argumentem jest zmienna cproxy. W wyniku działania dekoratora @publish zmienna ta automatycznie zostanie skojarzona z obiektem typu CommunicationBasePublisher. Obiekt ten pozwala na komunikację z frontendem przy pomocy funkcji send_event.

Klasa CommunicationBasePublisher wygląda tak:

```python
class CommunicationBasePublisher():

    def send_event(self, value):
        pass

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()
```

Uruchomienie zadań udostępniających komunikację z frontend'em jest podobne do tego z przykładu 1:

```python
from django_q.tasks import async_task, result

...
task_id = async_task("tasks.test_task", task_publish_id="test1",  param=123)
return { "ret": task_id }
```

Specjalne znaczenie ma tu przekazanie jako parametru "task_publish_id". Tworzy on razem z parametrem dekoratora @publish: task_publish_group dane, które jednoznacznie pozwalają zdefiniować zadanie.

Frontend z zadaniem w tle komunikuje się poprzez websocket, zdefiniowany pod adresem: "/schtasks/show_task_events/channel/". Najłatwiej komunikację tą zestawić przy pomocy webcomponent'u ptig-task. Przykładowa definicja webcomponent'u może wyglądać tak:

```html
<ptig-task
  websocket_href="/schtasks/show_task_events/channel/"
  task_id="demo__test1"
></ptig-task>
```

Warto tutaj omówić atrybut task_id, jest to połączenie task_publis_gorup, podówjnego podkreślenia "\_\_" oraz task_publish_id. Dla przedstawionych powyżej zadania i jego wywołania daje to "demo\_\_test1".

Kod źródłowy komponentu ptygi-task dostarczony jest z programem Pytigon. Jeżeli chcesz tworzyć elementy komunikacji między zadaniami w tle a frontend'em koniecznie rzuć okiem na to jak komponent jest skonstruowany.
