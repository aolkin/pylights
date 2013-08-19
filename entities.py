from __future__ import division, unicode_literals

import sender, keys, fields

class Entity:

    @classmethod
    def from_keylist(keylist):
        return Entity(keys.list_to_str(keylist))

    def __init__(self,keys):
        self.keystr = keys

    def __str__(self):
        return self._keys()

    def __repr__(self):
        cls = self.__class__
        return '<{}.{} \'{}\' at {:x}>'.format(cls.__module__,cls.__name__,
                                               str(self),id(self))
        return object.__repr__(self).replace("object",str(self))

    def _keys(self):
        if hasattr(self,"keystr"):
            return self.keystr
        else:
            raise NotImplementedError("Subclasses must implement _keys")

    def send(self):
        sender.send(self._keys())


class DictEntity(Entity,dict):
    __init__ = dict.__init__

    def _keys(self):
        if not hasattr(self,"_keyformat"):
            raise NotImplementedError("Subclasses must define _keyformat")
        return keys.parse_str(self._keyformat.format(e=self))

    def __getitem__(self,key):
        if key == fields.TYPE:
            if hasattr(self,"_type"):
                return self._type
        if self.get(key) != None:
            if key == fields.LABEL:
                return "{F6} "+dict.__getitem__(self,key).replace(" ","{SPACE}")
            if key == fields.LEVEL:
                if self.get(key) == 100: return "Full"
                else: return "{:02}".format(self.get(key))
            return dict.__getitem__(self,key)
        elif key not in self._fields:
            raise KeyError("{} does not have a {} field!".format(self.__class__.__name__,key))
        else:
            return ""

    def __setitem__(self,key,val):
        if key not in self._fields:
            raise KeyError("'{}' is an invalid {} field!".format(key,self.__class__.__name__))
        if fields.validateField(key,val) == False:
            raise TypeError("Supplied value is invalid for {} field!".format(key))
        dict.__setitem__(self,key,val)
