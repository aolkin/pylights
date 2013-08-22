from __future__ import print_function
"""Uses easygui to present simple choices to test the sending of various entities"""

import easygui
from fields import *
#import sender, keys

def send_str(string):
    string = keys.parse_str(string)
    print("Sending {}".format(string))
    sender.send(string)
