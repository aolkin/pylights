
### Field Type Constants
CUE = "CUE"
LABEL = "LABEL"
TYPE = "TYPE"
UPTIME = "UPTIME"
DOWNTIME = "DOWNTIME"
UPWAIT = "UPWAIT"
DOWNWAIT = "DOWNWAIT"
DWELL = "DWELL"
LINK = "LINK"
FOLLOW = "FOLLOW"
RATE = "RATE"
LEVEL = "LEVEL"
LEVELS = "LEVELS"
STEP = "STEP"
STEPS = "STEPS"
STYLE = "STYLE"
DWELL = "DWELL"
TIME = "TIME"
LOW = LOWLEVEL = "LOWLEVEL"
HIGH = HIGHLEVEL = "HIGHLEVEL"
CHANNELS = "CHANNELS"

### Validator function
def validateField(field,value):
    """
    Validates `value` as a value for a field of type `field`.

    It returns `True` if the field validates, and `False` if it doesn't. If
    :func:`validateField` does not validate the specified field, it returns `None`.
    """
    if field == LABEL:
        return False if len(value) > 16 else True
    elif field == LEVEL:
        return True if 0 <= value <= 100 else False
    elif field == LEVELS:
        return isinstance(value,Levels)

class Field():
    pass
class DictField(Field,dict):
    pass
class List(Field,list):
    def __init__(self,type_=None,*args,**kwargs):
        self._contains = type_
        for i in args:
            self._validate(i)
        list.__init__(self,*args)
        super(List,self).__init__(self,**kwargs)

    def __str__(self):
        out = ""
        for i in self:
            out += str(i)+"\n"
        return out
        
    def _validate(self,item):
        if self._contains and not isinstance(item,self._contains):
            raise TypeError("Supplied object is not of type '{}'!".format(
                self._contains.__name__))
            
    def append(self,item):
        self._validate(item)
        super(List,self).append(item)
        
    def __setitem__(self,key,val):
        self._validate(val)
        super(List,self).__setitem__(key,val)

### Complex Fields
class Levels(DictField):
    _channel_format = "Channel {chan} at {level}"

    def __str__(self):
        out = ""
        for i in self:
            if self[i] < 100:
                level = "{:02}".format(self[i])
            else:
                level = "Full"
            out += (" "*8)+self._channel_format.format(c=i,l=level)+"\n"
        return out
    
    def __setitem__(self,key,val):
        if type(key) != int or key > 192 or key < 1:
            raise KeyError("Invalid channel number! ({})".format(key))
        if not validateField(LEVEL,val):
            raise ValueError("Invalid level value! ({})".format(val))
        dict.__setitem__(self,key,val)
