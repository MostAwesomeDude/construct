"""
What : Internet Group Management Protocol, Version 2
 How : http://www.ietf.org/rfc/rfc2236.txt
 Who : jesse @ housejunkie . ca
"""

from construct import (
    Byte,
    Enum,
    Struct,
    UBInt16,
    UBInt32,
)
from construct.protocols.layer3.ipv4 import IpAddress

igmp_type = Enum(Byte("igmp_type"), 
    MEMBERSHIP_QUERY = 0x11,
    MEMBERSHIP_REPORT_V1 = 0x12,
    MEMBERSHIP_REPORT_V2 = 0x16,
    LEAVE_GROUP = 0x17,
)

igmpv2_header = Struct("igmpv2_header",
    igmp_type,
    Byte("max_resp_time"),
    UBInt16("checksum"),
    IpAddress("group_address"),
)

if __name__ == '__main__':
    
    capture = "1600FA01EFFFFFFD".decode("hex")
    print igmpv2_header.parse(capture)
