from dataclasses import dataclass, field


@dataclass
class Position:
    x: float = 0.0
    y: float = 0.0


@dataclass
class BotStatus:
    name: str = ""
    id: int = -1
    damage: float = 0.0
    velocity: float = 0.0
    direction: float = 0.0
    position: Position = field(default_factory=Position)


class Robot:
    def __init__(self):
        self._status = BotStatus()
        # TODO: Agregar atributos para almacenar acciones y sus resultados

    def initialize(self):
        pass

    def respond(self):
        pass

    def is_cannon_ready(self) -> bool:
        pass

    def cannon(self, degree: float, distance: float) -> None:
        pass

    def point_scanner(self, direction: float,
                      resolution_in_degrees: float) -> None:
        pass

    def scanned(self) -> float:
        pass

    def drive(self, direction: float, velocity: float) -> None:
        pass

    def get_direction(self) -> float:
        pass

    def get_velocity(self) -> float:
        pass

    def get_position(self) -> Position:
        pass

    def get_damage(self) -> float:
        pass
