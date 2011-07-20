============
Text parsing
============

What has text to do with Construct?

As you already know at this stage of the tutorial, Construct works with binary
data. That is, all sorts of data structures, file formats, and protocols, that
have a well defined binary structure. Construct can be used to parse such data
into objects (which are easier to handle programmatically), or build objects
into binary data.

But even with the narrow scope of protocols or file formats, there are many
textual protocols such as HTTP, or textual file formats such as RTF. As
Construct aims to be a one-parser-to-rule-them-all, I decided to add some
textual construction tools to Construct.

Nevertheless, I also wrote it so as to show people that Construct is really a
parser (and more). I got lots of mails saying Construct was not really a
parser, in the computer-science sense of the word, since it doesn't define a
grammar. So now it does, mwhahaha.

But this comes with a reservation: Construct's main target is still binary
data. It is possible to define fully functional context-free grammars with
Construct -- and I did write a grammar for a C-like language -- but if grammar
is what you seek, use a dedicated library. There are lots of possible
optimizations, such as using a tokenizer first or optimized LL/LR parsers,
handling text encoding, etc., which Construct does not (and will not) perform.
That's all for a different library.

"Parsing HTTP ought to be enough for everyone".

In order to use the text module, you'll have to explicitly import it.

>>> from construct.text import *
>>>


Matching characters
===================

Char
----

A single character (1-byte). Note that all characters are assumed to be 8-bit
ASCII. More complex encoding are left for a higher level.

CharOf
------

Matches a character that is one of a set of valid characters.

>>> digit = CharOf("digit", "0123456789")
>>> digit.parse("6")
'6'
>>> digit.parse("v")
Traceback (most recent call last):
  .
  .
construct.core.ValidatorError: ('invalid object', 'v')


CharNoneOf
----------

Matches a character that is not part of the set of invalid characters.

>>> nonquote = CharNoneOf("quote", '"')
>>> nonquote.parse("x")
'x'
>>> nonquote.parse('"')
Traceback (most recent call last):
  .
  .
construct.core.ValidatorError: ('invalid object', '"')


Literal
-------

Matches a given literal pattern (i.e., a keyword).

>>> while_statement = Struct("while_statement",
...     Literal("while"),
...     GreedyRange(CharOf(None, " \t")),
...     Word("name"),
...     Literal(":")
... )
>>> while_statement.parse("while    True:")
Container(name = 'True')
>>> while_statement.parse("if    True:")
Traceback (most recent call last):
  .
  .
construct.extensions.ConstError: expected 'while', found 'if   '
>>>


Select
------

Selects the first matching subconstruct, and uses it for parsing or building.
The order of the subconstructs is meaningful. Also note that Select can
operate with seekable streams only (files or in-memory). Raises SelectError if
no matching subconstruct is found.

>>> c = Select("foo",
...     Sequence("hex", Literal("0x"), HexNumber("value")),
...     FloatNumber("flt"),
...     DecNumber("dec"),
... )
>>> c.parse("123")
123
>>> c.parse("0x123")
[291]
>>> c.parse("123.456")
123.456
>>>
>>> c.build(123)
'123'
>>> c.build([123])
'0x7b'
>>> c.build(123.456)
'123.456'


Constructs for Languages
========================

These constructs are provided because they are likely to be very useful with
most common computer languages (C, java, python, ruby, ...)

QuotedString
------------

A quoted string. You can define the starting and ending quote chars, and
escape char.

>>> q = QuotedString("foo", start_char = "{", end_char = "}", esc_char = "~")
>>> q.parse("{hello world")
Traceback (most recent call last):
  .
  .
construct.core.EndOfStreamError
>>> q.parse("{hello world}")
'hello world'
>>> q.parse("{this ~} is an escaped ending quote }")
'this } is an escaped ending quote '
>>>


Whitespace
----------

Whitespace is a sequence of whitespace chars (by default space and tab) that
has no programmatic meaning. It is only used to separate tokens or to make the
code readable. You can specify ``allow_empty = False``, which means that the
whitespace is mandatory. Otherwise, whitespace is optional.

>>> Whitespace().parse("  \t")
>>>


DecNumber
---------

Decimal integral number ((0-9)+). Returns a python integer.

>>> DecNumber("foo").parse("123+456")
123


HexNumber
---------

Hexadecimal number ((0-9, A-F, a-f)+). Returns a python integer.

>>> HexNumber("foo").parse("c0ffee")
12648430


FloatNumber
-----------

Floating-pointer number ((0-9)+\.(0-9)+). Returns a python float.

>>> FloatNumber("foo").parse("123.456")
123.456


Word
----

A sequence of alpha characters ((A-Z, a-z)+).

>>> Word("foo").parse("hello world")
'hello'


StringUpto
----------

A string terminated by some character (similar to CString, but the terminator
char is not consumed).

>>> StringUpto("foo", "x").parse("hellox")
'hello'


Line
----

A text line (terminated by ``\r`` or ``\n``)

>>> Line("foo").parse("hello world\n")
'hello world'


Identifier
----------

A sequence of alpha-numeric or underscore characters commonly used as
identifiers in programming languages. The first char must be a alpha or
underscore (not number).

>>> Identifier("foo").parse("fat_boy3 beefed")
'fat_boy3'
