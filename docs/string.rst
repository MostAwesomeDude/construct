String
======

A fixed-length string field. It takes the following parameters:

    * name - the name
    * length - the length (in bytes) of the string
    * encoding - the encoding (i.e., 'utf8') or None for raw bytes (ASCII)
    * padchar - if the string is padded, specify the pad char (usually
'\x00'). None (the default) means no padding is used (in which case trimdir
and paddir have no effect).
    * paddir - 'right', 'left', or 'both', the padding direction. Applicable
only if padchar is not None.
    * trim - 'right', 'left'. Used only for building, specifies the direction
from which to trim too long strings. For example, if we try to write "ABCD" in
a 3-byte string, and trimdir == "right", you'll get "ABC". If trimdir ==
"left", you'll get "BCD". Applicable only when padchar is not None.

>>> String("foo", 5).parse("hello")
'hello'
>>>
>>> String("foo", 12, encoding = "utf8").parse("hello joh\xd4\x83n")
u'hello joh\u0503n'
>>>
>>> foo = String("foo", 10, padchar = "X", paddir = "right")
>>> foo.parse("helloXXXXX")
'hello'
>>> foo.build("hello")
'helloXXXXX'


PascalString
------------

A variable-length string; the data is prefixed by a length field. It takes the
following parameters:

    * name - the name
    * lengthfield - a construct class that returns a number. The default is
UBInt8 (one byte)
    * encoding - the encoding (i.e., 'utf8') or None for raw bytes (ASCII)


>>> foo = PascalString("foo")
>>> foo.parse("\x05hello")
'hello'
>>> foo.build("hello world")
'\x0bhello world'
>>>
>>> foo = PascalString("foo", lengthfield = UBInt16)
>>>#Try this if u got an error from above line:
>>>foo = PascalString("foo", length_field = UBInt16("length"))
>>> foo.parse("\x00\x05hello")
'hello'
>>> foo.build("hello")
'\x00\x05hello'
>>>


CString
-------

A variable-length string terminated by a terminator character (usually
'\x00'). It takes the following parameters:

    * name - the name
    * charsize - the number of bytes per character
    * terminators - a sequence of one-character strings. When one of the
terminator characters is encountered in the string, the string is terminated.
The default terminator is '\x00'. When building, the first terminator
character (terminators[0]) is used.
    * encoding - the encoding of the string or None (the default)

>>> foo = CString("foo")
>>>
>>> foo.parse("hello\x00")
'hello'
>>> foo.build("hello")
'hello\x00'
>>>
>>> foo = CString("foo", terminators = "XYZ")
>>>
>>> foo.parse("helloX")  # <-- any one of "X", "Y", or "Z" would work
'hello'
>>> foo.parse("helloY")
'hello'
>>> foo.parse("helloZ")
'hello'
>>> foo.build("hello")   # <-- uses the first terminator char ("x")
'helloX'
>>>
