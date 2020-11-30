# Scheduled tasks:

Jeżeli zdefiniujesz tu funkcję: init_schedule(scheduler, cmd, http), automatycznie będzie ona wywoływana
w trakcie startu systemu. Aby tak się stało Pytigon musi być odpowiednio w tym celu skonfigurwany: patrz [[Tasks]])

Przykłady użycia:
W przykładzie poniżej zaprezentowane są 3 typy zadań:

1. uruchamiane wg harmonogramu:

   - proste zadanie - przykład hello()
   - custom django-admin commands - przykłąd manage_send_mail, cmd stanowi proxy do akcji django (https://docs.djangoproject.com/en/2.1/howto/custom-management-commands/)
   - uruchomienie django views: przykład gen, http udostępnia metody get i post i stanowi proxy do serwera django.

2. uruchamiane zdalnie przez wywołanie funkcji XML-RPC, funkcję sum możesz uruchomić z programu zewnętrznego w sposób:
   import xmlrpc.client
   with xmlrpc.client.ServerProxy('http://localhost:7080/') as proxy:
   print(proxy.sum(2,3))

3. w odpowiedzi na przychodzącego maila, przykład check_mails, funkcja ta jest wywoływana wg harmonogramu, w momencie gdy nadejdzie mail wywoływana jest funkcja check_mail, z parametrem będącym zawartością maila.

```python
async def hello():
    print("Hello world!")

async def manage_send_mail(cmd):
    cmd("send_mail")

async def gen(http, id):
    param = { 'id': id }
    href = "/raporty/table/Raporty/action/gen/"
    http.post(None, href, param)

def check_mail(mail):
    print(mail)

async def check_mails(imap4):
    imap4.check_mails(callback):

def init_schedule(scheduler, cmd, http):
    scheduler.add_task("hourly(at=30,in_weekdays=range(1,6), in_hours=range(5,17))", manage_send_mail, cmd)
    scheduler.add_task("daily(at='22:30'))", gen, http=http, id='T')
    scheduler.add_task("in_minute_intervals(period=10)", check_mails, scheduler.imap4)
    scheduler.add_task("in_second_intervals(period=30)", hello)

    def _sum(a,b):
        return a+b

    scheduler.add_rcp_fun("sum", _sum)
```
