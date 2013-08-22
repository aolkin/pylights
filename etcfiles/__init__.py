"""Functionality for working with ETC's binary data files.

.. package:: etcfiles
    :synopsis: Provides functionality for representing and working with objects
        stored in binary files created by ETC software.

.. moduleauthor:: Aaron Olkin

"""

import struct

class Readable(object):
    """Inherit from this and define the following attributes and methods to make
    something "readable":

    @classmethod from_struct: A classmethod constructor called to build a class
    class attr _struct_format: a struct format string specifying the binary format
    class attr _struct_fields: a tuple mapping the fields returned from unpacking
        the binary struct to argument names passed into from_struct. Use None to
        indicate fields that should be ignored, and prefix fields that should be
        parsed into custom objects with *.
    class attr _struct_structs: A dictionary mapping field names to the custom
        classes on which from_string will be called.
    """

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
    def from_file(cls,fn,writeable=True):
        fd = open(fn,"rb")
        s = fd.read()
        fd.close()
        c = cls.from_string(s)
        if writeable and isinstance(c,Writeable):
            c._Writeable__filename = fn
        return c

    @classmethod
    def from_struct(cls,*args):
        raise NotImplementedError("Subclasses must implement from_struct!")

class Writeable(object):
    def to_string(self):
        t = list(self.to_struct())
        for n,i in enumerate(self._struct_fields):
            if i == None:
                t[n] = 0
            if i and i.startswith("*"):
                t[n] = t[n].to_string()
        return struct.pack(self._struct_format,*t)

    def write(self,fn=None):
        if not fn:
            try:
                fn = self.__filename
            except AttributeError:
                raise TypeError("Object has no filename, please provide one!")
        else:
            self.__filename = fn
        fd = open(fn,"wb")
        fd.write(self.to_string())
        fd.close()
        return True
