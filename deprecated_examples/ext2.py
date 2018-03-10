"""
Extension 2 (ext2) used in Linux systems
"""

from construct import *

Char = SLInt8
UChar = ULInt8
Short = SLInt16
UShort = ULInt16
Long = SLInt32
ULong = ULInt32

BlockPointer = Struct(
    "block_number" / ULong,
    # WARNING: unnamed field?
    OnDemandPointer(this.block_number),
)

superblock = Struct(
    "inodes_count" / ULong,
    "blocks_count" / ULong,
    "reserved_blocks_count" / ULong,
    "free_blocks_count" / ULong,
    "free_inodes_count" / ULong,
    "first_data_block" / ULong,
    "log_block_size" / Enum(ULong, 
        OneKB = 0,
        TwoKB = 1,
        FourKB = 2,
    ),
    "log_frag_size" / Long,
    "blocks_per_group" / ULong,
    "frags_per_group" / ULong,
    "inodes_per_group" / ULong,
    "mtime" / ULong,
    "wtime" / ULong,
    "mnt_count" / UShort,
    "max_mnt_count" / Short,
    "magic" / Const(UShort, 0xEF53),
    "state" / UShort,
    "errors" / UShort,
    Padding(2),
    "lastcheck" / ULong,
    "checkinterval" / ULong,
    "creator_os" / ULong,
    "rev_level" / ULong,
    Padding(235*4),
)

group_descriptor = Struct(
    "block_bitmap" / ULong,
    "inode_bitmap" / ULong,
    "inode_table" / ULong,
    "free_blocks_count" / UShort,
    "free_inodes_count" / UShort,
    "used_dirs_count" / UShort,
    Padding(14),
)

inode = Struct(
    "mode" / FlagsEnum(UShort,
        IXOTH = 0x0001,
        IWOTH = 0x0002,
        IROTH = 0x0004,
        IRWXO = 0x0007,
        IXGRP = 0x0008,
        IWGRP = 0x0010,
        IRGRP = 0x0020,
        IRWXG = 0x0038,
        IXUSR = 0x0040,
        IWUSR = 0x0080,
        IRUSR = 0x0100,
        IRWXU = 0x01C0,
        ISVTX = 0x0200,
        ISGID = 0x0400,
        ISUID = 0x0800,
        IFIFO = 0x1000,
        IFCHR = 0x2000,
        IFDIR = 0x4000,
        IFBLK = 0x6000,
        IFREG = 0x8000,
        IFLNK = 0xC000,
        IFSOCK = 0xA000,
        IFMT = 0xF000,
    ),
    "uid" / UShort,
    "size" / ULong,
    "atime" / ULong,
    "ctime" / ULong,
    "mtime" / ULong,
    "dtime" / ULong,
    "gid" / UShort,
    "links_count" / UShort,
    "blocks" / ULong,
    "flags" / FlagsEnum(ULong,
        SecureDelete = 0x0001,
        AllowUndelete = 0x0002,
        Compressed = 0x0004,
        Synchronous = 0x0008,
    ),
    Padding(4),
    # WARNING: doubled name
    "blocks" / ULong[12],
    "indirect1_block" / ULong,
    "indirect2_block" / ULong,
    "indirect3_block" / ULong,
    "version" / ULong,
    "file_acl" / ULong,
    "dir_acl" / ULong,
    "faddr" / ULong,
    "frag" / UChar,
    "fsize" / UChar,
    Padding(10),
)

# special inodes
EXT2_BAD_INO = 1
EXT2_ROOT_INO = 2
EXT2_ACL_IDX_INO = 3
EXT2_ACL_DATA_INO = 4
EXT2_BOOT_LOADER_INO = 5
EXT2_UNDEL_DIR_INO = 6
EXT2_FIRST_INO = 11 

directory_record = Struct(
    "inode" / ULong,
    "rec_length" / UShort,
    "name_length" / UShort,
    "name" / Bytes(this.name_length),
    Padding(this.rec_length - this.name_length),
)
