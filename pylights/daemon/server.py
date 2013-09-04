from __future__ import print_function

import os, sys, time, queue

from pylights.libs.six.moves import socketserver

from pylights.daemon import commands
from pylights.daemon import commandprocessors

class QueueingError(queue.Full):
    pass

class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        pass

class Server(socketserver.ThreadingMixIn,socketserver.TCPServer,object):
    @classmethod
    def from_cp(cls,config):
        c = cls((config.server_host,
                 config.server_root_port if os.geteuid() == 0 else config.server_port),
                Handler)
        c._cp = config
        c.modules = []
        for i in commandprocessors.modules:
            if config.modules.get(i.__name__.rpartition(".")[-1]):
                c.modules.append(i)
        return c

    def queue_message(self,message):
        errors = []
        for i in self.queues:
            try:
                i.put(message,True,10)
            except queue.Full as err:
                errors.append(err)
        raise QueueingError(errors)

    def start(self):
        self.processors = []
        self.queues = []
        for module in self.modules:
            m = module.__name__.split(".")[-1]
            try:
                self.processors.append(m.Processor(**self._cp.get_dict(m)))
                pqueue = self.processors[-1].get_queue()
                if not isinstance(pqueue,queue.Queue):
                    raise TypeError(type(pqueue))
                self.queues.append(pqueue)
            except AttributeError:
                print("Invalid module {}, must define Processor() class".format(m))
            except TypeError as err:
                print("Invalid queue type {}".format(err.args[0]))
        if len(self.queues) < 1:
            print("The server will not start because no queues registered successfully.")
            exit(3)
        #self.serve_forever()
