"""
common constructs for typical programming languages (numbers, strings, ...)
"""
from construct.core import (Construct, ConstructError, FieldError, SizeofError)
from construct.adapters import (Adapter, StringAdapter, IndexingAdapter,
    ConstAdapter, OneOf, NoneOf)
from construct.macros import (Field, OptionalGreedyRange, GreedyRange,
    Sequence, Optional)

from construct.lib.py3compat import bchr


#===============================================================================
# exceptions
#===============================================================================
class QuotedStringError(ConstructError):
    __slots__ = []


#===============================================================================
# constructs
#===============================================================================
class QuotedString(Construct):
    r"""
    A quoted string (begins with an opening-quote, terminated by a
    closing-quote, which may be escaped by an escape character)

    Parameters:
    * name - the name of the field
    * start_quote - the opening quote character. default is '"'
    * end_quote - the closing quote character. default is '"'
    * esc_char - the escape character, or None to disable escaping. defualt
      is "\" (backslash)
    * encoding - the character encoding (e.g., "utf8"), or None to return
      raw bytes. defualt is None.
    * allow_eof - whether to allow EOF before the closing quote is matched.
      if False, an exception will be raised when EOF is reached by the closing
      quote is missing. default is False.

    Example:
    QuotedString("foo", start_quote = "{", end_quote = "}", esc_char = None)
    """
    __slots__ = [
        "start_quote", "end_quote", "char", "esc_char", "encoding",
        "allow_eof"
    ]
    def __init__(self, name, start_quote = b'"', end_quote = None,
                 esc_char = b'\\', encoding = None, allow_eof = False):
        Construct.__init__(self, name)
        if end_quote is None:
            end_quote = start_quote
        self.start_quote = Literal(start_quote)
        self.char = Char("char")
        self.end_quote = end_quote
        self.esc_char = esc_char
        self.encoding = encoding
        self.allow_eof = allow_eof

    def _parse(self, stream, context):
        self.start_quote._parse(stream, context)
        text = []
        escaped = False
        try:
            while True:
                ch = self.char._parse(stream, context)
                if ch == self.esc_char:
                    if escaped:
                        text.append(ch)
                        escaped = False
                    else:
                        escaped = True
                elif ch == self.end_quote and not escaped:
                    break
                else:
                    text.append(ch)
                    escaped = False
        except FieldError:
            if not self.allow_eof:
                raise
        text = b"".join(text)
        if self.encoding is not None:
            text = text.decode(self.encoding)
        return text

    def _build(self, obj, stream, context):
        self.start_quote._build(None, stream, context)
        if self.encoding:
            obj = obj.encode(self.encoding)
        for ch in obj:
            ch = bchr(ch)
            if ch == self.esc_char:
                self.char._build(self.esc_char, stream, context)
            elif ch == self.end_quote:
                if self.esc_char is None:
                    raise QuotedStringError("found ending quote in data, "
                        "but no escape char defined", ch)
                else:
                    self.char._build(self.esc_char, stream, context)
            self.char._build(ch, stream, context)
        self.char._build(self.end_quote, stream, context)

    def _sizeof(self, context):
        raise SizeofError("can't calculate size")


#===============================================================================
# macros
#===============================================================================
class WhitespaceAdapter(Adapter):
    """
    Adapter for whitespace sequences; do not use directly.
    See Whitespace.

    Parameters:
    * subcon - the subcon to adapt
    * build_char - the character used for encoding (building)
    """
    __slots__ = ["build_char"]
    def __init__(self, subcon, build_char):
        Adapter.__init__(self, subcon)
        self.build_char = build_char
    def _encode(self, obj, context):
        return self.build_char
    def _decode(self, obj, context):
        return None

def Whitespace(charset = b" \t", optional = True):
    """whitespace (space that is ignored between tokens). when building, the
    first character of the charset is used.
    * charset - the set of characters that are considered whitespace. default
      is space and tab.
    * optional - whether or not whitespace is optional. default is True.
    """
    con = CharOf(None, charset)
    if optional:
        con = OptionalGreedyRange(con)
    else:
        con = GreedyRange(con)
    return WhitespaceAdapter(con, build_char = charset[0:1])

def Literal(text):
    """matches a literal string in the text
    * text - the text (string) to match
    """
    return ConstAdapter(Field(None, len(text)), text)

def Char(name):
    """a one-byte character"""
    return Field(name, 1)

def CharOf(name, charset):
    """matches only characters of a given charset
    * name - the name of the field
    * charset - the set of valid characters
    """
    return OneOf(Char(name), charset)

def CharNoneOf(name, charset):
    """matches only characters that do not belong to a given charset
    * name - the name of the field
    * charset - the set of invalid characters
    """
    return NoneOf(Char(name), charset)

