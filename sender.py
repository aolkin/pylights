
import pywinauto

import sys
if sys.version_info.major < 3:
    from Tkinter import Tk
    from tkMessageBox import showinfo,showwarning
else:
    from tkinter import Tk
    from tkinter.messagebox import showinfo

tkroot = Tk()
tkroot.withdraw()

title = "Expression Off-Line - .*"

app = pywinauto.application.Application()
app.connect_(title_re=title)

win = app.window_(title_re=title)

config = dict(alertshown=False)

def send(keys,speed=0.01,noalert=False):
    win.Maximize()
    if not (config["alertshown"] or noalert):
        win.SetFocus()
        showwarning("Keep EOL Focused!","Please leave the EOL window focused until your entire script has been sent!\n(The window will be restored when the script is sent.)",parent=tkroot)
    win.SetFocus()
    win.TypeKeys(keys,speed)
    win.Restore()
    if not (config["alertshown"] or noalert):
        showinfo("Done!","Your entire script has been sent to EOL!",parent=tkroot)
        config["alertshown"] = True
