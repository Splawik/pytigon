#from queue import Queue, Empty
from threading import Thread
from subprocess import Popen, PIPE 
from signal import SIGINT
import sys
import six
import datetime
import importlib
from schlib.schtasks.term_tools import ansi_to_txt
from schlib.schtools.schjson import json_dumps, json_loads
import sqlite3
import tempfile
#import gc

from queue import Empty
from multiprocessing import Process, Queue, Manager


_PROCESS_MANAGER = None
_MAX_PROC_LOG = 99
_ID = 0
_ON_POSIX = 'posix' in sys.builtin_module_names


def enqueue_input(process, input_queue, output_queue, id, status):
    while True:
        try:
            value = input_queue.get()
            if value=='^C':
                process.send_signal(SIGINT)
                process.terminate()
                break
        except:
            print("except")
            print(sys.exc_info()[0])
            break
        else:
            if type(value)==bytes:
                process.stdin.write(value.decode('utf-8'))
            else:
                process.stdin.write(value)
            process.stdin.flush()
            if status == 3:
                output_queue.put((id, "log", ">>> "+ value, {}))

def enqueue_error(process, input_queue, output_queue, id, status):
    while True:
        s = process.stderr.readline()
        if s:
            if type(s) == bytes:
                output_queue.put((id, 'log', s.decode('utf-8'), {}))
            else:
                output_queue.put((id, 'log', s, {}))
        if process.returncode is None:
            process.poll()
        else:
            input_queue.put("^C")
            s = process.stdout.read()
            if s:
                output_queue.put((id, 'log', s, {}))
            break


def write_to_output_queue(txt, output_queue, id, status):
    if type(txt)==bytes:
        s2 = txt.decode('utf-8')
    else:
        s2 = txt
    if status==3:
        s2 = ansi_to_txt(s2)
    output_queue.put((id, 'log', s2, {}))


class CommunicationProxy():
    def __init__(self, id, input_queue, output_queue):
        self.id = id
        self.input_queue = input_queue
        self.output_queue = output_queue

    def log(self, msg):
        self.output_queue.put((self.id, 'log', msg, {}))

    def add_task(self, request_or_username, title, func, user_parm):
        parm = { 'func': func, 'request_or_username': request_or_username, 'title': title, 'user_parm': user_parm }
        self.output_queue.put((self.id, 'system', 'add_task', parm))

#func:
#  ls
#  >ls
#  >>ls
#  >>>ls
#  @app:fun

def run_func(func, cproxy, args, kwargs):
    status = 0
    if isinstance(func, six.string_types) and not func.startswith('@'):
        if func[0]=='>':
            status = 1
            if func[1]=='>':
                status = 2
                if func[2]=='>':
                    status = 3
                    func2 = func[3:]
                else:
                    func2 = func[2:]
            else:
                func2 = func[1:]
        else:
            func2 = func

        l = list(args)
        if len(l)>0:
            cmd = [func2,] + list(args)
        else:
            cmd = func2

        try:
            p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=(status==1), bufsize=1, close_fds=_ON_POSIX, universal_newlines=True)
        except:
            print("cmd error:", cmd)

        t1 = Thread(target=enqueue_error, args=(p, cproxy.input_queue, cproxy.output_queue, id, status))
        t1.daemon = True
        t1.start()

        t2 = Thread(target=enqueue_input, args=(p, cproxy.input_queue, cproxy.output_queue, id, status))
        t2.daemon = True
        t2.start()

        while 1:
            s = p.stdout.readline()
            if s:
                write_to_output_queue(s, cproxy.output_queue, id, status)
            if p.returncode is None:
                p.poll()
            else:
                cproxy.input_queue.put("^C")
                s = p.stdout.read()
                if s:
                    write_to_output_queue(s, cproxy.output_queue, id, status)
                break

        t1.join()
        t2.join()

        return p.returncode
        
    else:
        param = None
        if isinstance(func, six.string_types) and func.startswith('@'):
            x = func[1:].split(':')
            app_name = x[0]
            y = x[1].split('#')
            func_name = y[0]
            if len(y)>1:
                param = json_loads(y[1])
            module = importlib.import_module(app_name+'.tasks')
            func2 = getattr(module, func_name)
        else:
            func2 = func

        return func2(cproxy, *args, **kwargs)


###################################################################################################
class ProcessWorker(Process):
    def __init__(self, task_queue, input_queue, output_queue, worker_id):
        Process.__init__(self)
        self.worker_id = worker_id
        self.task_queue = task_queue
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, id, args, kwargs = self.task_queue.get()
            self.output_queue.put((id, 'status', 'start_process', {'worker_id': self.worker_id }))
            try:
                cproxy = CommunicationProxy(id, self.input_queue, self.output_queue)
                run_func(func, cproxy, args, kwargs)
                self.output_queue.put((id, 'status', 'end_process',{}))
            except Exception as e:
                print("Exception in:", func)
                print(e)
                self.output_queue.put((id, 'status', 'end_process_error', {}))
            self.task_queue.task_done()



