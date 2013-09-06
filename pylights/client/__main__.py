from pylights.daemon.server import Server
from pylights.client.connector import Client
from pylights.libs import configreader

import argparse, os

cl_parser = argparse.ArgumentParser("client",
                                    description="Connect and send commands to a PyLights server.")
cl_parser.add_argument('-f',help="The configuration to use",nargs=1,dest="configfile",
                       required=True)

args = cl_parser.parse_args()
config = configreader.Configuration(args.configfile)
client = Client(config.server_host,config.server_port)
