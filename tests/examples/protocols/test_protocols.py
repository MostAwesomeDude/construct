# # -*- coding: utf-8 -*-

import unittest, pytest, os
from declarativeunittest import raises
ontravis = 'TRAVIS' in os.environ

from construct import *
from construct.lib import *
from construct.examples.protocols import *

from io import BytesIO
import os, random, itertools, hashlib, binascii
ident = lambda x: x



class TestProtocols(unittest.TestCase):

    def commondump(self, format, filename):
        if ontravis:
            filename = "examples/protocols/" + filename
        if not ontravis:
            filename = "tests/examples/protocols/" + filename
        with open(filename,'rb') as f:
            data = f.read()
        obj = format.parse(data)
        print(obj)
        data = format.build(obj)
        print(data)

    def commonhex(self, format, hexdata):
        obj = format.parse(binascii.unhexlify(hexdata))
        print(obj)
        data = format.build(obj)
        print(data)


    def test_ethernet(self):
        self.commonhex(ethernet_header, b"0011508c283c0002e34260090800")

    def test_ip4(self):
        self.commonhex(ipv4_header, b"4500003ca0e3000080116185c0a80205d474a126")

    def test_ip6(self):
        self.commonhex(ipv6_header, b"6ff00000010206803031323334353637383941424344454646454443424139383736353433323130")

    def test_tcp(self):
        self.commonhex(tcp_header, b"0db5005062303fb21836e9e650184470c9bc0000")

    def test_udp(self):
        self.commonhex(udp_header, b"0bcc003500280689")


