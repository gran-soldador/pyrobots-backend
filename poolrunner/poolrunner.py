import asyncio
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp


class PoolRunner:
    def __init__(self):
        ctx = mp.get_context("forkserver")
        self._pool = ProcessPoolExecutor(mp_context=ctx)

    async def run(self, func, *args, **kwargs):
        task = self._pool.submit(func, *args, **kwargs)
        return await asyncio.wrap_future(task)
