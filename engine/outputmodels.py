from typing import List
from pydantic import BaseModel


# These COULD be dataclasses, as we don't need validation. But we know we are
# inside a REST API, and using a model eases auto generating docs
class RobotId(BaseModel):
    id: int
    name: str


class Status(BaseModel):
    x: float
    y: float


class RobotStatus(Status):
    damage: float


class MissileStatus(Status):
    angle: float
    sender: int


class ExplosionStatus(Status):
    pass


class RoundResult(BaseModel):
    robots: List[RobotStatus]
    missiles: List[MissileStatus] = []
    explosions: List[ExplosionStatus] = []


class MatchResult(BaseModel):
    rounds_played: int
    players: List[RobotId]
    winners: List[RobotId]


class SimulationResult(MatchResult):
    maxrounds: int
    rounds: List[RoundResult]
