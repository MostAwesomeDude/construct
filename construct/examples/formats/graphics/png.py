"""
Portable Network Graphics (PNG) file format
Official spec: http://www.w3.org/TR/PNG

Original code contributed by Robin Munn (rmunn at pobox dot com)
(although the code has been extensively reorganized to meet Construct's
coding conventions)
"""
from construct import *


#===============================================================================
# utils
#===============================================================================
coord = Struct(
    "x" / Int32ub,
    "y" / Int32ub,
)

compression_method = "compression_method" / Enum(Byte, deflate = 0, default=Pass)


#===============================================================================
# 11.2.3: PLTE - Palette
#===============================================================================
plte_info = "plte_info" / Struct(
    "num_entries" / Computed(this._.length / 3),
    Array(this.num_entries,
        "palette_entries" / Struct(
            "red" / Byte,
            "green" / Byte,
            "blue" / Byte,
        ),
    ),
)

#===============================================================================
# 11.2.4: IDAT - Image data
#===============================================================================
idat_info = "idat_info" / Bytes(this.length)

#===============================================================================
# 11.3.2.1: tRNS - Transparency
#===============================================================================
trns_info = "trns_info" / Switch(this._.image_header.color_type, 
    {
        "greyscale": "data" / Struct(
            "grey_sample" / Int16ub,
        ),
        "truecolor": "data" / Struct(
            "red_sample" / Int16ub,
            "blue_sample" / Int16ub,
            "green_sample" / Int16ub,
        ),
        "indexed": "alpha" / Array(this.length, Byte),
    }
)

#===============================================================================
# 11.3.3.1: cHRM - Primary chromacities and white point
#===============================================================================
chrm_info = "chrm_info" / Struct(
    "white_point" / coord,
    "red" / coord,
    "green" / coord,
    "blue" / coord,
)

#===============================================================================
# 11.3.3.2: gAMA - Image gamma
#===============================================================================
gama_info = "gama_info" / Struct(
    "gamma" / Int32ub,
)

#===============================================================================
# 11.3.3.3: iCCP - Embedded ICC profile
#===============================================================================
iccp_info = "iccp_info" / Struct(
    "name" / CString(),
    compression_method,
    "compressed_profile" / Bytes(lambda ctx: ctx._.length - (len(ctx.name) + 2)),
)

#===============================================================================
# 11.3.3.4: sBIT - Significant bits
#===============================================================================
sbit_info = "sbit_info" / Switch(this._.image_header.color_type, 
    {
        "greyscale": Struct(
            "significant_grey_bits" / Byte,
        ),
        "truecolor": Struct("data",
            "significant_red_bits" / Byte,
            "significant_green_bits" / Byte,
            "significant_blue_bits" / Byte,
        ),
        "indexed": Struct("data",
            "significant_red_bits" / Byte,
            "significant_green_bits" / Byte,
            "significant_blue_bits" / Byte,
        ),
        "greywithalpha": Struct(
            "significant_grey_bits" / Byte,
            "significant_alpha_bits" / Byte,
        ),
        "truewithalpha": Struct(
            "significant_red_bits" / Byte,
            "significant_green_bits" / Byte,
            "significant_blue_bits" / Byte,
            "significant_alpha_bits" / Byte,
        ),
    }
)

#===============================================================================
# 11.3.3.5: sRGB - Standard RPG color space
#===============================================================================
srgb_info = "srgb_info" / Struct(
    "rendering_intent" / Enum(Byte,
        perceptual = 0,
        relative_colorimetric = 1,
        saturation = 2,
        absolute_colorimetric = 3,
        default=Pass
    ),
)

#===============================================================================
# 11.3.4.3: tEXt - Textual data
#===============================================================================
text_info = "text_info" / Struct(
    "keyword" / CString(),
    "text" / Bytes(lambda ctx: ctx._.length - len(ctx.keyword) + 1),
)

#===============================================================================
# 11.3.4.4: zTXt - Compressed textual data
#===============================================================================
ztxt_info = "ztxt_info" / Struct(
    "keyword" / CString(),
    compression_method,
    # As with iCCP, length is chunk length, minus length of
    # keyword, minus two: one byte for the null terminator,
    # and one byte for the compression method.
    "compressed_text" / Bytes(lambda ctx: ctx._.length - len(ctx.keyword) + 2),
)

