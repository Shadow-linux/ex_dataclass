"""
Concurrent Process
"""
import os
import typing
from concurrent.futures import Future, as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures.process import ProcessPoolExecutor

from src.m import ToolImpl

__all__ = [
    "FutureTurboEngine"
]


class FutureTurboEngine(ToolImpl):

    def __init__(self, max_workers: int = None, thread_name_prefix: str = None):
        # self.__engine = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix=thread_name_prefix)
        self.__engine = ProcessPoolExecutor(max_workers=max_workers)
        # task q
        self.__fuel_q: typing.List[Future] = []
        super().__init__()

    # submit execute function
    def refuel(self, future_fun: typing.Callable, *args, **kwargs):
        self.__fuel_q.append(self.__engine.submit(future_fun, *args, **kwargs))


    def as_complete(self):
        for future in as_completed(self.__fuel_q):
            result = future.result()
            yield result
