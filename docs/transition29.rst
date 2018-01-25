=================
Transition to 2.9
=================

Overall
=======

**Compilation feature for faster performance!** Read `this chapter <https://construct.readthedocs.io/en/latest/compilation.html>`_ for tutorial, particularly its restrictions section.


General classes
-----------------

Compiled CompilableMacro added (used internally)

FocusedSeq uses nested context (alike Struct and Sequence)

FieldError was replaced with StreamError (raised when stream returns less than requested amount) and FormatFieldError (raised by FormatField class, for example if building Float from non-float value and struct.pack complaining).

HexString removed
