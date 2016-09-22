# -*- coding: utf-8 -*-

import unittest
from declarativeunittest import raises
import pytest

from construct import *
from construct.lib import *
from construct.examples.formats import *

from io import BytesIO
import os, random, itertools
import hashlib
ident = lambda x: x
ontravis = 'TRAVIS' in os.environ



class TestFormats(unittest.TestCase):

    def common(self, format, filename):
        if ontravis:
            filename = "examples/" + filename
        if not ontravis:
            filename = "tests/examples/" + filename
        with open(filename,'rb') as f:
            data = f.read()
        obj = format.parse(data)
        print(repr(obj))
        data = format.build(obj)
        print(data)

    @pytest.mark.xfail(reason="parses fine but building fails")
    def test_png(self):
        self.common(png_file, "sample.png")

    def test_emf(self):
        self.common(emf_file, "emf1.emf")

    def test_bitmap(self):
        self.common(bitmap_file, "bitmap1.bmp")
        self.common(bitmap_file, "bitmap4.bmp")
        self.common(bitmap_file, "bitmap8.bmp")
        self.common(bitmap_file, "bitmap24.bmp")

    def test_mbr(self):
        self.common(mbr_format, "mbr1")

    @pytest.mark.xfail(reason="parses fine but building fails")
    def test_cap(self):
        self.common(cap_file, "cap2.cap")

    def test_snoop(self):
        self.common(snoop_file, "snoop1")


