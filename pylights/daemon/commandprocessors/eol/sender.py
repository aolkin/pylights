"""

Notes: 
    >>> from ctypes import *; c=cdll.LoadLibrary("libxdo.so.2"); t = c.xdo_new(":0");
    >>> h = c_uint(); w = c_uint();
    >>> c.xdo_get_viewport_dimensions(t,byref(w),byref(h),0)
"""
