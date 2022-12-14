from utils.poolrunner import PoolRunner
from .game import Game
from .outputmodels import SimulationResult


class GameRunners:
    """GameRunners

    Wrappers to be used by GameManager in child processes
    """
    @staticmethod
    def simulation(robots: list[tuple[int, str, str]],
                   num_rounds: int) -> SimulationResult:
        return Game(robots, num_rounds).simulation()

    @staticmethod
    def match(robots: list[tuple[int, str, str]],
              num_games: int,
              num_rounds: int) -> tuple[dict, dict]:
        rounds = {r_id: 0 for (r_id, _, _) in robots}
        scores = {r_id: 0 for (r_id, _, _) in robots}
        for _ in range(num_games):
            result = Game(robots, num_rounds).match()
            for winner in result.winners:
                rounds[winner.id] += result.rounds_played
                scores[winner.id] += 1
        return rounds, scores


class GameManager:
    """GameManager

    Wraps Game so that it is run in a separate process, to avoid problems
    with multithreaded code.
    """
    def __init__(self):
        self._runner = PoolRunner()

    async def match(self, *args, **kwargs):
        return await self._runner.run(GameRunners.match, *args, **kwargs)

    async def simulation(self, *args, **kwargs):
        return await self._runner.run(GameRunners.simulation, *args, **kwargs)


game_manager = GameManager()
