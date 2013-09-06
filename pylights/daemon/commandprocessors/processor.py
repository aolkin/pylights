
import threading, time

from pylights.libs.six.moves import queue

class CommandProcessor(object):
    def __init__(self,**kwargs):
        """Set up any external threads, libraries, or processes, as well as the message queue"""
        self.queue = queue.Queue()
        self.name = ".".join(self.__class__.__module__.split(".")[2:])
        tname = "Thread-{}-Worker".format(self.name)
        self.thread = threading.Thread(target=self.worker,name=tname)
        self._is_running = False

    def get_queue(self):
        """Return the FIFO queue into which messages should be inserted."""
        return self.queue

    def worker(self,*args,**kwargs):
        """Process queued messages."""
        while self._is_running:
            try:
                message = self.queue.get_nowait()
                self.process(message)
                self.queue.task_done()
            except queue.Empty as err:
                time.sleep(0.2)

    def start(self):
        """Start the worker thread."""
        if getattr(self,"load",None):
            try:
                self.load()
            except Exception as err:
                self.stop()
                raise Exception(err)
        self._is_running = True
        self.thread.start()

    def stop(self,block=True,timeout=None):
        self._is_running = False
        if block and self.is_running:
            self.thread.join(timeout)
        if getattr(self,"shutdown",None):
            self.shutdown()
        return self.is_running

    @property
    def is_running(self):
        return self.thread.is_alive()

    @is_running.setter
    def is_running(self,run):
        if run and not self.is_running:
            self.start()
        if not run and self.is_running:
            if self.stop(timeout=10):
                raise RuntimeError("Failed to stop worker thread!")

    def process(self,message):
        raise NotImplementedError("process must be implemented by subclasses!")
