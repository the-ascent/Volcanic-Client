import struct
def encodeMessageType(mtype):
    return struct.pack(">i",mtype)