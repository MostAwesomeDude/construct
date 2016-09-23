"""
TCP/IP Protocol Stack

WARNING: before parsing the application layer over a TCP stream, you must 
first combine all the TCP frames into a stream. See utils.tcpip for some solutions
"""
from construct import *
from construct.lib import *
from construct.protocols.layer2.ethernet import ethernet_header
from construct.protocols.layer3.ipv4 import ipv4_header
from construct.protocols.layer3.ipv6 import ipv6_header
from construct.protocols.layer4.tcp import tcp_header
from construct.protocols.layer4.udp import udp_header



layer4_tcp = Struct("layer4_tcp",
    Rename("header", tcp_header),
    HexDumpAdapter(
        Field("next", lambda ctx:
            ctx["_"]["header"].payload_length - ctx["header"].header_length
        )
    ),
)

layer4_udp = Struct("layer4_udp",
    Rename("header", udp_header),
    HexDumpAdapter(
        Field("next", lambda ctx: ctx["header"].payload_length)
    ),
)

layer3_payload = Switch("next", lambda ctx: ctx["header"].protocol,
    {
        "TCP" : layer4_tcp,
        "UDP" : layer4_udp,
    },
    default = Pass
)

layer3_ipv4 = Struct("layer3_ipv4",
    Rename("header", ipv4_header),
    layer3_payload,
)

layer3_ipv6 = Struct("layer3_ipv6",
    Rename("header", ipv6_header),
    layer3_payload,
)

layer2_ethernet = Struct("layer2_ethernet",
    Rename("header", ethernet_header),
    Switch("next", lambda ctx: ctx["header"].type,
        {
            "IPv4" : layer3_ipv4,
            "IPv6" : layer3_ipv6,
        },
        default = Pass,
    )
)

ip_stack = Rename("ip_stack", layer2_ethernet)





if __name__ == "__main__":
	# in file dumps

    obj = ip_stack.parse(cap1)
    print (obj)
    print (repr(ip_stack.build(obj)))

    obj = ip_stack.parse(cap2)
    print (obj)
    print (repr(ip_stack.build(obj)))


