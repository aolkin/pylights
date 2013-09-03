import struct

class Readable(object):
    @classmethod
    def from_string(cls,string):
        """Takes a bytestring and returns an object loaded from that bytestring."""
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
        try:
            return cls(**d)
        except TypeError:
            return cls.from_struct(**d)

    @classmethod
    def from_file(cls,fn,writeable=True):
        """
        A wrapper around :meth:`from_string`, this takes a filename and an optional boolean
        flag. It reads from the specified file and then calls :meth:`from_string` on its
        contents, and returns the result.

        Additionally, if the optional boolean `writeable` is True and the class inherits from
        Writeable, the specified filename will be remembered for when the object is written
        to a file.
        """
        fd = open(fn,"rb")
        s = fd.read()
        fd.close()
        c = cls.from_string(s)
        if writeable and isinstance(c,Writeable):
            c._Writeable__filename = fn
        return c

    @classmethod
    def from_struct(cls,**args):
        """
        This classmethod must be overwritten. It will be called to create a new object
        from a file with arguments as defined in :attr:`_struct_fields
        """
        raise NotImplementedError("Subclasses must implement from_struct!")

class Writeable(object):
    def to_string(self):
        """Returns a :mod:`struct` packed bytestring of the object."""
        t = list(self.to_struct())
        if getattr(self,"_struct_fields"):
            for n,i in enumerate(self._struct_fields):
                if i == None:
                    t[n] = 0
                if i and i.startswith("*"):
                    t[n] = t[n].to_string()
        return struct.pack(self._struct_format,*t)

    def write(self,fn=None):
        """
        A wrapper around :meth:`to_string`, this writes the data returned by :meth:`to_string`
        to the specified file, or, if none is specified and a filename was remembered when
        loading the object from a file, that remembered filename will be used.

        Returns True on success, for no particular reason.
        """
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
