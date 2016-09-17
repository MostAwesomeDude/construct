from construct.lib.py3compat import *


def integer2bits(number, width):
    r"""
    Convert an integer into its binary representation in a bytes object. Width is the amount of bits to generate. If width is larger than the actual amount of bits required to represent number in binary, sign-extension is used. If it's smaller, the representation is trimmed to width bits. Each "bit" is either b'\x00' or b'\x01'. The most significant is first.

    Examples:

        >>> integer2bits(19, 8)
        b'\x00\x00\x00\x01\x00\x00\x01\x01'
    """
    if width < 1:
        raise ValueError("width must be positive")
    number = int(number)
    if number < 0:
        number += 1 << width
    i = width - 1
    bits = [b"\x00"] * width
    while number and i >= 0:
        bits[i] = b"\x01" if number & 1 else b"\x00"
        # bits[i] = b"\x00\x01"[number & 1]
        number >>= 1
        i -= 1
    return b"".join(bits)


def bits2integer(bits, signed=False):
    r"""
    Logical opposite of integer2bits. Both b'0' and b'\x00' are considered zero, and both b'1' and b'\x01' are considered one. Set sign to interpret the number as a 2-s complement signed integer.

    HEAVILY OPTIMIZED FOR PERFORMANCE

    Examples:

        >>> bits2integer(b"\x01\x00\x00\x01\x01")
        19
        >>> bits2integer(b"10011")
        19
    """
    bits = "".join("01"[b & 1] for b in iterateints(bits))
    if signed and bits[0] == "1":
        # return -int(bits[1:], 2)
        bits = bits[1:]
        bias = 1 << len(bits)
        return int(bits, 2) - bias
    else:
        return int(bits, 2)


def bytes2bits(data):
    r""" 
    Create a binary representation of a b-string.

    Example:

        >>> bytes2bits(b'ab')
        b"\x00\x01\x01\x00\x00\x00\x00\x01\x00\x01\x01\x00\x00\x00\x01\x00"
    """
    return b"".join(integer2bits(c,8) for c in iterateints(data))


def bits2bytes(data):
    r""" 
    Create a binary representation of a b-string.

    Example:

        >>> bits2bytes(b"\x00\x01\x01\x00\x00\x00\x00\x01\x00\x01\x01\x00\x00\x00\x01\x00")
        b'ab'
    """
    if len(data) & 7:
        raise ValueError("data length must be a multiple of 8")
    return b"".join(int2byte(bits2integer(data[i:i+8])) for i in range(0,len(data),8))


def swapbitslines(data, linesize=8):
    r"""
    Bits is a b-string containing a binary representation. Assuming each linesize bits constitute a byte, perform an endianness byte swap.

    Example:

        >>> swapbitslines(b'00011011', 2)
        b'11100100'
        >>> swapbitslines(b'0000000011111111', 8)
        b'1111111100000000'
    """
    if len(data) % linesize:
        raise ValueError("data length must be multiple of linesize")
    if linesize < 1:
        raise ValueError("linesize must be a positive number")
    return b"".join(data[i:i+linesize] for i in reversed(range(0,len(data),linesize)))

