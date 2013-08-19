
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

### Validator function
def validateField(field,value):
    if field == LABEL:
        return False if len(value) > 16 else True
    elif field == LEVEL:
        return True if 0 <= value <= 100 else False
    elif field == LEVELS:
        return isinstance(value,Levels)

class Field(dict):
    pass

### Complex Fields
class Levels(Field):
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
