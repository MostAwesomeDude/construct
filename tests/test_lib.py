import declarativeunittest

from construct.lib.binary import *


class TestBinary(declarativeunittest.TestCase):
    def alltestsinteractive(self):

        yield [integer2bits(19, 5), b"\x01\x00\x00\x01\x01"]
        yield [integer2bits(19, 8), b'\x00\x00\x00\x01\x00\x00\x01\x01']
        yield [integer2bits(19, 3), b'\x00\x01\x01']
        yield [integer2bits(-13, 5), b"\x01\x00\x00\x01\x01"]
        yield [integer2bits(-13, 8), b"\x01\x01\x01\x01\x00\x00\x01\x01"]
        self.assertRaises(ValueError, integer2bits, 19, 0)
        self.assertRaises(ValueError, integer2bits, 19, -1)
        self.assertRaises(ValueError, integer2bits, -19, 0)
        self.assertRaises(ValueError, integer2bits, -19, -1)

        yield [integer2bytes(0, 4), b"\x00\x00\x00\x00"]
        yield [integer2bytes(1, 4), b"\x00\x00\x00\x01"]
        yield [integer2bytes(255, 4), b"\x00\x00\x00\xff"]
        yield [integer2bytes(-1, 4), b"\xff\xff\xff\xff"]
        yield [integer2bytes(-255, 4), b"\xff\xff\xff\x01"]
        self.assertRaises(ValueError, integer2bytes, 19, 0)
        self.assertRaises(ValueError, integer2bytes, 19, -1)
        self.assertRaises(ValueError, integer2bytes, -19, 0)
        self.assertRaises(ValueError, integer2bytes, -19, -1)

        yield [bits2integer(b"\x01\x00\x00\x01\x01"), 19]
        yield [bits2integer(b"\x01\x00\x00\x01\x01", True), -13]
        yield [bits2integer(b"10011"), 19]
        yield [bits2integer(b"10011", True), -13]

        for i in [-300,-255,-100,-1,0,1,100,255,300]:
            yield [bits2integer(integer2bits(i,64),signed=(i<0)), i]
            yield [bytes2integer(integer2bytes(i,8),signed=(i<0)), i]
            yield [bits2bytes(integer2bits(i,64)), integer2bytes(i,8)]
            yield [bytes2bits(integer2bytes(i,8)), integer2bits(i,64)]

        yield [bytes2bits(b"ab"), b"\x00\x01\x01\x00\x00\x00\x00\x01\x00\x01\x01\x00\x00\x00\x01\x00"]
        yield [bytes2bits(b""), b""]

        yield [bits2bytes(b"\x00\x01\x01\x00\x00\x00\x00\x01\x00\x01\x01\x00\x00\x00\x01\x00"), b"ab"]
        yield [bits2bytes(b""), b""]
        self.assertRaises(ValueError, bits2bytes, b"\x00")
        self.assertRaises(ValueError, bits2bytes, b"\x00\x00\x00\x00\x00\x00\x00")

        yield [swapbytes(b"aaaabbbbcccc", 4), b"ccccbbbbaaaa"]
        yield [swapbytes(b"abcdefgh", 2), b"ghefcdab"]
        yield [swapbytes(b"00011011", 2), b"11100100"]
        yield [swapbytes(b"", 2), b""]
        self.assertRaises(ValueError, swapbytes, b"12345678", 7)
        self.assertRaises(ValueError, swapbytes, b"12345678", -4)


