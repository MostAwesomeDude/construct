"""
Contributed by Dany Zatuchna (danzat at gmail)

Implementation of the following grammar for the GIF89a file format

<GIF Data Stream> ::=     Header <Logical Screen> <Data>* Trailer
<Logical Screen> ::=      Logical Screen Descriptor [Global Color Table]
<Data> ::=                <Graphic Block>  | <Special-Purpose Block>
<Graphic Block> ::=       [Graphic Control Extension] <Graphic-Rendering Block>
<Graphic-Rendering Block> ::=  <Table-Based Image>  | Plain Text Extension
<Table-Based Image> ::=   Image Descriptor [Local Color Table] Image Data
<Special-Purpose Block> ::=    Application Extension  | Comment Extension
"""

from construct import *


data_sub_block = PascalString(Int8ul, StringsAsBytes)

gif_logical_screen = Struct(
    "width" / Int16ul,
    "height" / Int16ul,
    "flags" / BitStruct(
        "global_color_table" / Bit,
        "color_resolution" / BitsInteger(3),
        "sort_flag" / Bit,
        "global_color_table_bpp" / BitsInteger(3),
    ),
    "bgcolor_index" / Int8ul,
    "pixel_aspect_ratio" / Int8ul,
    "palette" / If(this.flags.global_color_table,
        Array(lambda ctx: 2**(ctx.flags.global_color_table_bpp + 1),
            Struct(
                "R" / Int8ul,
                "G" / Int8ul,
                "B" / Int8ul,
            ))),
)

application_extension = Struct(
    "block_size" / Const(11, Int8ul),
    "application_identifier" / String(8, StringsAsBytes),
    "application_auth_code" / String(3, StringsAsBytes),
    "data_sub_block" / data_sub_block,
    "block_terminator" / Int8ul,
)

comment_extension = Struct(
    "data_sub_block" / data_sub_block,
    "block_terminator" / Int8ul,
)

graphic_control_extension = Struct(
    "block_size" / Const(4, Int8ul),
    "flags" / BitStruct(
        "reserved" / BitsInteger(3),
        "disposal_method" / BitsInteger(3),
        "user_input_flag" / Bit,
        "transparent_color_flag" / Bit,
    ),
    "delay" / Int16ul,
    "transparent_color_index" / Int8ul,
    "block_terminator" / Int8ul,
)

plain_text_extension = Struct(
    "block_size" / Const(12, Int8ul),
    "text_left" / Int16ul,
    "text_top" / Int16ul,
    "text_width" / Int16ul,
    "text_height" / Int16ul,
    "cell_width" / Int8ul,
    "cell_height" / Int8ul,
    "foreground_index" / Int8ul,
    "background_index" / Int8ul,
    "data_sub_block" / data_sub_block,
    "block_terminator" / Int8ul,
)

extension = Struct(
    "label" / Int8ul,
    "ext" / Switch(this.label, {
        0xFF: application_extension,
        0xFE: comment_extension,
        0xF9: graphic_control_extension,
        0x01: plain_text_extension
    }),
)

image_descriptor = Struct(
    "left" / Int16ul,
    "top" / Int16ul,
    "width" / Int16ul,
    "height" / Int16ul,
    "flags" / BitStruct(
        "local_color_table" / Bit,
        "interlace" / Bit,
        "sort" / Bit,
        "reserved" / BitsInteger(2),
        "local_color_table_bpp" / BitsInteger(3),
    ),
    "palette" / If(this.flags.local_color_table,
        Array(lambda ctx: 2**(ctx.flags.local_color_table_bpp + 1),
            Struct(
                "R" / Int8ul,
                "G" / Int8ul,
                "B" / Int8ul,
            ))),
    "lzw_minimum_code_size" / Int8ul,
    "data_sub_block" / RepeatUntil(lambda obj,lst,ctx: obj.size == 0, data_sub_block),
)

gif_data = Struct(
    "introducer" / Int8ul,
    "data" / Switch(this.introducer, {
        0x21: extension,
        0x2C: image_descriptor
    }),
)

gif_file = Struct(
    "signature" / Const(b"GIF"),
    "version" / Const(b"89a"),
    "logical_screen" / gif_logical_screen,
    "data" / GreedyRange(gif_data),
    # Const(Int8ul("trailer"), 0x3B)
)
