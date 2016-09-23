"""
Message Transport Part 3 (SS7 protocol stack)
(untested)
"""
from construct import *


mtp3_header = "mtp3_header" / BitStruct(
    "service_indicator" / Nibble,
    "subservice" / Nibble,
)

