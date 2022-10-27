from dataclasses import dataclass, field
from copy import deepcopy
import logging
from math import sin, cos, radians, isclose, sqrt
from typing import Tuple
from .constants import *
from .vector import Vector


@dataclass
class BotStatus:
    name: str = ""
    id: int = -1
    robot_id: int = -1
    damage: float = 0.0
    velocity: float = 0.0
    direction: float = 0.0
    position: Vector = field(default_factory=lambda: Vector(cartesian=(0, 0)))


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

        # Parameters are now valid
        # Now calculating actual movement, accounting for inertia
        angle = self._commands.drive_direction
        modulo = self._commands.drive_velocity / 100.0 * MAXSPEED
        newx = self._status.position.x + cos(radians(angle)) * modulo
        newy = self._status.position.y + sin(radians(angle)) * modulo
        if (not 0 <= newx <= MAXX) or (not 0 <= newy <= MAXY):
            self._status.damage += 2
            newx = min(MAXX, max(0, newx))
            newy = min(MAXY, max(0, newy))
            self._commands.drive_velocity = 0  # Have crashed, is now stopped

        # Saving resulting movement
        self._status.position.cartesian = (newx, newy)
        self._status.direction = self._commands.drive_direction
        self._status.velocity = self._commands.drive_velocity

    def get_direction(self) -> float:
        return self._status.direction

    def get_velocity(self) -> float:
        return self._status.velocity

    def get_position(self) -> Tuple[float, float]:
        return self._status.position.x, self._status.position.y

    def get_damage(self) -> float:
        return self._status.damage

    def _get_distance(self, other) -> float:
        x1, y1 = self._status.position.x, self._status.position.y
        x2, y2 = other._status.position.x, other._status.position.y
        dx, dy = abs(x1 - x2), abs(y1 - y2)
        return sqrt(dx**2 + dy**2)
