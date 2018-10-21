import pendulum
import traceback
import asyncio

def every_day(at_hour=0, at_minute=0, at_second=0, in_weekdays=None):
    def _every_day(dt=None):
        nonlocal at_hour, at_minute, at_second, in_weekdays
        if dt:
            x = dt.add(days=1)
        else:
            x = pendulum.now()
            if at_hour <= x.hour:
                if at_hour == x.hour:
                    if at_minute <= x.minute:
                        x = x.add(days=1)
                else:
                    x = x.add(days=1)
        x = x.set(hour = at_hour, minute=at_minute, second=at_second)
        if in_weekdays:
            for i in range(7):
                if x.weekday() in in_weekdays:
                    return x
                x = x.add(days=1)
        return x
    return _every_day

def every_day_in_weekend(at_hour=0, at_minute=0, at_second=0):
    return every_day(at_hour=at_hour, at_minute=at_mminute, at_second=at_second, in_weekdays=(6,7))

def every_work_day(at_hour=0, at_minute=0, at_second=0):
    return every_day(at_hour=at_hour, at_minute=at_mminute, at_second=at_second, in_weekdays=range(0,5))

def every_hour(hours=1, at_minute=0, at_second=0, n_weekdays=None, in_hours=None):
    def _every_hour(dt=None):
        nonlocal at_minute, at_second, in_hours
        if dt:
            x = dt.add(hours=hours)
        else:
            x=pendulum.now()
            if at_minute <= x.minute:
                x = x.add(hours=1)            
        x=x.set(minute = at_minute, second = at_second)
        if in_hours:
            if not x.hour in in_hours:
                x = x.add(days=1)
                x.hour = in_hours[0]        
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
    return _every_hour

def every_minute(minutes=1, at_second=0, in_weekdays=None, in_hours=None):
    def _every_minute(dt=None):
        nonlocal minutes, at_second, in_weekdays, in_hours
        if dt:
            x = dt.add(minutes=minutes)
        else:
            x = pendulum.now().add(minutes=1)
        x = x.set(second = at_second)
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

def every_second(seconds=1, in_weekdays=None, in_hours=None):
    def _every_second(dt=None):
        nonlocal seconds, in_weekdays, in_hours
        if dt:
            x = dt.add(seconds=seconds)
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
        
    def add_task(self, task, time_function, *argi, **argv):
        if type(time_function)==str:
            time_function = eval(time_function, globals())
        self.tasks.append( [task, argi, argv, time_function, time_function() ] )    

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

    scheduler.add_task(hello, every_minute(1))
    scheduler.add_task(hello3, "every_second(3)", "Zorro")
    scheduler.add_task(hello3, every_second(4), "Zorro", second="ABC")
    #scheduler.add_task(exit, every_minute(1))
    scheduler.run()

