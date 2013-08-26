"""Provides Cue entities and related helpers"""

from . import DictEntity,Entity

from fields import *

CUE_STARTER = "Delete Cue {CUE} <Confirm> Blind  Cue {CUE} Type {TYPE}"
CUE_END = "Label {LABEL} <enter> Record <enter>"

XF = CROSSFADE = 1
AF = ALLFADE = 2
BF = BLOCKING = 5
BLOCKING_STEP = 3

class Cue(DictEntity):
    _fields = (CUE,TYPE,UPTIME,DOWNTIME,UPWAIT,DOWNWAIT,LINK,FOLLOW,RATE,LEVELS,LABEL)
    _keyformat = CUE_STARTER+"""\n{LEVELS}
    Time {UPTIME} <enter> {DOWNTIME} Wait {UPWAIT} <enter> {DOWNWAIT}
    Link {LINK} <enter> S7 S2 {FOLLOW} S7 S5 {RATE}
    """+CUE_END
    def __init__(self,num,**kwargs):
        super(Cue,self).__init__(**kwargs)
        self[CUE] = num
        self[TYPE] = "<enter>"
        self[LEVELS] = Levels()
        self[FOLLOW] = "<clear>"

class SubroutineStep(DictEntity):
    _fields = (CUE,TYPE,LEVEL,UPTIME,DOWNTIME,FOLLOW)
    _keyformat = """
    S1 - + <enter> {CUE} <enter> <right> <right> {TYPE} {LEVEL}
    {UPTIME} <enter> {DOWNTIME} <enter> {FOLLOW}\n
    """
    def __init__(self,cue,type_=CROSSFADE,level=100,**kwargs):
        super(SubroutineStep,self).__init__(**kwargs)
        self[CUE] = cue
        self[TYPE] = type_
        self[LEVEL] = level
    
    def __setitem__(self,key,val):
        if key == TYPE:
            if val == BLOCKING:
                val = BLOCKING_STEP
        super(SubroutineStep,self).__setitem__(key,val)

class SubroutineCue(DictEntity):
    _fields = (CUE,STEPS,RATE,LABEL)
    _type = 4
    _keyformat = CUE_STARTER+"""\n{STEPS}
    S7 S3 {RATE} S7
    """+CUE_END
    def __init__(self,num,steps=tuple(),**kwargs):
        super(SubroutineCue,self).__init__(**kwargs)
        self[CUE] = num
        self[STEPS] = List(SubroutineStep,*steps)

    def _keys(self):
        if len(self.get(STEPS,[])) < 1:
            raise ValueError("Subroutine must have at least one step!")
        return super(SubroutineCue,self)._keys()

class EffectChannels(Levels):
    _channel_format = "Channel {c} S8 at {l}"

class EffectStep(DictEntity):
    _fields = (CHANNELS,TIME,UPTIME,DWELL,DOWNTIME,LOWLEVEL,HIGHLEVEL)
    _keyformat = """
    S1 - + <enter> \n{CHANNELS}
    S7 S2 S7 S7 {TIME} <enter>
    {UPTIME} <enter> {DWELL} <enter> {DOWNTIME} <enter>
    {LOWLEVEL} <enter> {HIGHLEVEL} <enter>
    """
    def __init__(self,channels={},**kwargs):
        super(EffectStep,self).__init__(**kwargs)
        self[CHANNELS] = EffectChannels(**channels)

class EffectCue(DictEntity):
    _fields = (CUE,STEPS,UPTIME,DOWNTIME,DWELL,LINK,FOLLOW,RATE,LABEL)
    _type = 3
    _keyformat = CUE_STARTER+"""\n{STEPS}
    Time {UPTIME} <enter> {DWELL} <enter> {DOWNTIME} <enter>
    Link {LINK} S7 S7 S2 {FOLLOW} S5 {RATE} S7
    """+CUE_END

    def __init__(self,num,steps=tuple(),**kwargs):
        super(EffectCue,self).__init__(**kwargs)
        self[CUE] = num
        self[STEPS] = List(EffectStep,*steps)
