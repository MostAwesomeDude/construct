"""
Internet Protocol version 4 (TCP/IP protocol stack)
"""
from construct import *


class IpAddressAdapter(Adapter):
    def _encode(self, obj, context):
        return list(map(int, obj.split(".")))
    def _decode(self, obj, context):
        return "{0}.{1}.{2}.{3}".format(*obj)
IpAddress = IpAddressAdapter(Byte[4])

def ProtocolEnum(code):
    return Enum(code,
        ICMP = 1,
        TCP = 6,
        UDP = 17,
    )

ipv4_header = "ip_header" / Struct(
    EmbeddedBitStruct(
        "version" / Const(Nibble, 4),
        "header_length" / ExprAdapter(Nibble, 
            decoder = lambda obj, ctx: obj * 4, 
            encoder = lambda obj, ctx: obj / 4
        ),
    ),
    "tos" / BitStruct(
        "precedence" / BitsInteger(3),
        "minimize_delay" / Flag,
        "high_throuput" / Flag,
        "high_reliability" / Flag,
        "minimize_cost" / Flag,
        Padding(1),
    ),
    "total_length" / Int16ub,
    "payload_length" / Computed(this.total_length - this.header_length),
    "identification" / Int16ub,
    EmbeddedBitStruct(
        "flags" / Struct(
            Padding(1),
            "dont_fragment" / Flag,
            "more_fragments" / Flag,
        ),
        "frame_offset" / BitsInteger(13),
    ),
    "ttl" / Int8ub,
    "protocol" / ProtocolEnum(Int8ub),
    "checksum" / Int16ub,
    "source" / IpAddress,
    "destination" / IpAddress,
    "options" / Bytes(this.header_length - 20),
)


