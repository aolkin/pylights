
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

### Validator function
def validateField(field,value):
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
    def __str__(self):
        out = ""
        for i in self:
            out += "Channel {} at ".format(i)
            if self[i] < 100:
                out += "{:02}\n".format(self[i])
            else:
                out += "Full\n"
        return out
    
    def __setitem__(self,key,val):
        if type(key) != int or key > 192 or key < 1:
            raise KeyError("Invalid channel number! ({})".format(key))
        if not validateField(LEVEL,val):
            raise ValueError("Invalid level value! ({})".format(val))
        dict.__setitem__(self,key,val)
