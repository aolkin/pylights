from __future__ import print_function

import os, sys, time, struct, socket

from pylights.libs.six.moves import socketserver, queue

header_struct = struct.Struct("!BBH")

from pylights.daemon import commandprocessors
from pylights.daemon import handlers as message_handlers

class QueueTypeError(TypeError):
    pass

class QueueingError(queue.Full):
    pass

class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        header = self.rfile.read(4)
        while len(header) == 4:
            mtype,subtype,length = header_struct.unpack(header)
            data = self.rfile.read(length)
            self.process_message(mtype,subtype,data)
            try:
                header = self.rfile.read(4)
            except socket.error as err:
                print(err)
                header = ""

    def process_message(self,mtype,subtype,data):
        try:
            message_handlers.get(mtype)(self.server,subtype,data)
            self.wfile.write("\x00"*4)
        except Exception as err:
            error = repr(err)
            self.wfile.write(header_struct.pack(0xFF,0xFF,len(error)))
            self.wfile.write(error)

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
                self.processors.append(module.Processor(**self._cp.get_dict(m)))
                pqueue = self.processors[-1].get_queue()
                if not isinstance(pqueue,queue.Queue):
                    raise QueueTypeError(type(pqueue))
                self.queues.append(pqueue)
                self.processors[-1].start()
            except AttributeError:
                print("Invalid module {}, must define Processor() class".format(m))
            except QueueTypeError as err:
                print("Invalid queue type {}".format(err.args[0]))
        if len(self.queues) < 1:
            print("The server will not start because no queues registered successfully.")
            exit(3)
        try:
            self.serve_forever()
        except BaseException:
            for i in self.processors:
                print("Stopping {}".format(i.name))
                if i.stop(True,10):
                    print(i,"didn't die!")
