
import queue, threading, time

class CommandProcessor(object):
    def __init__(self,**kwargs):
        """Set up any external threads, libraries, or processes, as well as the message queue"""
        self.queue = queue.Queue()
        tname = "Thread-{}-Worker".format(".".join(self.__class__.__module__.split(".")[2:]))
        self.thread = threading.Thread(target=self.worker,name=tname)
        self.is_running = False

    def get_queue(self):
        """Return the FIFO queue into which messages should be inserted."""
        return self.queue

    def worker(self,*args,**kwargs):
        """Process queued messages."""
        while self.is_running:
            try:
                message = self.queue.get_nowait()
                self.process(message)
                self.queue.task_done()
            except queue.Empty as err:
                time.sleep(0.2)

    def start(self):
        """Start the worker thread."""
        self.is_running = True
        self.thread.start()

    def stop(self,block=True,timeout=None):
        self.is_running = False
        if block:
            self.thread.join(timeout)
        return self.thread.is_alive()

    def process(self,message):
        raise NotImplementedError("process must be implemented by subclasses!")
