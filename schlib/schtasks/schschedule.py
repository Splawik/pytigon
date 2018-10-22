import pendulum
import traceback
import sys
import asyncio

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

def every_month(day=1, at=0, in_months=None, in_weekdays=None):
    ret = []
    _day = day
    def make_every_month_fun(_hour, _minute, _second):
        def _every_month(dt=None):
            nonlocal _day, _hour, _minute, _second, in_months, in_weekdays
            if dt:
                x = dt.add(months=1)
            else:
                x = pendulum.now()
                if _day <= x.day:
                    if _day == x.day:
                        if _hour <= x.hour:
                            if _hour == x.hour:
                                if _minute <= x.minute:
                                    x = x.add(months=1)
            x = x.set(day= _day, hour = _hour, minute=_minute, second=_second)
            if in_months:
                for i in range(12):
                    if x.month in in_months:
                        break
                    x = x.add(month=1)

            if in_weekdays:
                for i in range(7):
                    if x.weekday() in in_weekdays:
                        return x
                    x = x.add(days=1)
            return x
        return  _every_month
    for _hour, _minute, _second in at_iterate(at):
        ret.append(make_every_month_fun(_hour, _minute, _second))

    return ret

def every_day(at=0, in_weekdays=None):
    ret = []
    def make_every_day_fun(_hour, _minute, _second):
        def _every_day(dt=None):
            nonlocal _hour, _minute, _second, in_weekdays
            if dt:
                x = dt.add(days=1)
            else:
                x = pendulum.now()
                if _hour <= x.hour:
                    if _hour == x.hour:
                        if _minute <= x.minute:
                            x = x.add(days=1)
                    else:
                        x = x.add(days=1)
            x = x.set(hour = _hour, minute=_minute, second=_second)
            if in_weekdays:
                for i in range(7):
                    if x.weekday() in in_weekdays:
                        return x
                    x = x.add(days=1)
            return x
        return  _every_day
    for _hour, _minute, _second in at_iterate(at):
        ret.append(make_every_day_fun(_hour, _minute, _second))
    return ret

def every_day_in_weekend(at=0):
    return every_day(at, in_weekdays=(6,7))

def every_work_day(at=0):
    return every_day(at, in_weekdays=range(0,5))

def every_hour(period=1, at=0, in_weekdays=None, in_hours=None):
    ret = []
    def make_every_hour_fun(_minute, _second):
        def _every_hour(dt=None):
            nonlocal period, _minute, _second, in_weekdays, in_hours
            if dt:
                x = dt.add(hours=period)
            else:
                x=pendulum.now()
                if _minute <= x.minute:
                    x = x.add(hours=1)
            x=x.set(minute = _minute, second = _second)
            if in_hours:
                if not x.hour in in_hours:
                    x = x.add(days=1)
                    x.set(hour = in_hours[0])
            if in_weekdays:
                for i in range(7):
                    if x.weekday() in in_weekdays:
                        if in_hours:
                            x=x.set(hour=in_hours[0])
                        else:
                            x=x.set(hour = 0)
                        return x
                    x = x.add(days=1)
            return x
        return  _every_hour
    for _minute, _second, _ in at_iterate(at):
        ret.append(make_every_hour_fun(_minute, _second))
    return ret

def every_minute(period=1, at=0, in_weekdays=None, in_hours=None):
    ret = []
    def make_every_minute_fun(_second):
        def _every_minute(dt=None):
            nonlocal period, _second, in_weekdays, in_hours
            if dt:
                x = dt.add(minutes=period)
            else:
                x = pendulum.now().add(minutes=1)
            x = x.set(second = _second)
            if in_hours:
                if not x.hour in in_hours:
                    x = x.add(days=1).set(hour = in_hours[0])
            if in_weekdays:
                for i in range(7):
                    if x.weekday() in in_weekdays:
                        if in_hours:
                            x.hour =in_hours[0]
                        else:
                            x.hour = 0
                        return x
                    x = x.add(days=1)
            return x
        return _every_minute
    for _minute, _second, _ in at_iterate(at):
        ret.append(make_every_minute_fun(_second))
    return ret

def every_second(period=1, in_weekdays=None, in_hours=None):
    def _every_second(dt=None):
        nonlocal period, in_weekdays, in_hours
        if dt:
            x = dt.add(seconds=period)
        else:
            x =  pendulum.now()
        if in_hours:
            if not x.hour in in_hours:
                x = x.add(days=1).set(hour = in_hours[0], minute = 0, second = 0)
        if in_weekdays:
            for i in range(7):
                if x.weekday() in in_weekdays:
                    if in_hours:
                        x=x.set(hour = in_hours[0])
                    else:
                        x=x.set(hour = 0)
                    x=x.set(minute = 0, second = 0)
                    return x
                x = x.add(days=1)                
        return x
    return _every_second

class SChScheduler():
    def __init__(self):
        self.tasks = []
        self.current_task = None
        self.current_time = None
        
    def add_task(self, time_functions, task, *argi, **argv):
        functions = []
        if type(time_functions)==str:
            x = time_functions.split(';')
            for pos in x:
                if pos:
                    functions.append(eval(pos, globals()))
        elif type(time_functions) in (list, tuple):
            functions = time_functions
        else:
            functions = [time_functions,]
        for fun in functions:
            self.tasks.append([task, argi, argv, fun, fun()])
        print(self.tasks)
    async def process(self, dt):
        if self.tasks:
            processes = []
            for task in self.tasks:
                if task[4]<=dt:
                    task[4]=task[3](task[4])
                    try:
                        self.current_task = task
                        self.current_time = dt
                        processes.append(task[0](*task[1], **task[2]))
                        self.current_task = None
                        self.current_time = None
                    except:
                        print(sys.exc_info()[0])
                        print(traceback.print_exc())
                        
            def _key(elem):
                return elem[4]                
                
            self.tasks.sort(key=_key)
             
            if processes:
                await asyncio.wait(processes)
                print(self.tasks)
                
    async def _run(self):
        if self.tasks:
            old_time = None
            while True:
                dt  = pendulum.now()
                str_time = str(dt).strip('.')
                if not (old_time and old_time == str_time):
                    await self.process(dt)
                    if self.tasks:
                        dt  = pendulum.now()
                        x = dt - self.tasks[0][4]
                        delta = x.in_seconds()
                        if delta>1:
                            await asyncio.sleep(delta-1)
                    else:
                        return
                await asyncio.sleep(0.3)
        
    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._run())


if __name__ == '__main__':                    
    scheduler = SChScheduler()

    async def hello():
        print("hello world")

    async def hello3(name, second="x"):
        print("hello world: ", name, second)

    async def exit(scheduler):
        #scheduler.tasks.remove(scheduler.current_task)
        scheduler.tasks.clear()

    #scheduler.add_task(every_minute(1), hello)
    #scheduler.add_task("every_second(3)", hello3, "Zorro")
    #scheduler.add_task(every_second(4), hello3, "Zorro", second="ABC")
    #scheduler.add_task(exit, every_minute(1))
    scheduler.add_task(every_hour(at="2;3"), hello)
    scheduler.add_task(every_day(at="22:07"), hello)
    scheduler.add_task(every_month(day=1, at="22:07"), hello)
    scheduler.run()

