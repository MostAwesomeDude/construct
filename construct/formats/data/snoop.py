"""
what : snoop v2 capture file.
 how : http://tools.ietf.org/html/rfc1761
 who : jesse @ housejunkie . ca
"""

import time
from construct import (Adapter, Enum, Field, HexDumpAdapter, Magic, OptionalGreedyRange,
        Padding, Struct, UBInt32)

class EpochTimeStampAdapter(Adapter):
    """ Convert epoch timestamp <-> localtime """

    def _decode(self, obj, context):
        return time.ctime(obj)
    def _encode(self, obj, context):
        return int(time.mktime(time.strptime(obj)))

packet_record = Struct("packet_record",
        UBInt32("original_length"),
        UBInt32("included_length"),
        UBInt32("record_length"),
        UBInt32("cumulative_drops"),
        EpochTimeStampAdapter(UBInt32("timestamp_seconds")),
        UBInt32("timestamp_microseconds"),
        HexDumpAdapter(Field("data", lambda ctx: ctx.included_length)),
        # 24 being the static length of the packet_record header
        Padding(lambda ctx: ctx.record_length - ctx.included_length - 24),
    )

datalink_type = Enum(UBInt32("datalink"),
        IEEE802dot3 = 0,
        IEEE802dot4 = 1,
        IEEE802dot5 = 2,
        IEEE802dot6 = 3,
        ETHERNET = 4,
        HDLC = 5,
        CHARSYNC = 6,
        IBMCHANNEL = 7,
        FDDI = 8,
        OTHER = 9,
        UNASSIGNED = 10,
    )

snoop_file = Struct("snoop",
        Magic("snoop\x00\x00\x00"),
        UBInt32("version"), # snoop v1 is deprecated
        datalink_type,
        OptionalGreedyRange(packet_record),
    )
