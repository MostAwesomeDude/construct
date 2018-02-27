from construct import *

d = Struct(
    "count" / Int32ul,
    "items" / Array(this.count, Struct(
        "num1" / Int8ul,
        "num2" / Int24ul,
        "flags" / BitStruct(
            "bool1" / Flag,
            "num4" / BitsInteger(3),
            Padding(4),
        ),
        "fixedarray1" / Array(3, Int8ul),
        "name1" / CString("utf8"),
        "name2" / PascalString(Int8ul, "utf8"),
    )),
)


data = d.build(dict(count=1000, items=[dict(num1=0, num2=0, flags=dict(bool1=True, num4=0), fixedarray1=[0,0,0], name1=u"...", name2=u"...") for i in range(1000)]))
with open("blob","wb") as f:
    f.write(data)

# from timeit import timeit
# d.parse(data)
# parsetime = timeit(lambda: d.parse(data), number=1000)/1000
# print("Timeit measurements:")
# print("parsing:           {:.10f} sec/call".format(parsetime))

d = d.compile()
print(d.benchmark(data))
