=================
Transition to 2.9
=================

Overall
=======

**Compilation feature for faster performance!** Read `this chapter <https://construct.readthedocs.io/en/latest/compilation.html>`_ for tutorial, particularly its restrictions section.

**Docstrings of all classes were overhauled.** Check the `Core API pages <https://construct.readthedocs.io/en/latest/index.html#api-reference>`_.


General classes
-----------------

All constructs: `parse build sizeof` methods take context entries ONLY as keyword parameters \*\*kw

Compiled CompilableMacro added (used internally)

FocusedSeq uses nested context (alike Struct and Sequence)

HexString removed


Exceptions
-------------

FieldError was replaced with StreamError (raised when stream returns less than requested amount) and FormatFieldError (raised by FormatField class, for example if building Float from non-float value and struct.pack complains).
