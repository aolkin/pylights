
import struct

def unhandleable(*ignore,**more_ignore):
     raise NotImplementedError("Requested message type cannot be handled!")

def get(key):
    return globals().get("message_0x{:0>2x}".format(key),unhandleable)

def message_0x00(server,stype,data):
    raise NotImplementedError("Guess what? They don't exist...RTM")

def message_0x10(server,stype,data):
    ### Do string parsing of `data` here!
    # server.queue_message(parsed_data)
    pass

def message_0x12(server,stype,data):
    if not stype in (0,1):
        raise ValueError("0x12 Subtype must be 0x00 or 0x01")
    server.queue_message(struct.unpack("!{}{}".format(len(data)/(stype+1),
                                                      "H" if stype else "B"),data))
