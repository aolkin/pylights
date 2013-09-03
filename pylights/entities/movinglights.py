
from . import Entity,DictEntity

from keys import names

from fields import *

from etcfiles.personality import Personality

from entities.cues import EffectStep

names.addseq("<setup>15<enter>2<enter>","fixturepatch","movinglightpatch")
names.addseq("<softkey8>","fixture","movinglight")

class Fixture():

    def __init__(self,personality,channel):
        self.prs = personality
        self.channel = channel
        self.basedict = {}
        for i in self.prs.channels:
            self.basedict[i.type] = int((i.home/255)*100) if i.home else 0
        self.channels = self.basedict.copy()

    def setLevels(self,levels):
        for i in self.prs.channels:
            levels[self.channel+i.dimmer] = self.channels[i.type]

    def generateEffectSteps(self,from_,to_,in_,list_,stepargs={}):
        if len(from_) != len(to_):
            raise TypeError("Length of from and to dictionaries are not equal!")
        dists = {}
        for i in from_:
            dists[i] = float(to_[i]-from_[i])/in_
        for i in range(in_+1):
            cdists = dists.copy()
            step = EffectStep(LOWLEVEL="Full",HIGHLEVEL="Full",**stepargs)
            list_.append(step)
            for c in self.prs.channels:
                if c.type in cdists:
                    step[CHANNELS][c.dimmer+self.channel] = int(from_[c.type]+cdists[c.type]*i)
                    del cdists[c.type]
