"""
Transmission Control Protocol (TCP/IP protocol stack)
"""
from construct import *



tcp_header = "tcp_header" / Struct(
    "source" / Int16ub,
    "destination" / Int16ub,
    "seq" / Int32ub,
    "ack" / Int32ub,
    EmbeddedBitStruct(
        "header_length" / ExprAdapter(Nibble, 
            encoder = lambda obj, ctx: obj / 4,
            decoder = lambda obj, ctx: obj * 4,
        ),
        Padding(3),
        "flags" / Struct(
            "ns"  / Flag,
            "cwr" / Flag,
            "ece" / Flag,
            "urg" / Flag,
            "ack" / Flag,
            "psh" / Flag,
            "rst" / Flag,
            "syn" / Flag,
            "fin" / Flag,
        ),
    ),
    "window" / Int16ub,
    "checksum" / Int16ub,
    "urgent" / Int16ub,
    "options" / Bytes(this.header_length - 20),
)


