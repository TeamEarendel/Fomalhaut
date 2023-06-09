from multiprocessing import Queue

from .core.SharedData import SharedData as _SharedData
from .Instance import Instance as _Instance


def run():
    q: Queue = Queue()
    q.put(_SharedData())
    _Instance(q, "Fomalhaut")
