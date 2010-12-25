from repr import repr as repr2


def recursion_lock(retval, lock_name = "__recursion_lock__"):
    def decorator(func):
        def wrapper(self, *args, **kw):
            if getattr(self, lock_name, False):
                return retval
            setattr(self, lock_name, True)
            try:
                return func(self, *args, **kw)
            finally:
                setattr(self, lock_name, False)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator


class Formatter():
    def __init__(self, obj):
        self.__obj = obj
        self.__locked = False
    def __repr__(self):
        self.__obj
    def __getattr__(self, name):
        return(self.__obj, name)

class ReprFormatter(object):
    def __init__(self, subobj):
        self.__subobj = subobj
        self.__locked = False
    def __repr__(self):
        pass
    
        
        obj, nesting, indentation = "    "):
    items = obj.__introspect__()
    return 
















