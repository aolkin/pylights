from __future__ import division, unicode_literals

import pickle

import sender, keys, fields

ENTITY_MODULE = __name__

STRINGS = (str,getattr(__builtins__,"unicode",None))

class Entity:
    @classmethod
    def from_keylist(keylist):
        return Entity(keys.list_to_str(keylist))

    @classmethod
    def from_nice(string):
        return Entity(keys.parse_str(string))

    def __init__(self,keys):
        self.keystr = keys

    def __str__(self):
        return self._keys()

    def __repr__(self):
        cls = self.__class__
        return '{}.{}(\'{}\')'.format(cls.__module__,cls.__name__,self._keys())

    def _keys(self):
        if hasattr(self,"keystr"):
            return self.keystr
        else:
            raise NotImplementedError("Subclasses must implement _keys")

    def send(self):
        sender.send(self._keys())

class _NoFormatFakeDict:
    def __init__(self,name):
        self._name = name
    def __getitem__(self,key):
        return "{{{}[{}]}}".format(self._name,key)

class DictEntity(Entity,dict):

    __init__ = dict.__init__

    def __str__(self):
        if not hasattr(self,"_keyformat"):
            raise NotImplementedError("Subclasses must define _keyformat")
        fieldkeys = {}
        for i in dir(fields):
            if i.isupper():
                fieldkeys[i] = "{{e[{}]}}".format(getattr(fields,i))
        return self._keyformat.format(e=_NoFormatFakeDict("e"),**fieldkeys).format(e=self)

    def _keys(self):
        return keys.parse_str(str(self))

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

    def __setattr__(self,key,val):
        if key.upper() in self._fields:
            self[key.upper()] = val
        else:
            super(DictEntity,self).__setattr__(key,val)

    def __getattr__(self,key):
        if key.upper() in self._fields:
            return self[key.upper()]
        else:
            return self.__getattribute__(key)

    def save(self,f=None,nice=None):
        if not f:
            if not getattr(self,"_f",None):
                raise ValueError("This entity does not have a filename yet, please "+
                                 "supply one!")
            f = self._f
        self._f = f
        if nice == None:
            if getattr(self,"_nice",None) != None:
                nice = self._nice
        else:
            self._nice = nice
        if type(f) in STRINGS:
            f = open(f,"w" if nice else "wb")
        if nice:
            f.write(str(self))
        else:
            f.truncate(0)
            pickle.dump(self,f,pickle.HIGHEST_PROTOCOL)
