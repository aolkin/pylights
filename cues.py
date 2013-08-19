from entities import DictEntity,Entity

from fields import *

CUE_STARTER = """
    Delete Cue {e[CUE]} <Confirm> Blind
    Cue {e[CUE]} Type {e[TYPE]} <enter>
"""

class Cue(DictEntity):
    _fields = (CUE,TYPE,UPTIME,DOWNTIME,UPWAIT,DOWNWAIT,LINK,FOLLOW,RATE,LEVELS,LABEL)
    _keyformat = CUE_STARTER+"""
    {e[LEVELS]}
    Time {e[UPTIME]} <enter> {e[DOWNTIME]} Wait {e[UPWAIT]} <enter> {e[DOWNWAIT]}
    Link {e[LINK]} <enter> S7 S2 {e[FOLLOW]} S7 S5 {e[RATE]}
    Label {e[LABEL]} <enter> Record <enter>
    """
    def __init__(self,num,**kwargs):
        super(Cue,self).__init__(**kwargs)
        self[CUE] = num
        self[LEVELS] = Levels()
        self[FOLLOW] = "<clear>"


class SubroutineStep(DictEntity):
    _fields = (CUE,TYPE,LEVEL,UPTIME,DOWNTIME,FOLLOW)
    _keyformat = """
    S1 - + <enter> {e[CUE]} <enter> <right> <right> {e[TYPE]} {e[LEVEL]}
    {e[UPTIME]} <enter> {e[DOWNTIME]} <enter> {e[FOLLOW]}\n
    """
    def __init__(self,cue,type_=1,level=100,**kwargs):
        super(SubroutineStep,self).__init__(**kwargs)
        self[CUE] = cue
        self[TYPE] = type_
        self[LEVEL] = level

class SubroutineCue(DictEntity):
    _fields = (CUE,STEPS,RATE,LABEL)
    _type = 4
    _keyformat = CUE_STARTER+"""
    {e[STEPS]}
    S7 S3 {e[RATE]} S7
    Label {e[LABEL]} <enter> Record <enter>
    """
    def __init__(self,num,steps=tuple(),**kwargs):
        super(SubroutineCue,self).__init__(**kwargs)
        self[CUE] = num
        self[STEPS] = List(SubroutineStep,*steps)

    def _keys(self):
        if len(self.get(STEPS,[])) < 1:
            raise ValueError("Subroutine must have at least one step!")
        return super(SubroutineCue,self)._keys()
