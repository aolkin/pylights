from pylights.daemon.server import main

import argparse

cl_parser = argparse.ArgumentParser("launchdaemon",
                                    description="Run a PyLights command processing server.")
cl_parser.add_argument('configfile',help="The configuration to use")
args = cl_parser.parse_args()

main(**vars(args))
