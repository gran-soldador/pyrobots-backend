from dataclasses import dataclass, field
from copy import deepcopy
import logging
from math import sin, cos, radians, isclose

MAXX = 1000.0  # in meters
MAXY = 1000.0
MAXSPEED = 100  # in meters/round at 100% speed


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


@dataclass
class BotCommands:
    drive_direction: float = 0.0
    drive_velocity: float = 0.0


class Robot:

    def __init__(self):
        self._status = BotStatus()
        self._commands = BotCommands()

    def initialize(self):
        raise NotImplementedError("Robot has no initialize code")

    def _initialize_or_die(self):
        prev_status = deepcopy(self._status)
        try:
            self.initialize()
            assert self._status == prev_status
        except Exception:
            logging.getLogger(__name__).debug("Robot failed when initializing",
                                              exc_info=True)
            self._status = prev_status
            self._status.damage = 100

    def respond(self):
        raise NotImplementedError("Robot has no respond code")

    def _respond_or_die(self):
        prev_status = deepcopy(self._status)
        self._commands = BotCommands()
        try:
            self.respond()
            assert self._status == prev_status
        except Exception:
            logging.getLogger(__name__).debug("Robot failed when responding",
                                              exc_info=True)
            self._status = prev_status
            self._status.damage = 100

    def is_cannon_ready(self) -> bool:
        pass  # pragma: no cover

    def cannon(self, degree: float, distance: float) -> None:
        pass  # pragma: no cover

    def point_scanner(self, direction: float,
                      resolution_in_degrees: float) -> None:
        pass  # pragma: no cover

    def scanned(self) -> float:
        pass  # pragma: no cover

    def drive(self, direction: float, velocity: float) -> None:
        self._commands.drive_direction = direction
        self._commands.drive_velocity = velocity

    def _execute_drive(self) -> None:
        if not 0 <= self._commands.drive_velocity <= 100:
            raise ValueError("Invalid speed")
        if not 0 <= self._commands.drive_direction < 360:
            raise ValueError("Invalid angle")
        changed_dir = not isclose(self._commands.drive_direction,
                                  self._status.direction)
        stopped = isclose(0.0, self._status.velocity)
        if changed_dir and not stopped and self._commands.drive_velocity > 50:
            raise ValueError("Too fast for changing direction")

        angle = self._commands.drive_direction
        modulo = self._commands.drive_velocity / 100.0 * MAXSPEED
        newx = self._status.position.x + cos(radians(angle)) * modulo
        newy = self._status.position.y + sin(radians(angle)) * modulo
        if (not 0 <= newx <= MAXX) or (not 0 <= newy <= MAXY):
            self._status.damage += 2
            newx = min(MAXX, max(0, newx))
            newy = min(MAXY, max(0, newy))
        self._status.position.x = newx
        self._status.position.y = newy
        self._status.direction = self._commands.drive_direction
        self._status.velocity = self._commands.drive_velocity

    def get_direction(self) -> float:
        pass  # pragma: no cover

    def get_velocity(self) -> float:
        pass  # pragma: no cover

    def get_position(self) -> Position:
        pass  # pragma: no cover

    def get_damage(self) -> float:
        pass  # pragma: no cover
