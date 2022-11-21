import asyncio
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp


class PoolRunner:
    """PoolRunner

    Wraps a process pool to allow its use from async functions.

    Useful for calling code that may misbehave in multithreaded environments
    (e.g code that forks or uses signals) from a program that uses
    multithreading + asyncio.
    """
    def __init__(self):
        ctx = mp.get_context("forkserver")
        self._pool = ProcessPoolExecutor(mp_context=ctx)

    async def run(self, func, *args, **kwargs):
        """ Run func(*args, **kwargs) in a separate process.

        Arguments and return value have to support pickling.
        """
        task = self._pool.submit(func, *args, **kwargs)
        return await asyncio.wrap_future(task)
