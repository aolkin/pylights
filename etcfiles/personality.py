"""Reads and writes ETC's .prs Personality files."""

from collections import Sequence

from . import Readable,Writeable

class PChannel(Writeable,Readable):
    _struct_format = ">B3bBBBB"
    _struct_fields = ("attrs",None,None,None,"atype","home","dispformat","dimmer")
    _attributes = {"independent":"Independent","LTP":"LTP","sixteenbit":"16 Bit",
                   "flipped":"Flipped"}

    @classmethod
    def from_struct(cls,attrs,atype,home,dispformat,dimmer):
        return cls(atype,dimmer,home,dispformat,attrs)

    def to_struct(self):
        return (self.attrs,None,None,None,self.atype,self.home,self.dispformat,self.dimmer)

    def __init__(self,atype,dimmer,home=0,dispformat=0,attrs=None,
                 independent=False,LTP=False,sixteenbit=False,flipped=False):
        self.atype = atype
        self.__dimmer = dimmer
        self.home = home
        self.dispformat = dispformat
        self.independent = independent
        self.LTP = LTP
        self.sixteenbit = sixteenbit
        self.flipped = flipped
        if attrs:
            self.attrs = attrs

    @property
    def dimmer(self):
        return self.__dimmer

    @property
    def attrs(self):
        return int(("1" if self.flipped else "0")+("1" if self.sixteenbit else "0")+
                   ("1" if self.LTP else "0")+("1" if self.independent else "0"),2)

    @attrs.setter
    def attrs(self,a):
        self.independent = (a & 1) != 0
        self.LTP = (a & 2) != 0
        self.sixteenbit = (a & 4) != 0
        self.flipped = (a & 8) != 0

    def niceattrs(self):
        attrs = []
        for i in self._attributes:
            if getattr(self,i):
                attrs.append(self._attributes[i])
        if len(attrs) < 2:
            return "".join(attrs)+(" " if len(attrs) > 0 else "")
        elif len(attrs) == 2:
            return " and ".join(attrs)+" "
        else:
            return ", ".join(attrs[:-1])+", and "+attrs[-1]+" "

    def __str__(self):
        return "<{}{} Channel on Dimmer {}>".format(
            self.niceattrs(),_attribute_types[self.atype],self.dimmer+1)
    __repr__ = __str__

class Personality(Writeable,Readable):
    class __ChannelList(Sequence):
        def __init__(self,l):
            self.__list = []
            for i in l:
                self.add(i)
        
        def add(self,channel):
            if type(channel) != PChannel:
                raise TypeError("Can only add {} objects.".format(PChannel))
            n = channel.dimmer+1
            if channel.dimmer == len(self.__list):
                self.__list.append(channel)
            elif n > len(self.__list):
                for i in range(len(self.__list),n):
                    self.add(PChannel(0,i))
            self.__list[channel.dimmer] = channel
            
        def __getitem__(self,key):
            return self.__list.__getitem__(key)

        def __len__(self):
            return len(self.__list)

        def __repr__(self):
            return "{}({})".format(self.__class__.__name__,self.__list)

    _struct_format = ">3lH12sbB"+("8s"*64)
    _struct_fields = (None,None,None,"numchannels","label",None,"remdim")+(("*channels",)*64)
    _struct_structs = dict(channels=PChannel)

    @classmethod
    def from_struct(cls,numchannels,label,remdim,channels):
        return cls(label,channels[:numchannels],remdim)

    def to_struct(self):
        return ( (None,None,None,len(self.channels),self.label,None,self.remote_dimmer)+
                 tuple(self.channels)+
                 tuple(PChannel(0,0) for i in range(64-len(self.channels))) )

    def __init__(self,label="",channels=[],remdim=False):
        self.channels = channels
        self.label = label
        self.remote_dimmer = remdim

    def __setattr__(self,key,val):
        if key == "label":
            if len(val) > 12:
                raise ValueError("Label length must not exceed 12 characters!")
        if key == "remote_dimmer":
            if 1 < int(val) or int(val) < 0:
                raise ValueError("RemoteDimmer must be a Boolean value!")
        super(Personality,self).__setattr__(key,val)

    def addChannel(self,atype,dimmer=None,**kwargs):
        if dimmer == None:
            dimmer = len(self.__channels)
        self.__channels.add(PChannel(atype,dimmer,**kwargs))

    @property
    def channels(self):
        return self.__channels

    @channels.setter
    def channels(self,c):
        self.__channels = Personality.__ChannelList(c)


_attribute_types = [
    "Not Used",
    "Intensity",
    "Pan",
    "Tilt",
    "Color",
    "Color 2",
    "Cyan",
    "Magenta",
    "Yellow",
    "Gobo",
    "Gobo Rotation",
    "Gobo 2",
    "Gobo 2 Rotation",
    "F/X",
    "F/X Rotation",
    "Prism",
    "Strobe",
    "Zoom",
    "Focus",
    "Iris",
    "Frost",
    "Pan Rotation",
    "Tilt Rotation",
    "Beam 1A",
    "Beam 1B",
    "Beam 2A",
    "Beam 2B",
    "Beam 3A",
    "Beam 3B",
    "Beam 4A",
    "Beam 4B",
    "Beam Rotation",
    "Speed",
    "Speed 2",
    "Control",
    "Control 2",
    "Clear Function 2",
    "Gobo Function",
    "Gobo Function 2",
    "Macro",
    "Reserved 5",
    "Reserved 4",
    "Reserved 3",
    "Reserved 2",
    "Reserved 1",
    "Clear Function",
    "Lens Width (?)",
    "Checksum",
    "User 17",
    "User 16",
    "User 15",
    "User 14",
    "User 13",
    "User 12",
    "User 11",
    "User 10",
    "User 9",
    "User 8",
    "User 7",
    "User 6",
    "User 5",
    "User 4",
    "User 3",
    "User 2",
    "User 1"
]

_display_types = [
    "Percent",
    "Raw",
    "Hex",
    "Text"
]
