"""
User Datagram Protocol (TCP/IP protocol stack)
"""
from binascii import unhexlify

from construct import *


udp_header = "udp_header" / Struct(
    "header_length" / Computed(lambda ctx: 8),
    "source" / Int16ub,
    "destination" / Int16ub,
    "payload_length" / ExprAdapter(Int16ub, 
        encoder = lambda obj, ctx: obj + 8,
        decoder = lambda obj, ctx: obj - 8,
    ),
    "checksum" / Int16ub,
)


