"""Package for sending commands to EOL inside of Xvfb"""

priority = 10

from pylights.daemon.commandprocessors.processor import CommandProcessor
from pylights.daemon.commandprocessors.eol import xkeys

import sys, os, time
from subprocess import *

CHECK_FOR_XVFB = ["which","Xvfb"]
CHECK_FOR_WINE = ["which","wine"]
XVFB_COMMAND = ["Xvfb",":{}","-screen","0","800x600x16"]
EOL_COMMAND = ["wine","winx2.exe"]
EOL_CWD = os.path.join(os.path.abspath(os.path.dirname(__file__)),"eol311")

class Processor(CommandProcessor):
    def __init__(self,server=0,macrofile=None,**kwargs):
        try:
            check_output(CHECK_FOR_XVFB)
            check_output(CHECK_FOR_WINE)
        except CalledProcessError as err:
            raise RuntimeError("Missing required software: {}".format(err.cmd[1]))
        super(Processor,self).__init__(**kwargs)
        self.xserver = server
        self.env = os.environ.copy()
        self.env["DISPLAY"] = ":{}".format(server)
        self._xvfb_command = XVFB_COMMAND[:]
        self._xvfb_command[1] = self._xvfb_command[1].format(server)
        self.args = kwargs
        self.xvfb = None
        self.eol = None
        self.mfile = macrofile

    def load(self):
        xvfb_fd = open(os.devnull if self.args.get("disablexvfblogging") else
                       "logs/{}.xvfb.log".format(self.xserver),"w")
        if self.args.get("disabledxvfblogging") == "stdout":  xvfb_fd = None
        wine_fd = open(os.devnull if self.args.get("disablewinelogging") else
                       "logs/eol.wine.log","w")
        if self.args.get("disabledwinelogging") == "stdout":  wine_fd = None
        self.xvfb = Popen(self._xvfb_command,stdout=xvfb_fd,stderr=STDOUT)
        tries = 0
        while not self.eol or self.eol.poll():
            time.sleep(0.5)
            if self.eol:
                print(self.eol,self.eol.poll())
                self.eol.terminate()
            tries += 1
            if tries > 5:
                self.eol.terminate()
                raise RuntimeError("Failed to start EOL!")
            self.eol = Popen(EOL_COMMAND,stdout=wine_fd,stderr=STDOUT,
                             cwd=EOL_CWD,env=self.env)
            time.sleep(0.5)
        self.sender = XKeySender("Screen 1",self.env)
        self.eol_load_file(self.mfile)

    def shutdown(self):
        self.eol.terminate()
        self.xvfb.terminate()

    def eol_load_file(self,filename=None):
        fn = list(map(lambda k: xkeys.punctuation.get(k,k),
                      tuple(filename if filename else "macros.shw")))
        call(['xdotool',"search","--sync","--name","Expression Off-Line - untitled.shw",
              "windowraise","mousemove","10","30","click","--clearmodifiers","1"]+
             ("key Down Down Return Tab Shift+Tab".split(" "))+fn+["Return"],env=self.env)
        call(['xdotool',"search","--sync","--name","Screen 1","windowraise"],env=self.env)

class XKeySender:
    def __init__(self,windowtitle,environ):
        self.windowtitle = windowtitle
        self.env = environ
        self.window = int(check_output(['xdotool','search','--sync','--name',
                                        "{}".format(windowtitle)],env=self.env))

    def sendkeys(self, keys):
        call(['xdotool',"key","--window",str(self.window),"--clearmodifiers"]+list(keys),
             env=self.environ)

    def screenshot(self, name):
        if name == None: return
        homedir = os.environ['HOME']
        call(['xdotool','windowraise',str(self.window)],env=self.env)
        time.sleep(0.05)
        call(['import','-window',"{}".format(self.windowtitle),
              '$HOME/htdocs/{fname}{png}'.format(fname=name)],env=self.env)
