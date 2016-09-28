=======================
Adapters and Validators
=======================

Adapting
========

Adapting is the process of converting one representation of an object to another. One representation is usually "lower" (closer to the byte level), and the other "higher" (closer to the python object model). The process of converting the lower representation to the higher one is called decoding, and the process of converting the higher level representation to the lower one is called encoding. Encoding and decoding are expected to be symmetrical, so that they counter-act each other ``encode(decode(x)) == x`` and ``decode(encode(x)) == x``.

Custom adapter classes derive of the abstract Adapter class, and implement their own versions of ``_encode`` and ``_decode``, as shown below:

>>> class IpAddressAdapter(Adapter):
...     def _encode(self, obj, context):
...         return list(map(int, obj.split(".")))
...     def _decode(self, obj, context):
...         return "{0}.{1}.{2}.{3}".format(*obj)
...
>>> IpAddress = IpAddressAdapter(Byte[4])

As you can see, the IpAddressAdapter encodes strings of the format "XXX.XXX.XXX.XXX" to a binary string of 4 bytes, and decodes such binary strings into the more readable "XXX.XXX.XXX.XXX" format. Also note that the adapter does not perform any manipulation of the stream, it only converts between the objects!

This is called separation of concern, and is a key feature of component-oriented programming. It allows us to keep each component very simple and unaware of its consumers. Whenever we need a different representation of the data, we don't need to write a new Construct -- we only write the suitable adapter.

So, let's see our adapter in action:

>>> IpAddress.parse(b"\x01\x02\x03\x04")
'1.2.3.4'
>>> IpAddress.build("192.168.2.3")
b'\xc0\xa8\x02\x03'

Having the representation separated from the actual parsing or building means an adapter is loosely coupled with its underlying construct. As we'll see with enums in a moment, we can use the same enum for ``Byte`` or ``Int32sl`` or ``Float64l``, as long as the underlying construct returns an object we can map. Moreover, we can stack several adapters on top of one another, to created a nested adapter.

Enums
-----

Enums provide symmetrical name-to-value mapping. The name may be misleading, as it's not an enumeration as you would expect in C. But since enums in C are often just used as a collection of named values, we'll stick with the name. Hint: enums are implemented by the ``Mapping`` adapter, which provides mapping of values to other values (not necessarily names to numbers).

>>> c = Enum(Byte, TCP=6, UDP=17)
>>> c.parse(b"\x06")
'TCP'
>>> c.build("UDP")
b'\x11'
>>> c.build(17)
b'\x11'

We can also supply a default mapped value when no mapping exists for them. We do this by supplying a keyword argument named ``default``. If we don't supply a default value, an exception is raised.

>>> c = Enum(Byte, TCP=6, UDP=17)
>>> c.parse(b"\xff")
construct.core.MappingError: no decoding mapping for 255
>>> c.build("unknown")
construct.core.MappingError: no encoding mapping for 'unknown'

>>> c = Enum(Byte, TCP=6, UDP=17, default=0)
>>> c.parse(b"\xff")
0
>>> c.build(99)
b'\x00'

We can also just "pass through" unmapped values. We do this by supplying ``default = Pass``. If you are curious, ``Pass`` is a special construct that "does nothing"; in this context, we use it to indicate the Enum to "pass through" the unmapped value as-is.

>>> c = Enum(Byte, TCP=6, UDP=17, default=Pass)
>>> c.parse(b"\xff")
255

Using expressions instead of classes
------------------------------------

Adaters can be created declaratively using ExprAdapter:

>>> IpAddress = ExprAdapter(Byte[4], 
...     encoder = lambda obj,ctx: list(map(int, obj.split("."))),
...     decoder = lambda obj,ctx: "{0}.{1}.{2}.{3}".format(*obj), )


Validating
==========

Validating means making sure the parsed/built object meets a given condition. Validators simply raise the ``ValidatorError`` if the object is invalid. They are usually used to make sure a "magic number" is found, the correct version of the protocol, a file signature is matched. You can write custom validators by deriving from the Validator class and implementing the ``_validate`` method. This allows you to write validators for more complex things, such as making sure a CRC field (or even a cryptographic hash) is correct.

The two most common cases already exist as builtins. 

.. autoclass:: construct.NoneOf

.. autoclass:: construct.OneOf

Notice that `OneOf(dtype, [value])` is essentially equivalent to `Const(dtype, value)`.

.. autoclass:: construct.Filter


Using expressions instead of classes
------------------------------------

Validators can be created declaratively using ExprValidator:

>>> OneOf = ExprValidator(Byte, 
... 	validator = lambda obj,ctx: obj in [1,3,5])


Checking
========

Checks can also be made using the context, being done just in the middle of parsing or building and not on a particular object.

.. autoclass:: construct.Check