#===============================================================================
# 11.3.4.5: iTXt - International textual data
#===============================================================================
itxt_info = "itxt_info" / Struct(
    "keyword" / CString(),
    "compression_flag" / Byte,
    compression_method,
    "language_tag" / CString(),
    "translated_keyword" / CString(),
    "text" / Bytes(lambda ctx: ctx._.length - len(ctx.keyword) + len(ctx.language_tag) + len(ctx.translated_keyword) + 5),
)

#===============================================================================
# 11.3.5.1: bKGD - Background color
#===============================================================================
bkgd_info = "bkgd_info" / Switch(this._.image_header.color_type, 
    {
        "greyscale": Struct(
            "grey" / Int16ub,
        ),
        "greywithalpha": Struct(
            "grey" / Int16ub,
        ),
        "truecolor": Struct(
            "red" / Int16ub,
            "green" / Int16ub,
            "blue" / Int16ub,
        ),
        "truewithalpha": Struct(
            "red" / Int16ub,
            "green" / Int16ub,
            "blue" / Int16ub,
        ),
        "indexed": Struct(
            "index" / Int16ub,
        ),
    }
)

#===============================================================================
# 11.3.5.2: hIST - Image histogram
#===============================================================================
hist_info = "frequency" / Array(this._.length / 2, Int16ub,
)

#===============================================================================
# 11.3.5.3: pHYs - Physical pixel dimensions
#===============================================================================
phys_info = "phys_info" / Struct(
    "pixels_per_unit_x" / Int32ub,
    "pixels_per_unit_y" / Int32ub,
    "unit" / Enum(Byte, unknown = 0, meter = 1, default = Pass),
)

#===============================================================================
# 11.3.5.4: sPLT - Suggested palette
#===============================================================================
def splt_info_data_length(ctx):
    if ctx.sample_depth == 8:
        entry_size = 6
    else:
        entry_size = 10
    return (ctx._.length - len(ctx.name) - 2) / entry_size

splt_info = "data" / Struct(
    "name" / CString(),
    "sample_depth" / Byte,
    "table" / Array(splt_info_data_length,
        IfThenElse(this.sample_depth == 8,
            # Sample depth 8
            Struct(
                "red" / Byte,
                "green" / Byte,
                "blue" / Byte,
                "alpha" / Byte,
                "frequency" / Int16ub,
            ),
            # Sample depth 16
            Struct(
                "red" / Int16ub,
                "green" / Int16ub,
                "blue" / Int16ub,
                "alpha" / Int16ub,
                "frequency" / Int16ub,
            ),
        ),
    ),
)

#===============================================================================
# 11.3.6.1: tIME - Image last-modification time
#===============================================================================
time_info = "data" / Struct(
    "year" / Int16ub,
    "month" / Byte,
    "day" / Byte,
    "hour" / Byte,
    "minute" / Byte,
    "second" / Byte,
)

#===============================================================================
# chunks
#===============================================================================
default_chunk_info = HexDump(Bytes(this.length))

chunk = "chunk" / Struct(
    "length" / Int32ub,
    "type" / String(4),
    "data" / Switch(this.type,
        {
            "PLTE" : plte_info,
            "IEND" : Pass,
            "IDAT" : idat_info,
            "tRNS" : trns_info,
            "cHRM" : chrm_info,
            "gAMA" : gama_info,
            "iCCP" : iccp_info,
            "sBIT" : sbit_info,
            "sRGB" : srgb_info,
            "tEXt" : text_info,
            "zTXt" : ztxt_info,
            "iTXt" : itxt_info,
            "bKGD" : bkgd_info,
            "hIST" : hist_info,
            "pHYs" : phys_info,
            "sPLT" : splt_info,
            "tIME" : time_info,
        },
        default = default_chunk_info,
    ),
    "crc" / Int32ub,
)

image_header_chunk = "image_header" / Struct(
    "length" / Int32ub,
    "signature" / Const(b"IHDR"),
    "width" / Int32ub,
    "height" / Int32ub,
    "bit_depth" / Byte,
    "color_type" / Enum(Byte,
        greyscale = 0,
        truecolor = 2,
        indexed = 3,
        greywithalpha = 4,
        truewithalpha = 6,
        default = Pass,
    ),
    compression_method,
    # "adaptive filtering with five basic filter types"
    "filter_method" / Enum(Byte, adaptive5 = 0, default = Pass),
    "interlace_method" / Enum(Byte, none = 0, adam7 = 1, default = Pass),
    "crc" / Int32ub,
)


#===============================================================================
# the complete PNG file
#===============================================================================
png_file = "png" / Struct(
    "signature" / Const(b"\x89PNG\r\n\x1a\n"),
    image_header_chunk,
    "chunks" / GreedyRange(chunk),
)


