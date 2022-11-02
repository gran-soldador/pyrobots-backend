from typing import List
from dataclasses import dataclass


@dataclass
class RobotId:
    __slots__ = ["id", "name"]
    id: int
    name: str


@dataclass
class Status:
    __slots__ = ["x", "y"]
    x: float
    y: float


@dataclass
class RobotStatus(Status):
    __slots__ = ["damage"]
    damage: float


@dataclass
class MissileStatus(Status):
    __slots__ = ["angle", "sender"]
    angle: float
    sender: int


@dataclass
class ExplosionStatus(Status):
    pass


@dataclass
class RoundResult:
    __slots__ = ["robots", "missiles", "explosions"]
    robots: List[RobotStatus]
    missiles: List[MissileStatus]
    explosions: List[ExplosionStatus]


@dataclass
class MatchResult:
    rounds_played: int
    players: List[RobotId]
    winners: List[RobotId]


@dataclass
class SimulationResult(MatchResult):
    maxrounds: int
    rounds: List[RoundResult]
