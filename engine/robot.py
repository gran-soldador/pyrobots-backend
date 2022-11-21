from dataclasses import dataclass, field
import logging
from timeout_decorator import timeout, TimeoutError
from math import radians, isclose, degrees, pi
from typing import Optional
from .constants import *
from .vector import Vector, Pair


BOUNDS = (Vector((0, 0)), Vector((MAXX, MAXY)))


class MisbehavingRobotException(Exception):
    pass


@dataclass(slots=True)
class BotStatus:
    id: int
    name: str
    robot_id: int
    position: Vector
    damage: float
    movement: Vector = field(default_factory=lambda: Vector(cartesian=(0, 0)))
    cannon_cooldown: float = 0.0
    scan_result: Optional[float] = None


@dataclass(slots=True)
class BotCommands:
    drive_direction: float = 0.0
    drive_velocity: float = 0.0
    cannon_used: bool = False
    cannon_degree: float = 0.0
    cannon_distance: float = 0.0
    scanner_used: bool = False
    scanner_direction: float = 0.0
    scanner_resolution: float = 0.0


class Robot:

    def __init__(self, id: int = -1, name: str = "", robot_id: int = -1,
                 position: Pair = (0, 0), damage: float = 0):
        self._status = BotStatus(
            id, name, robot_id, Vector(cartesian=position), damage)
        self._commands = BotCommands()

    def initialize(self):
        raise NotImplementedError("Robot has no initialize code")

    def _initialize_or_die(self):
        try:
            timeout(TIMEOUT)(self.initialize)()
        except TimeoutError:
            pass
        except Exception:
            self._fail("initialize")

    def respond(self):
        raise NotImplementedError("Robot has no respond code")

    def _respond_or_die(self):
        self._commands = BotCommands()
        self._status.cannon_cooldown -= 1
        try:
            timeout(TIMEOUT)(self.respond)()
        except TimeoutError:
            pass
        except Exception:
            self._fail("respond")

    def is_cannon_ready(self) -> bool:
        return self._status.cannon_cooldown <= 0

    def cannon(self, degree: float, distance: float) -> None:
        self._commands.cannon_used = True
        self._commands.cannon_degree = degree
        self._commands.cannon_distance = distance

    def _validate_cannon(self) -> None:
        if not self.is_cannon_ready():
            raise ValueError("Cannon was not available")
        if not 0 <= self._commands.cannon_degree < 360:
            raise ValueError("Invalid angle")
        if not 0 < self._commands.cannon_distance <= 700:
            raise ValueError("Invalid distance")

    def _execute_cannon(self) -> Optional[Vector]:
        """ Execute last cannon request, killing robot if invalid

        :return: Missile destination iff there was a valid cannon request,
        otherwise None
        """
        if not self._commands.cannon_used:
            return
        try:
            self._validate_cannon()
        except ValueError:
            self._fail("cannon")
            return
        self._status.cannon_cooldown = \
            max(2, self._commands.cannon_distance * CANNON_COOLDOWN_FACTOR)
        return Vector(polar=(
            radians(self._commands.cannon_degree),
            self._commands.cannon_distance
        ))

    def point_scanner(self, direction: float,
                      resolution_in_degrees: float) -> None:
        self._commands.scanner_used = True
        self._commands.scanner_direction = direction
        self._commands.scanner_resolution = resolution_in_degrees

    def scanned(self) -> float:
        return self._status.scan_result

    def _validate_scanner(self) -> None:
        if not 0 <= self._commands.scanner_direction < 360:
            raise ValueError("Invalid direction")
        if not 0 < self._commands.scanner_resolution <= 20:
            raise ValueError("Invalid resolution")

    def _execute_scanner(self, positions: list[Vector]) -> None:
        """ Execute last scanner request, killing robot if invalid

        :param positions: Positions of other robots that scanner can detect
        """
        self._status.scan_result = None
        if not self._commands.scanner_used:
            return
        try:
            self._validate_scanner()
        except ValueError:
            self._fail("scanner")
            return
        direction = radians(self._commands.scanner_direction)
        resolution = radians(self._commands.scanner_resolution)
        min_angle = direction - resolution / 2
        max_angle = direction + resolution / 2
        best = float("inf")
        for other in positions:
            relative_position = other - self._status.position
            if angle_in_range(relative_position.angle, min_angle, max_angle):
                best = min(best, relative_position.modulo)
        if best < float("inf"):
            self._status.scan_result = best

    def drive(self, direction: float, velocity: float) -> None:
        self._commands.drive_direction = direction
        self._commands.drive_velocity = velocity

    def _validate_drive(self) -> None:
        if not 0 <= self._commands.drive_velocity <= 100:
            raise ValueError("Invalid speed")
        if not 0 <= self._commands.drive_direction < 360:
            raise ValueError("Invalid angle")
        changed_dir = not isclose(radians(self._commands.drive_direction),
                                  self._status.movement.angle, abs_tol=EPS_ANG)
        stopped = isclose(0.0, self._status.movement.modulo, abs_tol=EPSILON)
        if changed_dir and not stopped and self._commands.drive_velocity > 50:
            raise ValueError("Too fast for changing direction")

    def _execute_drive(self) -> None:
        """ Execute last drive request, killing robot if invalid, and
        applying damage if out of bounds
        """
        try:
            self._validate_drive()
        except ValueError:
            self._fail("drive")
            return
        requested = Vector(polar=(
            radians(self._commands.drive_direction),
            self._commands.drive_velocity / 100.0 * MAXSPEED
        ))
        movement = requested * (1 - INERTIA) + self._status.movement * INERTIA
        position = self._status.position + movement
        if not position.is_bounded(*BOUNDS):
            self._status.damage += 2
            position = position.clamp(*BOUNDS)
            movement = Vector((0, 0))

        self._status.position = position
        self._status.movement = movement

    def get_direction(self) -> float:
        return (degrees(self._status.movement.angle) + 360) % 360

    def get_velocity(self) -> float:
        return self._status.movement.modulo / MAXSPEED * 100

    def get_position(self) -> tuple[float, float]:
        return self._status.position.x, self._status.position.y

    def get_damage(self) -> float:
        return self._status.damage

    def _get_position_vec(self) -> Vector:
        return self._status.position

    def _get_id(self) -> int:
        return self._status.id

    def _apply_damage(self, amount: float) -> None:
        self._status.damage += amount

    def _fail(self, detail: Optional[str] = None) -> None:
        self._status.damage = 100.0
        msg = "Robot failed" if detail is None else f"Robot failed ({detail})"
        logging.getLogger(__name__).debug(msg, exc_info=True)


def angle_in_range(angle: float, min: float, max: float):
    MOD = 2 * pi
    angle = (angle + MOD) % MOD
    min = (min + MOD) % MOD
    max = (max + MOD) % MOD
    if min < max:
        return min <= angle <= max
    else:  # an angle has wrapped around
        return not max < angle < min
