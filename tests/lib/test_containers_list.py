from declarativeunittest import *
from construct import *
from construct.lib import *


def test_str():
    l = ListContainer(range(5))
    assert str(l)
    assert repr(l)

    l = ListContainer(range(5))
    l.append(l)
    assert str(l)
    assert repr(l)
