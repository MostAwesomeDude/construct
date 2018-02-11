from declarativeunittest import *
from construct import *
from construct.lib import *
from construct.examples.formats import *


def test_png():
    commondump(png_file, "sample.png")

@xfail(reason="Enum no longer supports default")
def test_emf():
    commondump(emf_file, "emf1.emf")

def test_bitmap():
    commondump(bitmap_file, "bitmap1.bmp")
    commondump(bitmap_file, "bitmap4.bmp")
    commondump(bitmap_file, "bitmap8.bmp")
    commondump(bitmap_file, "bitmap24.bmp")

def test_wmf():
    commondump(wmf_file, "wmf1.wmf")

def test_gif():
    commondump(gif_file, "sample.gif")

def test_mbr():
    commondump(mbr_format, "mbr1")

def test_cap():
    commondump(cap_file, "cap2.cap")

def test_snoop():
    commondump(snoop_file, "snoop1")

def test_pe32():
    commondump(pe32_file, "python.exe")
    commondump(pe32_file, "NOTEPAD.EXE")
    commondump(pe32_file, "sqlite3.dll")

@xfail(reason="Enum no longer supports default")
def test_elf32():
    commondump(elf32_file, "ctypes.so")
