import pywinauto

title = "Expression Off-Line - .*"

app = pywinauto.application.Application()
app.connect_(title_re=title)

win = app.window_(title_re=title)

def send(keys):
    win.Maximize()
    win.TypeKeys(keys,0.05)
    win.Restore()
