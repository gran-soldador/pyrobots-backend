from dataclasses import dataclass


@dataclass(slots=True)
class RobotId:
    id: int
    name: str


@dataclass(slots=True)
class Status:
    x: float
    y: float


@dataclass(slots=True)
class ScannerStatus:
    used: bool
    angle: float
    amplitude: float


@dataclass(slots=True)
class RobotStatus(Status):
    damage: float
    scanner: ScannerStatus


@dataclass(slots=True)
class MissileStatus(Status):
    angle: float
    sender: int


@dataclass(slots=True)
class ExplosionStatus(Status):
    pass


@dataclass(slots=True)
class RoundResult:
    robots: list[RobotStatus]
    missiles: list[MissileStatus]
    explosions: list[ExplosionStatus]


@dataclass
class MatchResult:
    rounds_played: int
    players: list[RobotId]
    winners: list[RobotId]


@dataclass
class SimulationResult(MatchResult):
    maxrounds: int
    rounds: list[RoundResult]
