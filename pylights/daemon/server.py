from __future__ import print_function

import os, sys, time, threading

from pylights.libs import configreader
from pylights.daemon import commands
from pylights.daemon import commandprocessors

def main(configfile):
    config = configreader.Configuration(configfile)
    print(dir(commandprocessors))
