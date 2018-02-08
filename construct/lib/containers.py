from construct.lib.py3compat import *
import re


globalfullprinting = None


def setglobalfullprinting(enabled):
    r"""
    Sets full printing for all Container instances. When enabled, Container __str__ produces full content of bytes and strings, otherwise and by default, it produces truncated output.

    :param enabled: bool to enable or disable full printing, or None to default
    """
    global globalfullprinting
    globalfullprinting = enabled


def recursion_lock(retval="<recursion detected>", lock_name="__recursion_lock__"):
    """Used internally."""
    def decorator(func):
        def wrapper(self, *args, **kw):
            if getattr(self, lock_name, False):
                return retval
            setattr(self, lock_name, True)
            try:
                return func(self, *args, **kw)
            finally:
                delattr(self, lock_name)

        wrapper.__name__ = func.__name__
        return wrapper

    return decorator


class Container(dict):
    r"""
    Generic ordered dictionary that allows both key and attribute access, and preserves key order by insertion. Adding keys is preferred using \*\*kw (requires Python 3.6). Equality does NOT check item order. Also provides regex searching.

	This container is mostly used by Struct construct, since its members have order, so do the values parsed.

    Example::

        # empty dict
        >>> Container()
        # list of pairs, not recommended
        >>> Container([ ("name","anonymous"), ("age",21) ])
        # This syntax requires Python 3.6
        >>> Container(name="anonymous", age=21)
        # This syntax is for internal use only
        >>> Container(name="anonymous")(age=21)
        # copies another dict
        >>> Container(dict2)
        >>> Container(container2)
    """
    __slots__ = ["__keys_order__", "__recursion_lock__"]

    def __getattr__(self, name):
        try:
            if name in self.__slots__:
                try:
                    return object.__getattribute__(self, name)
                except AttributeError as e:
                    if name == "__keys_order__":
                        r = []
                        object.__setattr__(self, "__keys_order__", r)
                        return r
                    else:
                        raise e
            else:
                return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        try:
            if name in self.__slots__:
                return object.__setattr__(self, name, value)
            else:
                self[name] = value
        except KeyError:
            raise AttributeError(name)

    def __delattr__(self, name):
        try:
            if name in self.__slots__:
                return object.__delattr__(self, name)
            else:
                del self[name]
        except KeyError:
            raise AttributeError(name)

    def __setitem__(self, key, value):
        if key not in self:
            self.__keys_order__.append(key)
        dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        """Removes an item from the Container in linear time O(n)."""
        if key in self:
            self.__keys_order__.remove(key)
        dict.__delitem__(self, key)

    def __init__(self, *args, **kw):
        self.__keys_order__ = []
        for arg in args:
            if isinstance(arg, dict):
                for k,v in arg.items():
                    self[k] = v
            else:
                for k,v in arg:
                    self[k] = v
        for k,v in kw.items():
            self[k] = v

    def __call__(self, **kw):
        """Chains adding new entries to the same container. See ctor."""
        for k,v in kw.items():
            self[k] = v
        return self

    def keys(self):
        return iter(self.__keys_order__)

    def values(self):
        return (self[k] for k in self.__keys_order__)

    def items(self):
        return ((k, self[k]) for k in self.__keys_order__)

    __iter__ = keys

    def clear(self):
        dict.clear(self)
        self.__keys_order__ = []

    def pop(self, key):
        """Removes and returns the value for a given key, raises KeyError if not found."""
        val = dict.pop(self, key)
        self.__keys_order__.remove(key)
        return val

    def popitem(self):
        """Removes and returns the last key and value from order."""
        k = self.__keys_order__.pop()
        v = dict.pop(self, k)
        return k, v

    def update(self, seqordict):
        if isinstance(seqordict, dict):
            seqordict = seqordict.items()
        for k,v in seqordict:
            self[k] = v

    def __getstate__(self):
        return self.__keys_order__

    def __setstate__(self, state):
        self.__keys_order__ = state

    def copy(self):
        return Container(self)

    __update__ = update

    __copy__ = copy

    def __dir__(self):
        """For auto completion of attributes based on container values."""
        return list(self.keys()) + list(self.__class__.__dict__) + dir(super(Container, self))

    def __eq__(self, other):
        if not isinstance(other, dict):
            return False
        if len(self) != len(other):
            return False
        def isequal(v1, v2):
            if v1.__class__.__name__ == "ndarray" or v2.__class__.__name__ == "ndarray":
                import numpy
                return numpy.array_equal(v1, v2)
            return v1 == v2
        for k,v in self.items():
            if k not in other or not isequal(v, other[k]):
                return False
        return True

    @recursion_lock()
    def __repr__(self):
        parts = ["Container"]
        for k,v in self.items():
            if not isinstance(k,str) or not k.startswith("_"):
                parts.extend(["(", str(k), "=", repr(v), ")"])
        if len(parts) == 1:
            parts.append("()")
        return "".join(parts)

    @recursion_lock()
    def __str__(self, indentation="\n    "):
        printingcap = 64
        text = ["Container: "]
        for k,v in self.items():
            if not isinstance(k,str) or not k.startswith("_"):
                text.extend([indentation, str(k), " = "])
                if isinstance(v, stringtypes):
                    if len(v) <= printingcap or globalfullprinting:
                        text.append("%s (total %d)" % (reprbytes(v), len(v)))
                    else:
                        text.append("%s... (truncated, total %d)" % (reprbytes(v[:printingcap]), len(v)))
                else:
                    text.append(indentation.join(str(v).split("\n")))
        return "".join(text)

    def _search(self, compiled_pattern, search_all):
        items = []
        for key in self.keys():
            try:
                if isinstance(self[key], (Container,ListContainer)):
                    ret = self[key]._search(compiled_pattern, search_all)
                    if ret is not None:
                        if search_all:
                            items.extend(ret)
                        else:
                            return ret
                elif compiled_pattern.match(key):
                    if search_all:
                        items.append(self[key])
                    else:
                        return self[key]
            except:
                pass
        if search_all:
            return items
        else:
            return None

    def search(self, pattern):
        compiled_pattern = re.compile(pattern)
        return self._search(compiled_pattern, False)

    def search_all(self, pattern):
        compiled_pattern = re.compile(pattern)
        return self._search(compiled_pattern, True)


