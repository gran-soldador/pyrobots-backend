from dataclasses import dataclass


@dataclass
class Position:
    x: float
    y: float


@dataclass
class BotStatus:
    name: str = ""
    damage: float = 0.0
    velocity: float = 0.0
    direction: float = 0.0
    position: Position = Position(0.0, 0.0)


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
