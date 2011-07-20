Adapting
========

Adapting is the process of converting one representation of an object to
another. One representation is usually "lower" (closer to the byte level), and
the other "higher" (closer to the python object model). The process of
converting the lower representation to the higher one is called decoding, and
the process of converting the higher level representation to the lower one is
called encoding. Encoding and decoding are expected to be symmetrical, so that
they counter-act each other (``encode(decode(x)) == x`` and ``decode(encode(x))
== x``).

Custom adapter classes derive of the abstract Adapter class, and implement
their own versions of ``_encode`` and ``_decode``, as shown below:

>>> class IpAddressAdapter(Adapter):
...     def _encode(self, obj, context):
...         return "".join(chr(int(b)) for b in obj.split("."))
...     def _decode(self, obj, context):
...         return ".".join(str(ord(b)) for b in obj)
...


As you can see, the IpAddressAdapter encodes strings of the format
"XXX.XXX.XXX.XXX" to a binary string of 4 bytes, and decodes such binary
strings into the more readable "XXX.XXX.XXX.XXX" format. Also note that the
adapter does not perform any manipulation of the stream, it only converts the
object!

This is called separation of concern, and is a key feature of
component-oriented programming. It allows us to keep each component very
simple and unaware of its consumers. Whenever we need a different
representation of the data, we don't need to write a new Construct -- we only
write the suitable adapter.

So, let's see our adapter in action:

>>> IpAddressAdapter(Bytes("foo", 4)).parse("\x01\x02\x03\x04")
'1.2.3.4'
>>> IpAddressAdapter(Bytes("foo", 4)).build("192.168.2.3")
'\xc0\xa8\x02\x03'


We can also use macro functions, to bind an adapter to a construct, instead of
having to do so manually every time:

>>> def IpAddress(name):
...    return IpAddressAdapter(Bytes(name, 4))
...
>>> IpAddress("foo").build("10.0.0.1")
'\n\x00\x00\x01'


Having the representation separated from the actual parsing or building means
an adapter is loosely coupled with its underlying construct. As we'll see with
enums in a moment, we can use the same enum for ``UBInt8``, ``SLInt32``, or
``LFloat64``, etc., as long as the underlying construct returns an object we
can map. Moreover, we can stack several adapters on top of one another, to
created a nested adapter.

Enums
-----

Enums provide symmetrical name-to-value mapping. The name may be misleading,
as it's not an enumeration as you would expect in C. But since enums in C are
often just used as a collection of named values, we'll stick with the name.
Hint: enums are implemented by the ``MappingAdapter``, which provides mapping
of values to other values (not necessarily names to numbers).

>>> c = Enum(Byte("protocol"),
...     TCP = 6,
...     UDP = 17,
... )
>>> c
<MappingAdapter('protocol')>

>>> # parsing
>>> c.parse("\x06")
'TCP'
>>> c.parse("\x11")
'UDP'
>>> c.parse("\x12")
Traceback (most recent call last):
  .
  .
construct.adapters.MappingAdapterError: undefined mapping for 18

>>> # building
>>> c.build("TCP")
'\x06'
>>> c.build("UDP")
'\x11'
>>>


We can also supply a default mapped value when no mapping exists for them. We
do this by supplying a keyword argument named ``_default_`` (a single uderscore
on each side). If we don't supply a default value, an exception is raised (as
we saw in the previous snippet).

>>> c = Enum(Byte("protocol"),
...     TCP = 6,
...     UDP = 17,
...     _default_ = "blah"
... )
>>> c.parse("\x11")
'UDP'
>>> c.parse("\x12") # no mapping for 18, so default to "blah"
'blah'
>>>


We can also just "pass through" unmapped values. We do this by supplying
``_default_ = Pass``. If you are curious, ``Pass`` is a special construct that
"does nothing"; in this context, we use it to indicate the Enum to "pass
through" the unmapped value as-is.

>>> c = Enum(Byte("protocol"),
...     TCP = 6,
...     UDP = 17,
...     _default_ = Pass
... )
>>> c.parse("\x11")
'UDP'
>>> c.parse("\x12") # no mapping, passing through
18
>>> c.parse("\xff") # no mapping, passing through
255


When we wish to use the same enum multiple times, we will use a simple macro
function. This keeps us conforming to the Don't Repeat Yourself principle:

>>> def ProtocolEnum(subcon):
...     return Enum(subcon,
...         ICMP = 1,
...         TCP = 6,
...         UDP = 17,
...     )
...
>>> ProtocolEnum(UBInt8("foo")).parse("\x06")
'TCP'
>>> ProtocolEnum(UBInt16("foo")).parse("\x00\x06")
'TCP'
>>>


Validating
==========

Validating means making sure the parsed/built object meets a given condition.
Validators simply raise an exception (``ValidatorError``) if the object is
invalid. The two most common cases already exist as builtins.

Validators are usually used to make sure a "magic number" is found, the
correct version of the protocol, a file signature is matched, etc. You can
write custom validators by deriving from the Validator class and implementing
the ``_validate`` method; this allows you to write validators for more complex
things, such as making sure a CRC field (or even a cryptographic hash) is
correct, etc.

.. autoclass:: construct.NoneOf

.. autoclass:: construct.OneOf
