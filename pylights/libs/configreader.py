from pylights.libs.six.moves import configparser

class Configuration(object):

    def __init__(self,fn=None,cp=None,section=None):
        if cp:
            self._cp = cp
        else:
            self._cp = configparser.ConfigParser()
        if fn:
            self._cp.read(fn)
        self._section = section

    def get(self,key,default=None,strict=False,raw=False):
        if self._section:
            key = self._section+"_"+key
        sect,_,opt = key.partition("_")
        section = sect.title()
        option = opt.replace("_","").lower()

        if not option:
            return Configuration(cp=self._cp,section=section)
        if not strict:
            if not self._cp.has_option(section,option):
                return default
        if raw:
            return self._cp.get(section,option)

        try:
            return self._cp.getboolean(section,option)
        except ValueError:
            val = self._cp.get(section,option)
            try:
                return int(val)
            except ValueError:
                try:
                    return float(val)
                except ValueError:
                    return val

    def __getattr__(self,key):
        if key in ("_cp","get","_section"):
            return object.__getattr__(self,key)
        
        return self.get(key,strict=True)
