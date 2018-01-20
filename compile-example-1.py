# Struct(
# 	"sig" / Const(b"MZ"),
# 	"inner" / Struct(
# 		"num" / Int8ub,
# 		"data" / Bytes(this.num),
# 		"ps" / PascalString(Int8ub, encoding="utf8"),
# 	)
# 	Check(this.sig == b"MZ"),
# 	"inner2" / Sequence(
# 		Int8ub,
# 		"num" / Int8ub,
# 	),
# )

# >>> timeit('f()', setup='def f(): pass')
# 0.09585036399948876
# >>> timeit('f(0,1,2)', setup='def f(a,b,c): pass')
# 0.11116954099998111

# compiles into

from construct import Container
from io import BytesIO
from struct import pack, unpack, calcsize


def read_bytes(io, count):
	assert count >= 0
	data = io.read(count)
	assert len(data) == count
	return data

def parse_const(io, value):
	data = read_bytes(io, len(value))
	assert data == value
	return value

def parse_formatfield(io, format, length):
	return unpack(format, read_bytes(io, length))[0]

def parse_pascalstring(io, encoding, length):
	data = read_bytes(io, length)
	return data.decode(encoding) if encoding else data

def parse_struct_1(io, context):
	class FIELDS:
		__slots__ = ["_","num","data","ps"]
	this = FIELDS()
	this._ = context
	this.num = parse_formatfield(io, "b", 1)
	this.data = read_bytes(io, this.num)
	this.ps = parse_pascalstring(io, "utf8", parse_formatfield(io, "b", 1))
	this._ = None
	return this

def parse_check(condition):
	assert condition

def parse_sequence_3(io, context):
	class FIELDS:
		__slots__ = ["_","num"]
	result = []
	this = FIELDS()
	this._ = context
	result.append(parse_formatfield(io, "b", 1))
	result.append(parse_formatfield(io, "b", 1))
	this.num = result[-1]
	return result

def parse_struct_4(io, context):
	class FIELDS:
		__slots__ = ["_","sig","inner","inner2"]
	this = FIELDS()
	this._ = context
	this.sig = parse_const(io, b"MZ")
	this.inner = parse_struct_1(io, this)
	parse_check(this.sig == b"MZ")
	this.inner2 = parse_sequence_3(io, this)
	this._ = None
	return this

def parse_all(io, context):
	return parse_struct_4(io, context)
