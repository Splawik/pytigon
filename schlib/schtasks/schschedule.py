import pendulum
import traceback
import sys
import asyncio

from asyncio.events import get_event_loop

loop = get_event_loop()

import twisted.internet.asyncioreactor
twisted.internet.asyncioreactor.install(loop)

from twisted.internet import reactor
import twisted
from twisted.internet.defer import inlineCallbacks, Deferred

from twisted.web import xmlrpc, server

INIT_TIME = pendulum.now()

def at_iterate(param):
    ret = []
    def tab_from_str(s):
        tab = [0, 0, 0]
        x = s.split(':')
        i = 0
        for ss in x[:3]:
            tab[i] = int(ss)
            i += 1
        return tab
    if type(param) in (list, tuple):
        for pos in param:
            if type(pos) == str:
                ret.append(tab_from_str(pos))
            else:
                ret.append([pos,0,0])
    elif type(param)==str:
        for pos in param.split(';'):
            if pos:
                ret.append(tab_from_str(pos))
    else:
        ret.append([param,0,0])
    return ret

def monthly(day=1, at=0, in_months=None, in_weekdays=None):
    ret = []
    _day = day
    def make_monthly_fun(_hour, _minute, _second):
        def _monthly(dt=None):
            nonlocal day, _day, _hour, _minute, _second, in_months, in_weekdays
            if dt:
                x = dt.add(months=1)
            else:
                x = INIT_TIME
                if _day <= x.day:
                    if _day == x.day:
                        if _hour <= x.hour:
                            if _hour == x.hour:
                                if _minute <= x.minute:
                                    x = x.add(months=1)
            day2=day
            test=False
            while not test:
                try:
                    x = x.set(day=day2, hour=_hour, minute=_minute, second=_second)
                    test = True
                except:
                    if _day in (29,30,31):
                        day2-=1
                    else:
                        day2+=1

            if in_months:
                for i in range(12):
                    if x.month in in_months:
                        break
                    x = x.add(month=1)

            if in_weekdays and not x.weekday in in_weekdays:
                for i in range(7):
                    x = x.add(days=1)
                    if x.weekday() in in_weekdays:
                        return x
            return x
        return  _monthly
    for _hour, _minute, _second in at_iterate(at):
        ret.append(make_monthly_fun(_hour, _minute, _second))

    return ret

def daily(at=0, in_weekdays=None):
    ret = []
    def make_daily_fun(_hour, _minute, _second):
        def _daily(dt=None):
            nonlocal _hour, _minute, _second, in_weekdays
            if dt:
                x = dt.add(days=1)
            else:
                x = INIT_TIME
                if _hour <= x.hour:
                    if _hour == x.hour:
                        if _minute <= x.minute:
                            x = x.add(days=1)
                    else:
                        x = x.add(days=1)
            x = x.set(hour = _hour, minute=_minute, second=_second)
            if in_weekdays and not x.weekday() in in_weekdays:
                for i in range(7):
                    x = x.add(days=1)
                    if x.weekday() in in_weekdays:
                        return x
            return x
        return  _daily
    for _hour, _minute, _second in at_iterate(at):
        ret.append(make_daily_fun(_hour, _minute, _second))
    return ret

def hourly(period=1, at=0, in_weekdays=None, in_hours=None):
    ret = []
    def make_hourly_fun(_minute, _second):
        def _hourly(dt=None):
            nonlocal period, _minute, _second, in_weekdays, in_hours
            if dt:
                x = dt.add(hours=period)
            else:
                x = INIT_TIME
                if _minute <= x.minute:
                    x = x.add(hours=1)
            x=x.set(minute = _minute, second = _second)
            if in_hours:
                if not x.hour in in_hours:
                    x = x.add(days=1)
                    x = x.set(hour = in_hours[0])
            if in_weekdays and not x.weekday() in in_weekdays:
                for i in range(7):
                    x = x.add(days=1)
                    if x.weekday() in in_weekdays:
                        if in_hours:
                            x=x.set(hour=in_hours[0])
                        else:
                            x=x.set(hour = 0)
                        return x
            return x
        return  _hourly
    for _minute, _second, _ in at_iterate(at):
        ret.append(make_hourly_fun(_minute, _second))
    return ret

def in_minute_intervals(period=1, at=0, in_weekdays=None, in_hours=None):
    ret = []
    def make_in_minute_intervals_fun(_second):
        def _in_minute_intervals(dt=None):
            nonlocal period, _second, in_weekdays, in_hours
            if dt:
                x = dt.add(minutes=period)
            else:
                x = INIT_TIME.add(minutes=1)
            x = x.set(second = _second)
            if in_hours:
                if not x.hour in in_hours:
                    x = x.add(days=1).set(hour = in_hours[0])
            if in_weekdays and not x.weekday() in in_weekdays:
                for i in range(7):
                    x = x.add(days=1)
                    if x.weekday() in in_weekdays:
                        if in_hours:
                            x.hour =in_hours[0]
                        else:
                            x.hour = 0
                        return x
            return x
        return _in_minute_intervals
    for _minute, _second, _ in at_iterate(at):
        ret.append(make_in_minute_intervals_fun(_second))
    return ret

