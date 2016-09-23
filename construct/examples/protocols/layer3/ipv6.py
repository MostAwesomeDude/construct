"""
Internet Protocol version 6 (TCP/IP protocol stack)
"""

from construct import *


def ProtocolEnum(code):
    return Enum(code,
        ICMP = 1,
        TCP = 6,
        UDP = 17,
    )

class Ipv6AddressAdapter(Adapter):
    def _encode(self, obj, context):
        return [int(part, 16) for part in obj.split(":")]
    def _decode(self, obj, context):
        return ":".join("%02x" % b for b in obj)

Ipv6Address = Ipv6AddressAdapter(Byte[16])


ipv6_header = "ip_header" / Struct(
    EmbeddedBitStruct(
        "version" / OneOf(BitsInteger(4), [6]),
        "traffic_class" / BitsInteger(8),
        "flow_label" / BitsInteger(20),
    ),
    "payload_length" / Int16ub,
    "protocol" / ProtocolEnum(Int8ub),
    "hoplimit" / Int8ub,
    Alias("ttl", "hoplimit"),
    "source" / Ipv6Address,
    "destination" / Ipv6Address,
)


if __name__ == "__main__":
    o = ipv6_header.parse()
    print(o)
    print(repr(ipv6_header.build(o)))

