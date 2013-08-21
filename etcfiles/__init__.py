"""Functionality for working with ETC's binary data files."""

import struct

class Readable(object):
    @classmethod
    def from_string(cls,string):        
        t = struct.unpack(cls._struct_format,string)
        d = {}
        for n,i in enumerate(cls._struct_fields):
            if i:
                o = t[n]
                if i.startswith("*"):
                    i = i[1:]
                    o = cls._struct_structs[i].from_string(o)
                if d.get(i,False):
                    if type(d[i]) == list:
                        d[i].append(o)
                    else:
                        d[i] = [d[i]]
                        d[i].append(o)
                else:
                    d[i] = o
        return cls.from_struct(**d)

    @classmethod
    def from_file(cls,fn):
        fd = open(fn,"rb")
        s = fd.read()
        fd.close()
        return cls.from_string(s)

class Writeable(object):
    def save(self,fn):
        pass
