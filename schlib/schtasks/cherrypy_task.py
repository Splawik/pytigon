import queue
import threading
import cherrypy
from cherrypy import log
from cherrypy.process import plugins
import schlib.schtasks.base_task as btask


class BackgroundTaskQueue(plugins.SimplePlugin):
    thread = None
    
    def __init__(self, bus):
        plugins.SimplePlugin.__init__(self, bus)
        self.pm = None


    def start(self):
        self.running = True
        if not self.pm:
            self.pm = btask.get_base_process_manager()
            self.bus.subscribe("put", self.pm.put)
            self.bus.subscribe("put_message", self.pm.put_message)
            self.bus.subscribe("get_messages", self.pm.get_messages)
            self.bus.subscribe("pop_messages", self.pm.pop_messages)
            self.bus.subscribe("kill_thread", self.pm.kill_thread)
            self.bus.subscribe("remove_thread", self.pm.remove_thread)
            self.bus.subscribe("list_threads", self.pm.list_threads)
            self.bus.subscribe("thread_info", self.pm.thread_info)
            self.bus.subscribe("kill_all", self.pm.kill_all)
            self.bus.subscribe("wait_for_result", self.pm.wait_for_result)


    def stop(self):
        if self.pm:
            #self.bus.log("BackgroundTaskQueue stop", level=40, traceback=True)
            self.bus.unsubscribe("put", self.pm.put)
            self.bus.unsubscribe("put_message", self.pm.put_message)
            self.bus.unsubscribe("get_messages", self.pm.get_messages)
            self.bus.unsubscribe("pop_messages", self.pm.pop_messages)
            self.bus.unsubscribe("kill_thread", self.pm.kill_thread)
            self.bus.unsubscribe("remove_thread", self.pm.remove_thread)
            self.bus.unsubscribe("list_threads", self.pm.list_threads)
            self.bus.unsubscribe("thread_info", self.pm.thread_info)
            self.bus.unsubscribe("kill_all", self.pm.kill_all)
            self.bus.unsubscribe("wait_for_result", self.pm.wait_for_result)
            self.pm = None


class CherryPyProcessManager():

    def _sig(self, sig, *args, **kwargs):
        ret = cherrypy.engine.publish(sig, *args, **kwargs)
        if len(ret)>0:
            return ret[0]
        else:
            return None

    def put(self, request_or_username, title, func, *args, **kwargs):
        return self._sig('put', request_or_username, title, func, *args, **kwargs)

    def put_message(self, id, message):
        return self._sig('put_message', id, message)

    def get_messages(self, id, id_start=0):
        return self._sig('get_messages', id, id_start)

    def pop_messages(self, id):
        return self._sig('pop_messages', id)

    def kill_thread(self, id):
        return self._sig('kill_thread', id)

    def remove_thread(self, id):
        return self._sig('remove_thread', id)

    def list_threads(self, all=False):
        return self._sig('list_threads', all)

    def thread_info(self, id):
        return self._sig('thread_info', id)

    def kill_all(self):
        return self._sig('kill_all')

    def wait_for_result(self):
        return self._sig('wait_for_result')


def subscribe():
    BackgroundTaskQueue(cherrypy.engine).subscribe()


def get_process_manager():
    if not btask._PROCESS_MANAGER:
        btask._PROCESS_MANAGER=CherryPyProcessManager()
    return btask._PROCESS_MANAGER