def in_second_intervals(period=1, in_weekdays=None, in_hours=None):
    def _in_second_intervals(dt=None):
        nonlocal period, in_weekdays, in_hours
        if dt:
            x = dt.add(seconds=period)
        else:
            x =  INIT_TIME
        if in_hours:
            if not x.hour in in_hours:
                x = x.add(days=1).set(hour = in_hours[0], minute = 0, second = 0)
        if in_weekdays and not x.weekday() in in_weekdays:
            for i in range(7):
                x = x.add(days=1)
                if x.weekday() in in_weekdays:
                    if in_hours:
                        x=x.set(hour = in_hours[0])
                    else:
                        x=x.set(hour = 0)
                    x=x.set(minute = 0, second = 0)
                    return x
        return x
    return _in_second_intervals


class RpcServer(xmlrpc.XMLRPC):

    def xmlrpc_echo(self, x):
        return x + "!"


class SChScheduler():
    def __init__(self, mail_conf=None):
        self.tasks = []
        self.fmap = {
            'M': monthly,
            'd': daily,
            'h': hourly,
            'm': in_minute_intervals,
            's': in_second_intervals
        }
        self.rcpserver = RpcServer()
        reactor.listenTCP(7080, server.Site(self.rcpserver))
        if mail_conf:
            from schlib.schtools.imap4client import IMAPClient
            self.imap4 = IMAPClient(mail_conf['server'], mail_conf['username'], mail_conf['password'],
                                    mail_conf['inbox'], mail_conf['outbox'])
        else:
            self.imap4 = None

        self.rcpserver_activated = False

    def __getattr__(self, item):
        return self.fmap[item]

    def add_task(self, time_functions, task, *argi, **argv):
        functions = []
        if type(time_functions)==str:
            x = time_functions.split(';')
            for pos in x:
                if pos:
                    if (len(pos)>2 and pos[1]=='(') or len(pos)==1:
                        if pos[0] in self.fmap:
                            x = pos.split('(')
                            if len(x)>1:
                                pos = self.fmap[pos[0]].__name__+"("+x[1]
                            else:
                                pos = self.fmap[pos[0]].__name__+"()"

                    y = eval(pos, globals())
                    if type(y) in (list, tuple):
                        functions = y
                    else:
                        functions.append(y)
        elif type(time_functions) in (list, tuple):
            functions = time_functions
        else:
            functions = [time_functions,]
        for fun in functions:
            self.tasks.append([task, argi, argv, fun, fun(), task.__name__])

    def add_rcp_fun(self, name, fun):
        setattr(self.rcpserver, name, fun)
        self.rcpserver_activated = True

    def get_tasks(self, name):
        ret = []
        for task in self.tasks:
            if task[5] == name:
                ret.append(task)
        return ret

    def remove_tasks(self, name):
        tasks = self.get_tasks(name)
        for task in tasks:
            self.tasks.remove(task)

    def clear(self):
        self.tasks.clear()

    async def process(self, dt):
        if self.tasks:
            processes = []
            for task in self.tasks:
                if task[4]<=dt:
                    task[4]=task[3](task[4])
                    try:
                        processes.append(task[0](*task[1], **task[2]))
                    except:
                        print(sys.exc_info()[0])
                        print(traceback.print_exc())

            def _key(elem):
                return elem[4]

            self.tasks.sort(key=_key)

            if processes:
                await asyncio.wait(processes)

    async def _run(self):
        if self.tasks or self.rcpserver_activated or self.imap4:
            old_time = None
            while True:
                dt  = pendulum.now()
                str_time = str(dt).strip('.')
                if not (old_time and old_time == str_time):
                    await self.process(dt)
                    if not self.tasks and not self.rcpserver_activated and not self.imap4:
                        return

                await asyncio.sleep(0.2)

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._run())


if __name__ == '__main__':    
    INIT_TIME = pendulum.datetime(2016, 5, 1)

    scheduler = SChScheduler()

    async def hello():
        print("Hello world")

    async def hello1(name="", scheduler=None):
        if scheduler:
            tasks = scheduler.get_tasks('hello1')
            if len(tasks)>0:
                print(tasks[0][4])
                return
        print("Hello world 1")

    async def hello2(scheduler):
        print("Hello world 2")
        scheduler.remove_tasks('hello2')

    async def exit(scheduler):
        scheduler.clear()

    if False:
        scheduler.add_task(in_minute_intervals(1), hello)
        scheduler.add_task("in_second_intervals(3)", hello)
        scheduler.add_task(in_second_intervals(4), hello)
        scheduler.add_task(hourly(at="2;3"), hello)
        scheduler.add_task(daily(at="22:07"), hello)
        scheduler.add_task(monthly(day=1, at="22:07"), hello)

        scheduler.add_task(monthly(day=1, at="22:07"), hello1, name="monthly", scheduler=scheduler)
        scheduler.add_task(daily(at="22:07", in_weekdays=(1,2,3,4,5)), hello1, name="monthly", scheduler=scheduler)
        scheduler.add_task("hourly(at=7,in_weekdays=range(1,6), in_hours=range(3,5))",  hello1, name="monthly", scheduler=scheduler)
        scheduler.add_task("in_second_intervals(in_weekdays=range(1,2), in_hours=range(3,5))",  hello1, name="in_second_intervals", scheduler=scheduler)

        scheduler.add_task("in_second_intervals(in_weekdays=range(1,2), in_hours=range(3,5))",  hello2, scheduler)

        scheduler.add_task(in_minute_intervals(1), exit, scheduler=scheduler)

    scheduler.add_task("M(day=31, at='22:07')", hello1, name="monthly", scheduler=scheduler)
    scheduler.add_task("M", hello1, name="monthly", scheduler=scheduler)
    scheduler.add_task(scheduler.s(), hello1, name="monthly", scheduler=scheduler)

    scheduler.run()
