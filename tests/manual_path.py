from construct import *

st = "outter" / Struct(
    "inner" / Struct(
        "spam" / Enum(Byte,
            ABC = 1,
            DEF = 2,
            GHI = 3,
        ),
        "eggs" / VarInt,
    ),
)

print(st.parse(b"\xff\x01"))
print(st.build(dict(inner=dict(spam=255))))
print(st.sizeof())

