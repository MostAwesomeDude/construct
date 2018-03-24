"""
Master Boot Record
The first sector on disk, contains the partition table, bootloader, et al.

http://www.win.tue.nl/~aeb/partitions/partition_types-1.html
"""

from construct import *

mbr_format = Struct(
    "bootloader_code" / Bytes(446),
    "partitions" / Array(4, Struct(
        "state" / Enum(Byte,
            INACTIVE = 0x00,
            ACTIVE = 0x80,
        ),
        "beginning" / BitStruct(
            "head" / BitsInteger(8),
            "sect" / BitsInteger(6),
            "cyl" / BitsInteger(10),
        ),
        "type" / Enum(Byte,
            Nothing = 0x00,
            FAT12 = 0x01,
            XENIX_ROOT = 0x02,
            XENIX_USR = 0x03,
            FAT16_old = 0x04,
            Extended_DOS = 0x05,
            FAT16 = 0x06,
            NTFS = 0x07,
            FAT32 = 0x0B,
            FAT32_LBA = 0x0C,
            ExtendedWithLBA = 0x0F,
            LINUX_SWAP = 0x82,
            LINUX_NATIVE = 0x83,
        ),
        "ending" / BitStruct(
            "head" / BitsInteger(8),
            "sect" / BitsInteger(6),
            "cyl" / BitsInteger(10),
        ),
        "sector_offset" / Int32ub, # offset from MBR in sectors
        "size" / Int32ub, # in sectors
    )),
    "signature" / Const(b"\x55\xAA"),
)
