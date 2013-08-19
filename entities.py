from __future__ import division, unicode_literals

import sender
import keys


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
        return self.keystr

    def send(self):
        sender.send(self._keys())
