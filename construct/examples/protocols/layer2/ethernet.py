"""
Ethernet (TCP/IP protocol stack)
"""
from construct import *
from construct.lib import *



class MacAddressAdapter(Adapter):
    def _encode(self, obj, context):
        return [int(part, 16) for part in obj.split("-")]
    def _decode(self, obj, context):
        return "-".join("%02x" % b for b in obj)

MacAddress = MacAddressAdapter(Byte[6])


ethernet_header = "ethernet_header" / Struct(
    "destination" / MacAddress,
    "source" / MacAddress,
    "type" / Enum(Int16ub,
        IPv4 = 0x0800,
        ARP = 0x0806,
        RARP = 0x8035,
        X25 = 0x0805,
        IPX = 0x8137,
        IPv6 = 0x86DD,
        default = Pass,
    ),
)


