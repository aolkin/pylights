"""Helps in mapping nice representations to SendKeys-compatible keystroke strings."""

class KeyMap(dict):
    def addkeys(self,d):
        """
        This accepts a single argument, which should be a dictionary of the form::

            {
                '<key(s)>': '<name>',
                '<key(s)>': ('<name1>','<name2>')
            }

        It will iterate over this dictionary, adding maps for each key/key sequence
        from the name or names specified. A real example of this can be seen in the
        :ref:`default-names-content`.
        """
        for i in d:
            if isinstance(d[i],(list,tuple)):
                self.addkey(i,*d[i])
            else:
                self.addkey(i,d[i])
    def addkey(self,key,*names):
        """This maps one or more names to a single key."""
        if len(names) < 1:
            raise ValueError("Must provide at least one name!")
        for k in names:
            self[k] = key
    def addseq(self,seq,*names):
        """
        This maps one or more names to a specially formatted sequence. Use this method
        when you want to map a key sequence that uses existing keys or sequences.
        
        To include existing keys/sequences in your new sequence, simply enclose their
        names in `<` and `>`.
        """
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
    'f': ('full','fl'),
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
    'w': 'wait',
    '{SPACE}':'space',
    '+=': ('+','plus')
})

### Softkeys
for i in range(1,9):
    names.addkey('^{{F{i}}}'.format(i=i),'soft{}'.format(i),
                 'softkey{}'.format(i),'s{}'.format(i))

### Built-In Sequences
# Maps several names to pressing "enter" twice.
names.addseq("<enter><enter>","confirm","confirmed","dblenter","enterenter","doubleenter")

# Maps "forcestage" to a sequence that should put the console in stage mode no matter what.
names.addseq("<stage><macroenter><clear><stage>","forcestage")

# Maps "save" to the sequence needed to execute the "Write All to Disk" action.
names.addseq("<setup>3<enter>1<enter><enter><stage>","save")

# Maps "reset" to a sequence that will execute a system reset.
names.addseq("<setup>4<enter><s1><enter>","reset")

names.addseq("<blind><s6>","deletecue")
names.addseq("<blind><sub><s6>","deletesub","deletesubmaster")

# Maps "pause" to twenty presses of the space key, which is ignored by EOL.
names.addseq("<space>"*20,"pause")

def get(name,strict=False):
    """
    Looks up a name in :data:`names`.

    It will lowercase its argument before performing the lookup, and if it finds nothing it
    simply returns its argument as-is. As long as `strict` is `False`, it will also remove
    spaces from its argument. This allows easy lookups of button presses with multi-word names.
    """
    if not strict:
        name = name.replace(" ","")
    return names.get(name.lower(),name)

def list_to_str(keys):
    """
    Performs :func:`get` lookups on a list and :meth:`joins <str.join>` the result together
    with spaces.
    """
    return " ".join([get(i) for i in keys])

def parse_str(keys):
    """
    Accepts a single string argument. This should be a nice human-readable sequence of button
    presses, which will be converted into a string of key strokes suitable for sending to
    :term:`EOL`.

    It is extremely flexible, and can take almost anything you can throw at it. It will accept
    any capitalization and spacing, and will even catch multi-word button names. However, if
    a multi-word button name's first word is itself a button name, it will treat it as that
    button.

    :func:`parse_str` even allows you to add `<` and `>` around button names, in which case
    they will simply be ignored. However, as of now, there is no way to include comments in
    a keystring.

    Examples::

        >>> parse_str('Cue 7 Go')
        'q 7 ^g'
        >>> parse_str('Channel 1 at 50 '+
                      'Channel 2 at 75 '+
                      'Channel 5 at 27 '+
                      'Record cue 7 \\n Cue 7 <GO>')
        'c 1 a 50 c 2 a 75 c 5 a 27 r q 7 q 7 ^g'
        >>> parse_str('AB Go <stage> AB Clear')
        '^g +{F1} ^a'
    """
    keylist = []
    keys = keys.replace("<"," ").replace(">"," ").split()
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
        elif pos == 6 or pos == -5:
            keylist.append(orig_key)
    return list_to_str(keylist)
            
    
        
