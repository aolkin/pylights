from pylights.daemon.server import Server
from pylights.daemon.commandprocessors import modules
from pylights.libs import configreader

import argparse, os

executable_modules = []
for i in modules:
    if getattr(i,"execute_command_line",None):
        executable_modules.append(i.__name__.split(".")[-1])

cl_parser = argparse.ArgumentParser("launchdaemon",
                                    description="Run a PyLights command processing server.")
cl_parser.add_argument('-f',help="The configuration to use",nargs=1,dest="configfile",
                       required=False if len(executable_modules) > 0 else True)
if len(executable_modules) > 0:
    cl_parser.add_argument('-m',choices=executable_modules,dest="module",
                           help="Run command processor module commands")
args = cl_parser.parse_args()
if len(executable_modules) > 0 and args.module:
    from importlib import import_module
    m = import_module("pylights.daemon.commandprocessors."+args.module)
    m.execute_command_line()
elif args.configfile:
    config = configreader.Configuration(args.configfile)
    server = Server.from_cp(config)
    server.start()
else:
    print("Much specify either a configuration file or a module command!")
    exit(2)
