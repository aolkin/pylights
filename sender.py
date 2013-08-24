"""This module handles sending virtual keystrokes to Expression Off-Line."""

import sys

# Attempt to detect if documentation is being build, in which case
# errors may be ignored.
import os
IS_MAKING = os.environ.get("MAKELEVEL") == "1"

TITLE_RE = "Expression Off-Line - .*"

config = dict(alertshown=False)

try:
    import pywinauto.application
    app = pywinauto.application.Application()
    app.connect_(title_re=TITLE_RE)
    win = app.window_(title_re=TITLE_RE)
except ImportError as err:
    if not IS_MAKING:
        raise err

if sys.version_info.major < 3:
    from Tkinter import Tk,TclError
    from tkMessageBox import showinfo,showwarning
else:
    from tkinter import Tk,TclError
    from tkinter.messagebox import showinfo

try:
    tkroot = Tk()
    tkroot.withdraw()
except TclError as err:
    if not IS_MAKING:
        raise err


def send(keys,speed=0.01,noalert=False):
    """
    :param keys: a :meth:`SendKeys <pywinauto.controls.HwndWrapper.HwndWrapper.TypeKeys>`\
    compatible keystring to send to :term:`EOL`.
    :param speed: How long to wait between virtual keypresses. 0.01 seconds usually works.\
    See :meth:`SendKeys <pywinauto.controls.HwndWrapper.HwndWrapper.TypeKeys>` for more\
    information.
    :param noalert: if `True`, disables the dialog boxes before and after sending keystrokes.

    :meth:`send` maximizes the back :term:`EOL` window and gives focus to :term:`EOL` before
    sending any keystrokes. It is important that it retains focus until all keystrokes have
    been sent, or unexpected results may occur. As long as `noalert` is `False`, the first
    time this function is called it will pop up a dialog box saying so.

    Once all keystrokes have been sent, the back :term:`EOL` window will be restored, and
    if `noalert` is `False` and it is the first time this function has been called, a dialog
    box will pop up to alert the user that it is done.
    """
    if not (config["alertshown"] or noalert):
        win.Maximize()
        win.SetFocus()
        showwarning("Keep EOL Focused!","Please leave the EOL window focused until your entire script has been sent!\n(The window will be restored when the script is sent.)",parent=tkroot)
    win.Maximize()
    win.SetFocus()
    win.TypeKeys(keys,speed)
    win.Restore()
    if not (config["alertshown"] or noalert):
        showinfo("Done!","Your entire script has been sent to EOL!",parent=tkroot)
        config["alertshown"] = True
