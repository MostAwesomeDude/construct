"""
Transmission Control Protocol (TCP/IP protocol stack)
"""
from construct import *
from binascii import unhexlify
import six


tcp_header = Struct("tcp_header",
    UBInt16("source"),
    UBInt16("destination"),
    UBInt32("seq"),
    UBInt32("ack"),
    EmbeddedBitStruct(
        ExprAdapter(Nibble("header_length"), 
            encoder = lambda obj, ctx: obj / 4,
            decoder = lambda obj, ctx: obj * 4,
        ),
        Padding(3),
        Struct("flags",
            Flag("ns"),
            Flag("cwr"),
            Flag("ece"),
            Flag("urg"),
            Flag("ack"),
            Flag("psh"),
            Flag("rst"),
            Flag("syn"),
            Flag("fin"),
        ),
    ),
    UBInt16("window"),
    UBInt16("checksum"),
    UBInt16("urgent"),
    Field("options", lambda ctx: ctx.header_length - 20),
)

if __name__ == "__main__":
    cap = unhexlify(six.b("0db5005062303fb21836e9e650184470c9bc0000"))
    
    obj = tcp_header.parse(cap)
    print (obj)
    built = tcp_header.build(obj)
    print (built)
    assert cap == built
















