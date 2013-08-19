"""Uses easygui to present simple choices to test the sending of various entities"""

import easygui
from fields import *
import sender, keys

def send_str(string):
    sender.send(keys.parse_str(string))