def Alpha(name):
    """a letter character (A-Z, a-z)"""
    return CharOf(name, set(b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'))

def Digit(name):
    """a digit character (0-9)"""
    return CharOf(name, set(b'0123456789'))

def AlphaDigit(name):
    """an alphanumeric character (A-Z, a-z, 0-9)"""
    return CharOf(name, set(b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"))

def BinDigit(name):
    """a binary digit (0-1)"""
    return CharOf(name, set(b'01'))

def HexDigit(name):
    """a hexadecimal digit (0-9, A-F, a-f)"""
    return CharOf(name, set(b'0123456789abcdefABCDEF'))

def Word(name):
    """a sequence of letters"""
    return StringAdapter(GreedyRange(Alpha(name)))

class TextualIntAdapter(Adapter):
    """
    Adapter for textual integers

    Parameters:
    * subcon - the subcon to adapt
    * radix - the base of the integer (decimal, hexadecimal, binary, ...)
    * digits - the sequence of digits of that radix
    """
    __slots__ = ["radix", "digits"]
    def __init__(self, subcon, radix = 10, digits = b"0123456789abcdef"):
        Adapter.__init__(self, subcon)
        if radix > len(digits):
            raise ValueError("not enough digits for radix %d" % (radix,))
        self.radix = radix
        self.digits = digits
    def _encode(self, obj, context):
        chars = []
        if obj < 0:
            chars.append(b"-")
            n = -obj
        else:
            n = obj
        r = self.radix
        digs = self.digits
        while n > 0:
            n, d = divmod(n, r)
            chars.append(digs[d])
        # obj2 = "".join(reversed(chars))
        # filler = digs[0] * (self._sizeof(context) - len(obj2))
        # return filler + obj2
        return b"".join(reversed(chars))
    def _decode(self, obj, context):
        return int(b"".join(obj), self.radix)

def DecNumber(name):
    """decimal number"""
    return TextualIntAdapter(GreedyRange(Digit(name)))

def BinNumber(name):
    """binary number"""
    return TextualIntAdapter(GreedyRange(BinDigit(name)), 2)

def HexNumber(name):
    """hexadecimal number"""
    return TextualIntAdapter(GreedyRange(HexDigit(name)), 16)

class TextualFloatAdapter(Adapter):
    def _decode(self, obj, context):
        whole, frac, exp = obj
        mantissa = b"".join(whole) + b"." + b"".join(frac)
        if exp:
            sign, value = exp
            if not sign:
                sign = b""
            return float(mantissa + b"e" + sign + b"".join(value))
        else:
            return float(mantissa)
    def _encode(self, obj, context):
        obj = str(obj)
        exp = None
        if b"e" in obj:
            obj, exp = obj.split(b"e")
            sign = exp[0:1]
            value = exp[1:]
            exp = [sign, value]
        whole, frac = obj.split(b".")
        return [whole, frac, exp]

def FloatNumber(name):
    return TextualFloatAdapter(
        Sequence(name,
            GreedyRange(Digit("whole")),
            Literal(b"."),
            GreedyRange(Digit("frac")),
            Optional(
                Sequence("exp",
                    Literal(b"e"),
                    Optional(CharOf("sign", b"+-")),
                    GreedyRange(Digit("value")),
                )
            )
        )
    )

def StringUpto(name, terminators, consume_terminator = False, allow_eof = True):
    """a string that stretches up to a terminator, or EOF. this is a more
    flexible version of CString.
    * name - the name of the field
    * terminator - the set of terminator characters
    * consume_terminator - whether to consume the terminator character. the
      default is False.
    * allow_eof - whether to allow EOF to terminate the string. the default
      is True. this option is applicable only if consume_terminator is set.
    """
    con = StringAdapter(OptionalGreedyRange(CharNoneOf(name, terminators)))
    if not consume_terminator:
        return con
    if allow_eof:
        term = Optional(CharOf(None, terminators))
    else:
        term = CharOf(None, terminators)
    return IndexingAdapter(Sequence("foo", con, term), index = 0)

def Line(name, consume_terminator = True, allow_eof = True):
    r"""a textual line (up to "\n")
    * name - the name of the field
    * consume_terminator - whether to consume the newline character. the
      default is True.
    * allow_eof - whether to allow EOF to terminate the string. the default
      is True. this option is applicable only if consume_terminator is set.
    """
    return StringUpto(name, b"\n",
        consume_terminator = consume_terminator,
        allow_eof = allow_eof
    )

class IdentifierAdapter(Adapter):
    """
    Adapter for programmatic identifiers

    Parameters:
    * subcon - the subcon to adapt
    """
    def _encode(self, obj, context):
        return obj[0], obj[1:]
    def _decode(self, obj, context):
        return obj[0] + b"".join(obj[1])


_default_identifier_headset = set()
for c in b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_":
    _default_identifier_headset.add(bchr(c))

_default_identifier_tailset = set()
for c in b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_":
    _default_identifier_tailset.add(bchr(c))


def Identifier(name,
               headset=_default_identifier_headset,
               tailset=_default_identifier_tailset
    ):
    """a programmatic identifier (symbol). must start with a char of headset,
    followed by a sequence of tailset characters
    * name - the name of the field
    * headset - charset for the first character. default is A-Z, a-z, and _
    * tailset - charset for the tail. default is A-Z, a-z, 0-9 and _
    """
    return IdentifierAdapter(
        Sequence(name,
            CharOf("head", headset),
            OptionalGreedyRange(CharOf("tail", tailset)),
        )
    )
