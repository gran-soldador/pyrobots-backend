import pytest
from os import getpid

from utils.poolrunner import *


def echo(*args, **kwargs):  # pragma: no cover
    return getpid(), args, kwargs


@pytest.mark.asyncio
async def test_run():
    runner = PoolRunner()
    args = (1, "a", {})
    kwargs = {"key1": "value1", "key2": None}
    pid, ret_args, ret_kwargs = await runner.run(echo, *args, **kwargs)
    assert pid != getpid()
    assert args == ret_args
    assert kwargs == ret_kwargs
