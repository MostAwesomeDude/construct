from construct.lib.py3compat import *


def integer2bits(number, width):
    r"""
    Converts an integer into its binary representation in a b-string. Width is the amount of bits to generate. If width is larger than the actual amount of bits required to represent number in binary, sign-extension is used. If it's smaller, the representation is trimmed to width bits. Each bit is represented as either b'\\x00' or b'\\x01'. The most significant is first, big-endian. This is reverse to `bits2integer`.

    Examples:

        >>> integer2bits(19, 8)
        b'\x00\x00\x00\x01\x00\x00\x01\x01'
    """
    if width < 1:
        raise ValueError("width must be positive")
    number = int(number)
    if number < 0:
        number += 1 << width
    bits = [b"\x00"] * width
    i = width - 1
    while number and i >= 0:
        bits[i] = int2byte(number & 1)
        number >>= 1
        i -= 1
    return b"".join(bits)


def integer2bytes(number, width):
    r"""
    Converts a b-string into an integer. This is reverse to `bytes2integer`.

    Examples:

        >>> integer2bytes(19,4)
        '\x00\x00\x00\x13'
    """
    if width < 1:
        raise ValueError("width must be positive")
    number = int(number)
    if number < 0:
        number += 1 << (width * 8)
    acc = [b"\x00"] * width
    i = width - 1
    while number > 0:
        acc[i] = int2byte(number & 255)
        number >>= 8
        i -= 1
    return b"".join(acc)


ONEBIT2INTEGER_CACHE = {b"0":0, b"\x00":0, b"1":1, b"\x01":1}
def onebit2integer(b):
    try:
        return ONEBIT2INTEGER_CACHE[b]
    except KeyError:
        raise ValueError(r"bit was not recognized as one of: 0 1 \x00 \x01")


def bits2integer(data, signed=False):
    r"""
    Converts a b-string into an integer. Both b'0' and b'\\x00' are considered zero, and both b'1' and b'\\x01' are considered one. Set sign to interpret the number as a 2-s complement signed integer. This is reverse to `integer2bits`.

    Examples:

        >>> bits2integer(b"\x01\x00\x00\x01\x01")
        19
        >>> bits2integer(b"10011")
        19
    """
    number = 0
    for b in iteratebytes(data):
        number = (number << 1) | onebit2integer(b)

    if signed and onebit2integer(data[0:1]):
        bias = 1 << (len(data) -1)
        return number - bias*2
    else:
        return number


def bytes2integer(data, signed=False):
    r"""
    Converts a b-string into an integer. This is reverse to `integer2bytes`.

    Examples:

        >>> bytes2integer(b'\x00\x00\x00\x13')
        19
    """
    number = 0
    for b in iterateints(data):
        number = (number << 8) | b

    if signed and byte2int(bytes2bits(data[0:1])[0:1]):
        bias = 1 << (len(data)*8 -1)
        return number - bias*2
    else:
        return number


BYTES2BITS_CACHE = {i:integer2bits(i,8) for i in range(256)}
def bytes2bits(data):
    r""" 
    Converts between bit and byte representations in b-strings.

    Example:

        >>> bytes2bits(b'ab')
        b"\x00\x01\x01\x00\x00\x00\x00\x01\x00\x01\x01\x00\x00\x00\x01\x00"
    """
    return b"".join(BYTES2BITS_CACHE[b] for b in iterateints(data))


BITS2BYTES_CACHE = {bytes2bits(int2byte(i)):int2byte(i) for i in range(256)}
def bits2bytes(data):
    r""" 
    Converts between bit and byte representations in b-strings.

    Example:

        >>> bits2bytes(b"\x00\x01\x01\x00\x00\x00\x00\x01\x00\x01\x01\x00\x00\x00\x01\x00")
        b'ab'
    """
    if len(data) & 7:
        raise ValueError("data length must be a multiple of 8")
    return b"".join(BITS2BYTES_CACHE[data[i:i+8]] for i in range(0,len(data),8))


def swapbytes(data):
    r"""
    Performs an endianness swap on a bit-string bytes. Its length must be multiple of 8.

    Example:

        >>> swapbytes(b'0000000011111111')
        b'1111111100000000'
    """
    if len(data) & 7:
        raise ValueError("data length must be multiple of 8")
    return b"".join(data[i:i+8] for i in reversed(range(0,len(data),8)))


SWAPBITS_CACHE = {i:bits2bytes(bytes2bits(int2byte(i))[::-1]) for i in range(256)}
def swapbits(data):
    r"""
    Performs a bit-reversal on bytes.

    Example:

        >>> swapbits(b'\xf0')
        b'\x0f'
    """
    return b"".join(SWAPBITS_CACHE[b] for b in iterateints(data))
