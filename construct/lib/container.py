"""
Various containers.
"""


def recursion_lock(retval="<recursion detected>", lock_name="__recursion_lock__"):
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
    Generic ordered dictionary that allows both key and attribute access.

    Containers are dictionaries, translating attribute access into key access, and preserving key order. Also they use call method to add keys, because **kw does not preserve order.

    Structs parse return containers, becuase their fields have order.

    Example::

        Container([ ("name","anonymous"), ("age",21) ])
        
        Container(name="anonymous")(age=21)

        # This is NOT correct because keyword arguments order is not preserved.
        Container(name="anonymous", age=21)

        Container(container2)
    """
    __slots__ = ["__keys_order__","__recursion_lock__"]

    def __init__(self, *args, **kw):
        object.__setattr__(self, "__keys_order__", [])
        if isinstance(args, dict):
            for k, v in args.items():
                self[k] = v
            return
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v
            else:
                for k, v in arg:
                    self[k] = v
        for k, v in kw.items():
            self[k] = v

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setitem__(self, key, val):
        if key not in self:
            self.__keys_order__.append(key)
        dict.__setitem__(self, key, val)

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self.__keys_order__.remove(key)

    __delattr__ = __delitem__
    __setattr__ = __setitem__

    def __call__(self, **kw):
        """
        Chains adding new entries to the same container. See ctor.
        """
        for k,v in kw.items():
            self.__setitem__(k, v)
        return self

    def clear(self):
        dict.clear(self)
        del self.__keys_order__[:]

    def pop(self, key, *default):
        """
        Removes and returns the value for a given key, raises KeyError if not found.
        """
        val = dict.pop(self, key, *default)
        self.__keys_order__.remove(key)
        return val

    def popitem(self):
        """
        Removes and returns the last key and value from order.
        """
        k = self.__keys_order__.pop()
        v = dict.pop(k)
        return k, v

    def update(self, seqordict, **kw):
        if isinstance(seqordict, dict):
            for k, v in seqordict.items():
                self[k] = v
        else:
            for k, v in seqordict:
                self[k] = v
        dict.update(self, kw)

    def copy(self):
        return Container(self.iteritems())

    __update__ = update
    __copy__ = copy

    def iterkeys(self):
        return iter(self.__keys_order__)

    def itervalues(self):
        return (self[k] for k in self.__keys_order__)

    def iteritems(self):
        return ((k, self[k]) for k in self.__keys_order__)

    def keys(self):
        return self.__keys_order__

    def values(self):
        return list(self.itervalues())

    def items(self):
        return list(self.iteritems())

    __iter__ = iterkeys

    def __eq__(self, other, skiporder=False):
        if not isinstance(other, dict):
            return False
        if len(self) != len(other):
            return False
        if skiporder:
            for k,v in self.iteritems():
                if k not in other or v != other[k]:
                    return False
        else:
            for (k,v),(k2,v2) in zip(self.iteritems(), other.iteritems()):
                if k != k2 or v != v2:
                    return False
        return True

    def __ne__(self, other, skiporder=False):
        return not self.__eq__(other, skiporder)

    def _search(self, name, search_all):
        items = []
        for key in self.keys():
            try:
                if key == name:
                    if search_all:
                        items.append(self[key])
                    else:
                        return self[key]
                if type(self[key]) == Container or type(self[key]) == ListContainer:
                    ret = self[key]._search(name, search_all)
                    if ret is not None:
                        if search_all:
                            items.extend(ret)
                        else:
                            return ret
            except:
                pass
        if search_all:
            return items
        else:
            return None

    def search(self, name):
        return self._search(name, False)

    def search_all(self, name):
        return self._search(name, True)

    @recursion_lock()
    def __repr__(self):
        parts = ["Container"]
        for k,v in self.iteritems():
            if not k.startswith("_"):
                parts.extend(["(",str(k),"=",repr(v),")"])
        if len(parts) == 1:
            parts.append("()")
        return "".join(parts)

    @recursion_lock()
    def __str__(self, indentation="\n    "):
        text = ["Container: "]
        for k,v in self.iteritems():
            if not k.startswith("_"):
                text.extend([indentation, k, " = "])
                text.append(indentation.join(str(v).split("\n")))
        return "".join(text)


class FlagsContainer(Container):
    r"""
    A container providing pretty-printing for flags.

    Only set flags are displayed.
    """

    def __eq__(self, other, skiporder=True):
        return super(FlagsContainer, self).__eq__(other, skiporder)

    def __ne__(self, other, skiporder=True):
        return not self.__eq__(other, skiporder)

    @recursion_lock()
    def __str__(self, indentation="\n    "):
        text = ["FlagsContainer: "]
        for k,v in self.iteritems():
            if not k.startswith("_") and v:
                text.extend([indentation, k, " = "])
                lines = str(v).split("\n")
                text.append(indentation.join(lines))
        return "".join(text)


class ListContainer(list):
    r"""
    A container for lists.
    """

    @recursion_lock()
    def __str__(self, indentation="\n    "):
        text = ["ListContainer: "]
        for k in self:
            text.extend([indentation])
            lines = str(k).split("\n")
            text.append(indentation.join(lines))
        return "".join(text)

    def _search(self, name, search_all):
        items = []
        for item in self:
            try:
                ret = item._search(name, search_all)
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

    def search(self, name):
        return self._search(name, False)

    def search_all(self, name):
        return self._search(name, True)


class LazyContainer(object):
    __slots__ = ["subcons", "offsetmap", "cached", "stream", "addoffset", "context", "count"]

    def __init__(self, subcons, offsetmap, cached, stream, addoffset, context):
        self.subcons = subcons
        self.offsetmap = offsetmap
        self.cached = cached
        self.stream = stream
        self.addoffset = addoffset
        self.context = context
        self.count = len(self.keys())

    def __getitem__(self, key):
        if key not in self.cached:
            at, sc = self.offsetmap.pop(key)
            self.stream.seek(self.addoffset + at)
            self.cached[key] = sc._parse(self.stream, self.context)
        return self.cached[key]

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __len__(self):
        return self.count

    def keys(self):
        return list(sc.name for sc in self.subcons if sc.name is not None)

    def __eq__(self, other):
        try:
            for name in self.keys():
                if self[name] != other[name]:
                    return False
            for name in other.keys():
                if self[name] != other[name]:
                    return False
            return True
        except KeyError:
            return False

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        if self._value is NotImplemented:
            text = "<unread>"
        else:
            text = str(self._value)
        return "%s: %s" % (self.__class__.__name__, text)

    def read(self):
        self.stream.seek(self.pos)
        return self.subcon._parse(self.stream, self.context)

    def dispose(self):
        self.subcon = None
        self.stream = None
        self.context = None
        self.pos = None

    def _get_value(self):
        if self._value is NotImplemented:
            self._value = self.read()
        return self._value

    value = property(_get_value)

    has_value = property(lambda self: self._value is not NotImplemented)



class LazyListContainer(ListContainer):
    __slots__ = ["subcon", "subsize", "count", "stream", "addoffset", "context", "cached"]

    def __init__(self, subcon, subsize, count, stream, addoffset, context):
        self.subcon = subcon
        self.subsize = subsize
        self.count = count
        self.stream = stream
        self.addoffset = addoffset
        self.context = context
        self.cached = {}

    def __getitem__(self, index):
        if not 0 <= index < count:
            raise ValueError("index %d out of range 0-%d" % (index,self.count-1))
        if index not in self.cached:
            self.stream.seek(self.addoffset + index * self.subsize)
            self.cached[index] = self.subcon._parse(self.stream, self.context)
        return self.cached[index]

    def __len__(self):
        return self.count

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for i in range(self.count):
            if self[i] != other[i]:
                return False
        return True


