# import unittest.mock as mock
import mock
import pytest

from engine.outputmodels import MatchResult, RobotId
from engine.gamemanager import *


@pytest.fixture
def echo_func():
    async def echo(*args, **kwargs):
        return args, kwargs
    return echo


@pytest.fixture
def mocked_poolrunner():
    def apply(self, f, *args, **kwargs):
        return f(*args, **kwargs)
    with mock.patch("utils.poolrunner.PoolRunner.run", apply) as ctx_mgr:
        yield ctx_mgr


@pytest.mark.asyncio
async def test_gamemanager_match(mocked_poolrunner, echo_func):
    args = (1, "a", {})
    kwargs = {"key1": "value1", "key2": None}
    with mock.patch("engine.gamemanager.GameRunners.match", echo_func):
        ret_args, ret_kwargs = await game_manager.match(*args, **kwargs)
    assert args == ret_args
    assert kwargs == ret_kwargs


@pytest.mark.asyncio
async def test_gamemanager_simulation(mocked_poolrunner, echo_func):
    args = (1, "a", {})
    kwargs = {"key1": "value1", "key2": None}
    with mock.patch("engine.gamemanager.GameRunners.simulation", echo_func):
        ret_args, ret_kwargs = await game_manager.simulation(*args, **kwargs)
    assert args == ret_args
    assert kwargs == ret_kwargs


def test_gamerunners_simulation():
    args = ([], 100)
    game = mock.MagicMock()
    with mock.patch("engine.gamemanager.Game",
                    return_value=game) as mocked_game:
        GameRunners.simulation(*args)
    mocked_game.assert_called_once_with(*args)
    game.simulation.assert_called_once()


def test_gamerunners_match():
    args = ([(1, "", ""), (2, "", ""), (3, "", "")], 17, 10)
    match_result = MatchResult(
        10, [RobotId(1, ""), RobotId(2, ""), RobotId(3, "")], [RobotId(2, "")]
    )
    game = mock.MagicMock()
    game.match = mock.MagicMock(return_value=match_result)
    with mock.patch("engine.gamemanager.Game",
                    return_value=game) as mocked_game:
        rounds, scores = GameRunners.match(*args)
    assert rounds == {1: 0, 2: args[1] * match_result.rounds_played, 3: 0}
    assert scores == {1: 0, 2: args[1], 3: 0}
    mocked_game.assert_called_with(args[0], args[2])
    assert mocked_game.call_count == args[1]
    assert game.match.call_count == args[1]

