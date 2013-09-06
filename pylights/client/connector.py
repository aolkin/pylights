from __future__ import division

import os, sys, time, socket, struct

header_struct = struct.Struct("!BBH")

NULL = 0x00

class Client(object):
    def __init__(self,host,port):
        self.address = (host,port)

    def __enter__(self):
        self.sock = socket.create_connection(self.address,None)
        return self

    def send_message(self,mtype,subtype,data):
        d = bytes(data)
        header = header_struct.pack(mtype,subtype,len(d))
        self.sock.sendall(header+d)
        header = self.sock.recv(4)
        if len(header) == 4:
            if header == "\x00"*4:
                return True
            xFF,xFF,length = header_struct.unpack(header)
            return self.sock.recv(length)

    def send_raw(self,message):
        self.send_message(0x10,NULL,message)

    def send_sequence(self,sequence):
        single_byte = (max(sequence) < 256)
        fmt_char = "B" if single_byte else "H"
        try:
            self.send_message(0x12,int(not single_byte),struct.pack("!{}{}".format(
                        len(sequence),fmt_char),*sequence))
        except struct.error as err:
            raise ValueError("{} is outside the range of supported commands!".format(
                    max(sequence)))

    def __exit__(self,*ignore):
        self.sock.close()
