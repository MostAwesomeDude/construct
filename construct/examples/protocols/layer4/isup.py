"""
ISDN User Part (SS7 protocol stack)
"""
from construct import *


isup_header = "isup_header" / Struct(
    "routing_label" / Bytes(5),
    "cic" / Int16ub,
    "message_type" / Int8ub,
    # mandatory fixed parameters
    # mandatory variable parameters
    # optional parameters
)