class FlagsContainer(Container):
    r"""
    Container class derivative, extended for representing FlagsEnum. Equality does NOT check item order. Provides pretty-printing for flags, showing only values set to True. Also provides regex searching.
    """

    @recursion_lock()
    def __str__(self, indentation="\n    "):
        text = ["FlagsContainer: "]
        for k,v in self.items():
            if not k.startswith("_") and v:
                text.extend([indentation, k, " = "])
                lines = str(v).split("\n")
                text.append(indentation.join(lines))
        return "".join(text)


class ListContainer(list):
    r"""
    Generic container like list. Provides pretty-printing. Also provides regex searching.
    """

    @recursion_lock()
    def __str__(self, indentation="\n    "):
        text = ["ListContainer: "]
        for k in self:
            text.append(indentation)
            lines = str(k).split("\n")
            text.append(indentation.join(lines))
        return "".join(text)

    def _search(self, compiled_pattern, search_all):
        items = []
        for item in self:
            try:
                ret = item._search(compiled_pattern, search_all)
            except:
                continue
            if ret is not None:
                if search_all:
                    items.extend(ret)
                else:
                    return ret
        if search_all:
            return items
        else:
            return None

    def search(self, pattern):
        compiled_pattern = re.compile(pattern)
        return self._search(compiled_pattern, False)

    def search_all(self, pattern):
        compiled_pattern = re.compile(pattern)
        return self._search(compiled_pattern, True)

