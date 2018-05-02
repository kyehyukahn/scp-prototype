import threading
import time


class Timer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # default delay set..
        self.delay = 1
        self.state = True
        self.handler = None

    def setDelay(self, delay):
        self.delay = delay

    def run(self):
        while self.state:
            time.sleep(self.delay)
            if self.handler is not None:
                self.handler()

    def end(self):
        self.state = False
        self.handler = None

    def setHandler(self, handler):
        self.handler = handler
