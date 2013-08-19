from entities import DictEntity,Entity

from fields import *

class CrossfadeCue(DictEntity):
    _fields = (CUE,TYPE,UPTIME,DOWNTIME,UPWAIT,DOWNWAIT,LINK,FOLLOW,RATE,LEVELS,LABEL)
    _keyformat = """
    Delete Cue {e[CUE]} <Confirm> Blind
    Cue {e[CUE]} Type {e[TYPE]} <enter>
    {e[LEVELS]}
    Time {e[UPTIME]} <enter> {e[DOWNTIME]} Wait {e[UPWAIT]} <enter> {e[DOWNWAIT]}
    Link {e[LINK]} <enter> S7 S2 {e[FOLLOW]} S7 S5 {e[RATE]}
    Label {e[LABEL]} {{F6}} <enter> Record <enter>
    """
    def __init__(self,num,*args,**kwargs):
        super(CrossfadeCue,self).__init__(*args,**kwargs)
        self[CUE] = num
        self[LEVELS] = Levels()
        self[FOLLOW] = "<clear>"

Cue = CrossfadeCue
