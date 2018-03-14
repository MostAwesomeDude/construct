from construct import *

docs = """
PE/COFF format as used on Windows to store EXE DLL SYS files. This includes 64-bit and .NET code.

Microsoft specifications:
https://msdn.microsoft.com/en-us/library/windows/desktop/ms680547(v=vs.85).aspx
https://msdn.microsoft.com/en-us/library/ms809762.aspx
Format tutorial breakdown at:
http://blog.dkbza.org/
https://drive.google.com/file/d/0B3_wGJkuWLytQmc2di0wajB1Xzg/view
https://drive.google.com/file/d/0B3_wGJkuWLytbnIxY1J5WUs4MEk/view

Authored by Arkadiusz Bulski, under same license.
"""

msdosheader = Struct(
    "signature" / Const(b"MZ"),
    "lfanew" / Pointer(0x3c, Int16ul),
)

coffheader = Struct(
    "signature" / Const(b"PE\x00\x00"),
    "machine" / Enum(Int16ul,
        UNKNOWN = 0x0,
        AM33 = 0x1d3,
        AMD64 = 0x8664,
        ARM = 0x1c0,
        ARM64 = 0xaa64,
        ARMNT = 0x1c4,
        EBC = 0xebc,
        I386 = 0x14c,
        IA64 = 0x200,
        M32R = 0x9041,
        MIPS16 = 0x266,
        MIPSFPU = 0x366,
        MIPSFPU16 = 0x466,
        POWERPC = 0x1f0,
        POWERPCFP = 0x1f1,
        R4000 = 0x166,
        RISCV32 = 0x5032,
        RISCV64 = 0x5064,
        RISCV128 = 0x5128,
        SH3 = 0x1a2,
        SH3DSP = 0x1a3,
        SH4 = 0x1a6,
        SH5 = 0x1a8,
        THUMB = 0x1c2,
        WCEMIPSV2 = 0x169,
    ),
    "sections_count" / Int16ul,
    "created" / Timestamp(Int32ul, 1., 1970),
    "symbol_pointer" / Int32ul, #deprecated
    "symbol_count" / Int32ul, #deprecated
    "optionalheader_size" / Int16ul,
    "characteristics" / FlagsEnum(Int16ul,
        RELOCS_STRIPPED = 0x0001,
        EXECUTABLE_IMAGE = 0x0002,
        LINE_NUMS_STRIPPED = 0x0004, #deprecated
        LOCAL_SYMS_STRIPPED = 0x0008, #deprecated
        AGGRESSIVE_WS_TRIM = 0x0010, #deprecated
        LARGE_ADDRESS_AWARE = 0x0020,
        RESERVED = 0x0040, #reserved
        BYTES_REVERSED_LO = 0x0080, #deprecated
        MACHINE_32BIT = 0x0100,
        DEBUG_STRIPPED = 0x0200,
        REMOVABLE_RUN_FROM_SWAP = 0x0400,
        SYSTEM = 0x1000,
        DLL = 0x2000,
        UNIPROCESSOR_ONLY = 0x4000,
        BIG_ENDIAN_MACHINE = 0x8000, #deprecated
    ),
)

plusfield = IfThenElse(this.signature == "PE32plus", Int64ul, Int32ul)

entriesnames = {
    0 : 'export_table',
    1 : 'import_table',
    2 : 'resource_table',
    3 : 'exception_table',
    4 : 'certificate_table',
    5 : 'base_relocation_table',
    6 : 'debug',
    7 : 'architecture',
    8 : 'global_ptr',
    9 : 'tls_table',
    10 : 'load_config_table',
    11 : 'bound_import',
    12 : 'import_address_table',
    13 : 'delay_import_descriptor',
    14 : 'clr_runtime_header',
    15 : 'reserved',
}

datadirectory = Struct(
    "name" / Computed(lambda this: entriesnames[this._._index]),
    "virtualaddress" / Int32ul,
    "size" / Int32ul,
)

optionalheader = Struct(
    "signature" / Enum(Int16ul, 
        PE32 = 0x10b,
        PE32plus = 0x20b,
        ROMIMAGE = 0x107,
    ),
    "linker_version" / Int8ul[2],
    "size_code" / Int32ul,
    "size_initialized_data" / Int32ul,
    "size_uninitialized_data" / Int32ul,
    "entrypoint" / Int32ul,
    "base_code" / Int32ul,
    "base_data" / If(this.signature == "PE32", Int32ul),
    "image_base" / plusfield,
    "section_alignment" / Int32ul,
    "file_alignment" / Int32ul,
    "os_version" / Int16ul[2],
    "image_version" / Int16ul[2],
    "subsystem_version" / Int16ul[2],
    "win32versionvalue" / Int32ul, #deprecated
    "image_size" / Int32ul,
    "headers_size" / Int32ul,
    "checksum" / Int32ul,
    "subsystem" / Enum(Int16ul,
        UNKNOWN = 0,
        NATIVE = 1,
        WINDOWS_GUI = 2,
        WINDOWS_CUI = 3,
        OS2_CUI = 5,
        POSIX_CUI = 7,
        WINDOWS_NATIVE = 8,
        WINDOWS_CE_GUI = 9,
        EFI_APPLICATION = 10,
        EFI_BOOT_SERVICE_DRIVER = 11,
        EFI_RUNTIME_DRIVER = 12,
        EFI_ROM = 13,
        XBOX = 14,
        WINDOWS_BOOT_APPLICATION = 16,
    ),
    "dll_characteristics" / FlagsEnum(Int16ul,
        HIGH_ENTROPY_VA = 0x0020,
        DYNAMIC_BASE = 0x0040,
        FORCE_INTEGRITY = 0x0080,
        NX_COMPAT = 0x0100,
        NO_ISOLATION = 0x0200,
        NO_SEH = 0x0400,
        NO_BIND = 0x0800,
        APPCONTAINER = 0x1000,
        WDM_DRIVER = 0x2000,
        GUARD_CF = 0x4000,
        TERMINAL_SERVER_AWARE = 0x8000,
    ),
    "stack_reserve" / plusfield,
    "stack_commit" / plusfield,
    "heap_reserve" / plusfield,
    "heap_commit" / plusfield,
    "loader_flags" / Int32ul, #reserved
    "datadirectories_count" / Int32ul,
    "datadirectories" / Array(this.datadirectories_count, 
        datadirectory),
)

