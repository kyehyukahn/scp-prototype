from .application import BaseApplication
from utils import logger
from queue import Queue
import threading
import time


class LockedQueue(Queue):
    def __init__(self, maxsize=0):
        super(LockedQueue, self).__init__(maxsize)
        self.lock = threading.Lock()

    def push_queue(self, element):
        self.lock.acquire()
        self.put(element)
        self.lock.release()
        return

    def pop_queue(self):
        self.lock.acquire()
        element = self.get()
        self.lock.release()
        return element


class Executor(threading.Thread):
    def __init__(self, application, action_queue):
        assert isinstance(application, BaseApplication)
        assert isinstance(action_queue, LockedQueue)

        super(Executor, self).__init__()
        self.application = application
        self.action_queue = action_queue

        self.log = logger.get_logger('executor', node=self.application.node.name)

    def run(self):
        while True:
            if self.action_queue.empty():
                time.sleep(1)
            else:
                element = self.action_queue.pop_queue()
                assert isinstance(element, tuple)
                func_name = element[0]
                arg = element[1]

                if not hasattr(self.application, func_name):
                    self.log.error('%s method is not exist in Consensus object' % func_name)
                func = getattr(self.application, func_name)
                if arg is not None:
                    func(arg)
                else:
                    func()
        return True


class EventManager():
    def __init__(self, application):
        assert isinstance(application, BaseApplication)

        self.application = application
        self.action_queue = LockedQueue()
        t = Executor(self.application, self.action_queue)
        t.start()

    def push_element(self, func_name, arg):
        self.action_queue.push_queue((func_name, arg))
