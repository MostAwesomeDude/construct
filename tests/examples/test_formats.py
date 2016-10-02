# -*- coding: utf-8 -*-

import unittest, pytest, os
from declarativeunittest import raises
ontravis = 'TRAVIS' in os.environ

from construct import *
from construct.lib import *
from construct.examples.formats import *

from io import BytesIO
import os, random, itertools, hashlib, binascii
from binascii import hexlify, unhexlify
ident = lambda x: x



class TestFormats(unittest.TestCase):

    def commondump(self, format, filename):
        if ontravis:
            filename = "examples/formats/" + filename
        if not ontravis:
            filename = "tests/examples/formats/" + filename
        with open(filename,'rb') as f:
            data = f.read()
        self.commonbytes(format, data)

    def commonhex(self, format, hexdata):
        self.commonbytes(format, binascii.unhexlify(hexdata))

    def commonbytes(self, format, bytesdata):
        obj = format.parse(bytesdata)
        print(obj)
        data = format.build(obj)
        print(hexlify(bytesdata))
        print(hexlify(data))
        # assert hexlify(bytesdata) == hexlify(data)



    def test_png(self):
        self.commondump(png_file, "sample.png")

    def test_emf(self):
        self.commondump(emf_file, "emf1.emf")

    def test_bitmap(self):
        self.commondump(bitmap_file, "bitmap1.bmp")
        self.commondump(bitmap_file, "bitmap4.bmp")
        self.commondump(bitmap_file, "bitmap8.bmp")
        self.commondump(bitmap_file, "bitmap24.bmp")

    def test_mbr(self):
        self.commondump(mbr_format, "mbr1")

    def test_cap(self):
        self.commondump(cap_file, "cap2.cap")

    def test_snoop(self):
        self.commondump(snoop_file, "snoop1")

