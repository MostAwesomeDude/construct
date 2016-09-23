"""
What : Internet Group Management Protocol, Version 2
 How : http://www.ietf.org/rfc/rfc2236.txt
 Who : jesse @ housejunkie . ca
"""

from construct import Byte, Enum,Struct, UBInt16
from construct.protocols.layer3.ipv4 import IpAddress
from binascii import unhexlify


igmp_type = "igmp_type" / Enum(Byte, 
    MEMBERSHIP_QUERY = 0x11,
    MEMBERSHIP_REPORT_V1 = 0x12,
    MEMBERSHIP_REPORT_V2 = 0x16,
    LEAVE_GROUP = 0x17,
)

igmpv2_header = "igmpv2_header" / Struct(
    igmp_type,
    "max_resp_time" / Byte,
    "checksum" / Int16ub,
    "group_address" / IpAddress,
)

if __name__ == '__main__':
    capture = unhexlify(b"1600FA01EFFFFFFD")
    print (igmpv2_header.parse(capture))


