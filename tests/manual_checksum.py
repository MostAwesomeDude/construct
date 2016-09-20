from construct import *
import hashlib

def sha512(b):
    return hashlib.sha512(b).digest()
d = Struct(
    "fields" / RawCopy(Struct(
        "a" / Byte,
        "b" / Byte,
    )),
    "checksum" / Checksum(Bytes(64), sha512, "fields"),
)

data = d.build(dict(fields=dict(value=dict(a=1,b=2))))
print(data)
# returned
b'\x01\x02\xbd\xd8\x1a\xb23\xbc\xebj\xd23\xcd\x18qP\x93 \xa1\x8d\x035\xa8\x91\xcf\x98s\t\x90\xe8\x92>\x1d\xda\x04\xf35\x8e\x9c~\x1c=\x16\xb1o@\x8c\xfa\xfbj\xf52T\xef0#\xed$6S8\x08\xb6\xca\x993'
