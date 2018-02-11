from declarativeunittest import *
from construct import *
from construct.lib import *


def test_multiprocessing():
    import multiprocessing

    def worker(q):
        obj = q.get()
        print(obj)

    queue = multiprocessing.Queue()

    p = multiprocessing.Process(target=worker, args=(queue,))
    p.start()

    obj = Container(name="test")
    print(obj)
    queue.put(obj)

    # Wait for the worker to finish
    queue.close()
    queue.join_thread()
    p.join()