class ThreadStatus(object):
    def __init__(self, manager, id, title, username):
        self.manager = manager
        self.id = int(id)
        self.title = title
        self.input_queue = None
        self.status = 0
        self.username = username
        self.time_from = datetime.datetime.now()
        self.time_to = None

    def __getitem__(self, item):
        if item in ('id', 'title', 'status', 'username', 'time_from', 'time_to'):
            return getattr(self, item)
        else:
            raise KeyError(key)
            return None

    def get_messages(self, start_id=0):
        return self.manager.get_messages(self.id, start_id)

    def pop_messages(self):
        return self.manager.pop_messages(self.id)


class ProcessManager():
    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.workers = []
        self.process_list = {}

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            temp_file_name = tmp.name
        self.db=sqlite3.connect(temp_file_name)
        self.cur = self.db.cursor()
        self.cur.execute("CREATE TABLE log(Id INTEGER, Value TEXT);")
        self.manager = None

    def _init_process_manager(self):
        self.manager = Manager()
        self.task_queue = self.manager.Queue()
        self.output_queue = self.manager.Queue()

        for process_id in range(self.num_threads):
            input_queue = self.manager.Queue()
            self.workers.append((process_id, input_queue))
            ProcessWorker(self.task_queue, input_queue, self.output_queue, process_id)

    def _add_task(self, func, id, args, kwargs):
        if not self.manager:
            self._init_process_manager()
        self.task_queue.put((func, id, args, kwargs))

    def _wait_completion(self):
        self.task_queue.join()

    def _process_output_queue(self):
        to_del = []
        if len(self.process_list)> _MAX_PROC_LOG:
            for key in self.process_list:
                if self.process_list[key].status in (2,3):
                    to_del.append(key)
            for key in to_del:
                del self.process_list[key]

        while 1:
            try:
                id, typ, group, argv = self.output_queue.get_nowait()
                if typ == 'status':
                    if group == 'start_process':
                        self.process_list[id].status=1
                        worker_id= argv['worker_id']
                        self.process_list[id].input_queue = self.workers[worker_id][1]
                    elif group == 'end_process':
                        self.process_list[id].status=2
                        self.process_list[id].time_to = datetime.datetime.now()
                    elif group ==  'end_process_error':
                        self.process_list[id].status=3
                elif typ == 'log':
                    self.cur.execute("INSERT INTO log(Id, Value) VALUES (?, ?);", (id, group))
                elif typ == 'system':
                    if group == 'add_task':
                        func= argv['func']
                        request_or_username = argv['request_or_username']
                        title= argv['title']
                        user_parm=argv['user_parm']
                        self.put(request_or_username, title, func, user_parm=user_parm)
                self.output_queue.task_done()
            except Empty:
                break


    def put(self, request_or_username, title, func, *args, **kwargs):
        global _ID
        _ID = _ID+1

        if type(request_or_username) == str:
            username = request_or_username
        else:
            if request_or_username.user.is_authenticated():
                username = request_or_username.user.username
            else:
                username = 'guest'

        self.process_list[_ID] = ThreadStatus(self, _ID, title, username)
        self._add_task(func, _ID, args, kwargs)
        return _ID

    def put_message(self, id, message):
        iid = int(id)
        if iid in self.process_list:
            self.process_list[iid].input_queue.put(message)
      
    def get_messages(self, id, id_start=0):
        iid = int(id)
        iid_start = int(id_start)

        tbl = self.cur.execute("SELECT Value from log where Id = ?;", (iid,) )
        if iid_start>0:
            self.cur.fetchmany(iid_start)
        ret=[]
        for pos in self.cur.fetchall():
            ret.append(pos[0])

        return ret

    def pop_messages(self, id):
        iid = int(id)
        ret = self.get_messages(iid)
        self.cur.execute("delete from where Id = ?;", (iid,) )
        return ret
    
    def kill_thread(self, id):
        iid = int(id)
        if iid in self.process_list:
            p = self.process_list[iid]
            if p.status == 1:
                p.input_queue.put("^C")

    def remove_thread(self, id):
        iid = int(id)
        self.kill_thread(iid)
        self.get_messages(iid)
    
    def list_threads(self, all=False):
        ret = []
        for key in self.process_list:
            p = self.process_list[key]
            if p.status in (0,1) or all:
                ret.append(p)
        return ret
 
    def thread_info(self, id):
        iid = int(id)
        if iid in self.process_list:
            return self.process_list[iid]
        else:
            return None


    def kill_all(self):
        threads = self.list_threads(all=True)
        for thread in threads:
            self.kill_thread(thread.id)


    def wait_for_result(self):
        if self.manager:
            self._wait_completion()
            tasks = self.list_threads(all=True)
            for task in tasks:
                msgs=self.get_messages(task.id)
            self._process_output_queue()
        return None

    def on_idle(self):
        if self.manager:
            self._process_output_queue()

def get_base_process_manager():
    return ProcessManager(2)

def get_process_manager():
    global _PROCESS_MANAGER
    if not _PROCESS_MANAGER:
        _PROCESS_MANAGER=get_base_process_manager()
    return _PROCESS_MANAGER

