from declarativeunittest import *
from construct import *
from construct.lib import *
from construct.examples.formats import *


class TestFormats(unittest.TestCase):

    def test_png(self):
        commondump(png_file, "sample.png")

    def test_emf(self):
        commondump(emf_file, "emf1.emf")

    def test_bitmap(self):
        commondump(bitmap_file, "bitmap1.bmp")
        commondump(bitmap_file, "bitmap4.bmp")
        commondump(bitmap_file, "bitmap8.bmp")
        commondump(bitmap_file, "bitmap24.bmp")

    def test_wmf(self):
        commondump(wmf_file, "wmf1.wmf")

    def test_gif(self):
        commondump(gif_file, "sample.gif")

    def test_mbr(self):
        commondump(mbr_format, "mbr1")

    def test_cap(self):
        commondump(cap_file, "cap2.cap")

    def test_snoop(self):
        commondump(snoop_file, "snoop1")

    def test_pe32(self):
        commondump(pe32_file, "python.exe")
        commondump(pe32_file, "NOTEPAD.EXE")
        commondump(pe32_file, "sqlite3.dll")

    def test_elf32(self):
        commondump(elf32_file, "ctypes.so")
