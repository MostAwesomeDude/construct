from construct import *

foo = Struct(
    "bar" / Byte,
    Debugger(
        "spam" / Enum(Byte,
            ABC = 1,
            DEF = 2,
            GHI = 3,
        )
    ),
    "eggs" / Byte,
)

print(foo.parse(b"\x01\x02\x03"))
print(foo.parse(b"\x01\x04\x03"))