section = Struct(
    "name" / PaddedString(8, "utf8"),
    "virtual_size" / Int32ul,
    "virtual_address" / Int32ul,
    "rawdata_size" / Int32ul,
    "rawdata_pointer" / Int32ul,
    "relocations_pointer" / Int32ul,
    "linenumbers_pointer" / Int32ul,
    "relocations_count" / Int16ul,
    "linenumbers_count" / Int16ul,
    "characteristics" / FlagsEnum(Int32ul,
        TYPE_REG = 0x00000000,
        TYPE_DSECT = 0x00000001,
        TYPE_NOLOAD = 0x00000002,
        TYPE_GROUP = 0x00000004,
        TYPE_NO_PAD = 0x00000008,
        TYPE_COPY = 0x00000010,
        CNT_CODE = 0x00000020,
        CNT_INITIALIZED_DATA = 0x00000040,
        CNT_UNINITIALIZED_DATA = 0x00000080,
        LNK_OTHER = 0x00000100,
        LNK_INFO = 0x00000200,
        TYPE_OVER = 0x00000400,
        LNK_REMOVE = 0x00000800,
        LNK_COMDAT = 0x00001000,
        MEM_FARDATA = 0x00008000,
        MEM_PURGEABLE = 0x00020000,
        MEM_16BIT = 0x00020000,
        MEM_LOCKED = 0x00040000,
        MEM_PRELOAD = 0x00080000,
        ALIGN_1BYTES = 0x00100000,
        ALIGN_2BYTES = 0x00200000,
        ALIGN_4BYTES = 0x00300000,
        ALIGN_8BYTES = 0x00400000,
        ALIGN_16BYTES = 0x00500000,
        ALIGN_32BYTES = 0x00600000,
        ALIGN_64BYTES = 0x00700000,
        ALIGN_128BYTES = 0x00800000,
        ALIGN_256BYTES = 0x00900000,
        ALIGN_512BYTES = 0x00A00000,
        ALIGN_1024BYTES = 0x00B00000,
        ALIGN_2048BYTES = 0x00C00000,
        ALIGN_4096BYTES = 0x00D00000,
        ALIGN_8192BYTES = 0x00E00000,
        LNK_NRELOC_OVFL = 0x01000000,
        MEM_DISCARDABLE = 0x02000000,
        MEM_NOT_CACHED = 0x04000000,
        MEM_NOT_PAGED = 0x08000000,
        MEM_SHARED = 0x10000000,
        MEM_EXECUTE = 0x20000000,
        MEM_READ = 0x40000000,
        MEM_WRITE = 0x80000000,
    ),
    "rawdata" / Pointer(this.rawdata_pointer, 
        Bytes(lambda this: this.rawdata_size if this.rawdata_pointer else 0)),
    "relocations" / Pointer(this.relocations_pointer,
        Array(this.relocations_count, Struct(
            "virtualaddress" / Int32ul,
            "symboltable_index" / Int32ul,
            "type" / Int16ul * "complicated platform-dependant Enum",
        ))
    ),
    "linenumbers" / Pointer(this.linenumbers_pointer,
        Array(this.linenumbers_count, Struct(
            "_type" / Int32ul,
            "_linenumber" / Int16ul,
            "is_symboltableindex" / Computed(this._linenumber == 0),
            "is_linenumber" / Computed(this._linenumber > 0),
            "symboltableindex" / If(this.is_symboltableindex, Computed(this._type)),
            "linenumber" / If(this.is_linenumber, Computed(this._linenumber)),
            "virtualaddress" / If(this.is_linenumber, Computed(this._type)),
        ))
    ),
)

pe32file = docs * Struct(
    "msdosheader" / msdosheader,
    Seek(this.msdosheader.lfanew),
    "coffheader" / coffheader,
    "optionalheader" / If(this.coffheader.optionalheader_size > 0, optionalheader),
    "sections_count" / Computed(this.coffheader.sections_count),
    "sections" / Array(this.sections_count, section),
)
