"""Packages that recieve commands and process them"""

from importlib import import_module
import sys

__all__ = ["eol","midi","history"]

def _module_sort_function(m):
    p = getattr(m,"priority",-1)
    if p < 0:
        p = sys.maxsize+p
    return p

modules = [import_module("."+i,__name__) for i in __all__]
modules.sort(key=_module_sort_function)
