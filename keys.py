from __future__ import unicode_literals, division

class KeyMap(dict):
    def addkeys(self,d):
        for i in d:
            if isinstance(d[i],(list,tuple)):
                self.addkey(i,*d[i])
            else:
                self.addkey(i,d[i])
    def addkey(self,key,*names):
        if len(names) < 1:
            raise ValueError("Must provide at least one name!")
        for k in names:
            self[k] = key
    def addseq(self,seq,*names):
        seq = seq.replace("{","{{").replace("}","}}")
        seq = seq.replace("<","{").replace(">","}")
        key = seq.format(**self)
        self.addkey(key,*names);

names = KeyMap()
names.addkeys({
    '^d': ('abback','back'),
    '^a': 'abclear',
    '^g': ('abgo','go'),
    '^f': 'abhold',
    '^s': 'abrate',
    '{F3}': 'about',
    'n': 'and',
    'a': 'at',
    '^k': 'blackout',
    '+{F2}': ('blind','blindmode'),
    '^c': 'cdback',
    '^z': 'cdclear',
    '^b': 'cdgo',
    '^v': 'cdhold',
    '^x': 'cdrate',
    'c': ('channel','chan','ch'),
    '{DELETE}': 'clear',
    'q': 'cue',
    'd': ('dimmer','dim'),
    '{DOWN}': ('down','downarrow'),
    '{ENTER}': 'enter',
    'x': 'except',
    '+{F8}': 'expand',
    '+{F3}': 'fader',
    '!': ('focuspoint','fp'),
    'f': 'full',
    'g': 'group',
    '?': 'help',
    'b': 'label',
    '{F4}': 'learn',
    '{LEFT}': ('left','leftarrow'),
    'v': 'level',
    '{PGDN}': ('levelwheeldown','leveldown','wheeldown'),
    '{PGUP}': ('levelwheelup','levelup','wheelup'),
    'k': 'link',
    '#': ('loadsub','loadsubmaster'),
    'm': ('macro*','m*'),
    '^e': ('macroenter','menter'),
    '^w': ('macrowait','mwait'),
    'o': 'only',
    'j': ('page','subpage','submasterpage'),
    '+{F6}': 'park',
    'p': 'part',
    '+{F5}': 'patch',
    '{END}': ('ratedown','ratewheeldown'),
    '{HOME}': ('rateup','ratewheelup'),
    'r': ('record','rec'),
    'l': ('release','rel'),
    '{RIGHT}': ('right','rightarrow'),
    '+{F7}': 'setup',
    'u': 'solobump',
    '+{F1}': 'stage',
    'e': ('submode','submastermode'),
    's': ('sub','submaster'),
    '{F2}': 'swap',
    't': ('thru','through'),
    'i': 'time',
    '^': 'track',
    '+{F4}': 'tracksheet',
    '*': 'type',
    '{UP}': ('up','uparrow'),
    'w': 'wait'
})
for i in range(1,9):
    names.addkey('^{{F{i}}}'.format(i=i),'soft{}'.format(i),
                 'softkey{}'.format(i),'s{}'.format(i))
names.addseq("<stage><macroenter><clear><stage>","forcestage")
names.addseq("<setup>3<enter>1<enter><enter><stage>","save")
names.addseq("<setup>4<enter><s1><enter>","reset")
names.addseq("<blind><s6>","deletecue")
names.addseq("<blind><sub><s6>","deletesub","deletesubmaster")

def get(name,strict=False):
    if not strict:
        name = name.replace(" ","")
    return names.get(name.lower(),name)

def list_to_str(keys):
    return " ".join([get(i) for i in keys])

def parse_str(keys):
    keylist = []
    keys = keys.split()
    keys.reverse()
    while len(keys) > 0:
        orig_key = key = keys.pop()
        pos = 0
        while 1 > pos > -5:
            if get(key) != key:
                keylist.append(key)
                pos = 5
            else:
                pos -= 1
                try:
                    key += keys[pos]
                    if get(key) != key:
                        keylist.append(key)
                        pos = pos*-1
                except IndexError:
                    pos = 6
        if 5 > pos > 0:
            for i in range(pos):
                keys.pop()
        elif pos == 6:
            keylist.append(orig_key)
    return list_to_str(keylist)
            
    
        
